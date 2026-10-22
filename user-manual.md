# NutriMagnus User Manual

*Updated 2026-10-22:1127* / Reading time: 9 hours, 21 minutes

*Last full audit: 2026-10-09* / [Disclaimer](/disclaimer)

<!-- t:26-10-02:0741 Today I will start marking sections I have reviewed/edited with HTML comment of this sort. I have previously reviewed many sections, but not marked them, but I need to know which sections have not yet been reviewed so this is how I'll keep records. A section no so marked may be one of those previously reviewed, but it will take me a while to catch up with such sections, and I may not recall them all anyway. I may or may not append a comment to the basic flag comment, the first of which may be seen below. -->

<!-- t:26-10-02 -->

**NutriMagnus ("NuMa")** is a computer program with open source (publicly available) code which provides a thorough nutritional analysis of a user's food choices. NuMa has special resources for tracking and analysis of protein because this is a problem for those eating primarily a plant-based diet, for older people, and for the chronically-ill:

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

NuMa runs as a web app, opened in your ordinary browser — once it's installed (Part 1, section A), there's no command line involved.

- Read **Part 1** (To get a quick start) for a fast orientation before diving in.
- Read **Part 2** (Introduction) for the ideas behind the program.
- Read **Part 3 — Using the Web App** for how to actually operate NuMa.
- Read **Part 4** (Core nutrition concepts) for more of the ideas behind the program.
- Read **Part 5** (Reading Your Results) whenever you want to know what a column or table means.
- Read **Part 6** (Shared Operations) for behaviors that show up in more than one place in the app, explained once.
- Parts 7 to 10 apply to everyone; Part 11 logs recent program updates.
- Trying to find something in this document itself, not in the app? See [Using this manual's search](#search-howto) — it works differently from a plain text search.

## Part 1 — To get a quick start <!-- t:26-10-04 -->

*(Reading time: 18 minutes)*

### A. Download and install the program <!-- t:26-10-03 -->

*Search terms: installation, installer, setup, get the program, get NuMa.*

NuMa runs on Windows and on Linux. Find your own system below and ignore the other — the two are installed quite differently. Whichever you're on, read [What kind of program this is](#install-webapp-note) at the end; it explains something about NuMa that surprises nearly everyone at first.

#### Windows {: #install-windows}

*Search terms: Windows 10, Windows 11, SmartScreen, blocked download, virus warning, upgrade, upgrading, uninstall, Start menu.*

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

*Search terms: installation, Debian, Mint, Fedora, upgrade, uninstall, app menu, AppImage.*

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

Your data doesn't live in the installed program: it's in two folders in your home folder, `~/.local/share/numa` and `~/.config/numa`, so updating or reinstalling NuMa leaves it untouched. See [Backing up your data](#backup).

#### What kind of program this is {: #install-webapp-note}

*Search terms: offline, no internet, privacy, private, localhost, server, page won't load, site can't be reached, connection refused, hibernate.*

NuMa is a "web app" — it runs quietly in the background and shows its screens in a browser tab, like a website, but it's talking only to itself on your machine. It doesn't need the internet to run at all, and nothing you enter leaves your computer; NuMa reaches out only when you look up a food in an online [database](#gloss-database), or when it checks whether a newer version has been released. Two things follow from all this:

   - **The browser tab and the program are different things.** Closing the tab doesn't close NuMa — it's still running. To get back, start NuMa again the way you normally do (which opens a fresh tab) or open a new tab yourself to the same address.
   - **Sleep can disconnect the tab.** If your computer sleeps or hibernates while NuMa is open, the background program may stop and need restarting when it wakes — you'll typically see the tab fail to load. This is expected, not a sign anything's broken. Start NuMa again to relaunch it; your data is on disk and unaffected.

#### What's on your computer, and why {: #installed-files}

*Search terms: uninstall, uninstalling, file locations, where my data is stored, disk space.*

NuMa puts only a handful of files on your computer. The program itself is one file; everything else is either a menu shortcut or your own data.

**The program**

| File | What it's for |
|---|---|
| `nutrimagnus.exe` (Windows, in the folder you chose) or `~/.local/bin/nutrimagnus` (Linux) | The whole program, in one file. The built-in User Manual and NuMa's reference tables (oxalate, glycemic index, the UK, Australian and French food tables, starter foods and recipes) are packed inside it. |
| `~/.local/share/icons/nutrimagnus.png` (Linux) | NuMa's icon, for the applications menu. |
| `~/.local/share/applications/nutrimagnus.desktop` (Linux) | The applications-menu entry that starts NuMa. |

**Your data** — created the first time NuMa runs, and never touched by an update. On Windows these folders are `%LOCALAPPDATA%\numa` (data) and `%APPDATA%\numa` (settings); on Linux, `~/.local/share/numa` and `~/.config/numa`.

| File | What it's for |
|---|---|
| `numa.db` (data folder) | Everything you've entered: your Food Cache, pantry, recipes, logged meals, [GI](#gloss-gi) and [DIAAS](#gloss-diaas) notes, and the rest. The one file that matters most to back up. |
| `prefs.json` (data folder) | How you like the pages: sort orders, chosen columns, dismissed notices. |
| `demo_data.json`, `demo_data_seed_attempted`, `starter_versions.json` (data folder) | Small notes about the [starter foods and recipes](#starter-data): which were loaded, and which version of them you have. |
| `manual/` (data folder) | Only if you've clicked **Update manual now**: a newer User Manual than the one inside the program. |
| `gi_data_local.json` (data folder) | Only if you've built it in Settings → 7: your own copy of the 2021 glycemic index tables. |
| `config.json` (settings folder) | Your [USDA](#gloss-usda) key, if you've entered one, and the search-depth setting. |
| `profiles/`, `active_profile.txt` (settings folder) | Your profiles (age, weight, activity level, targets) and which one is in use. |

To remove NuMa completely, delete the program file (and on Linux the icon and menu entry), then both folders above. To keep your data, keep the folders — see [Backing up your data](#backup).

#### Backing up your data {: #backup}

*Search terms: migrate, migration, transfer, data loss, lost data, sync, safe copy.*

This section covers your data's location — where NuMa keeps it on your computer — and its storage, backing it up, restoring it, and moving your data to a new computer.

Everything you put into NuMa lives in two folders on your computer, kept apart from the program itself: your foods, pantry, recipes, logged meals, annotations, profile and settings, and your 2021 glycemic index table if you built one (do this in Settings, item 11).

   - **Windows:** `%LOCALAPPDATA%\numa` and `%APPDATA%\numa`. Type either one, exactly as written, into File Explorer's address bar and press Enter to open it.
   - **Linux:** `~/.local/share/numa` and `~/.config/numa`. These are hidden folders in your home folder; press Ctrl+H in your file manager to show them.

**To back up,** copy both folders somewhere safe — a memory stick, an external drive, or a cloud-synced folder. Do it when NuMa isn't in the middle of saving something; the simplest way is to do it before you start NuMa for the day. Repeat it now and then: a backup only holds what you'd entered when you made it.

**To restore, or to move your data to another computer** — a new computer, or one whose system was wiped — install NuMa as described above, but don't start it yet. Copy both backed-up `numa` folders into place, replacing any that exist, and then start NuMa. Everything comes back as it was.

A [CSV](#gloss-csv) export from the Food Cache or Recipes pages is *not* a full backup. It's for moving selected foods or recipes around, and leaves out your meals, pantry, profile and settings.

### B. Start with what's easiest <!-- t:26-10-03 -->

*Search terms: getting started, beginner, first steps, where to begin, new user, learning curve.*

This is a complex and powerful analytical program. A careful Internet search reveals that it is unique in its power and depth. It can be successfully approached by moving slowly and thoughtfully, with real benefit obtained early from using some of its easiest and simplest features. 

Start with what is easiest to understand: analysis of single foods and simple recipes. Use the manual to learn more. Do not expect to learn it all in a few sessions. [Contact us](#feedback) quickly rather than slowly if you start to get overwhelmed — one of our goals is to minimize the risk of that happening!

### C. Simple tips for new learners <!-- t:26-10-03 --> 

*Search terms: getting started, beginner, how to learn, learning curve, how long to learn, practice.*

**Slow down and look carefully at what you see on your screen.** What you see is the interface between you and the program. By design, it is rich in information. You don't need to understand or use all of it immediately, but notice that there are often links such as "Learn more ==>" or "Why?" encouraging you to link to a section of the manual that will tell you much more about something. We've worked very hard on the Manual, with the hope that it will both help you and educate you.

**Plan frequent program usage in the beginning.** Learning a powerful tool requires time and frequent contact. You have two critical things to learn: basic concepts (covered in [Part 4](#coreNutrition)) and the interface itself, including the functions listed on the main menu items' drop-down menus (see [Finding your way around](#web-shortcuts) in Part 3, and [Using the Foods menu](#foods-menu-web) and the sections after it for each menu in turn). **If you don't commit to daily use of the program, for about a week, you will not get past the slow-fumbling stage.** What you are dealing with is a Boeing 727, not a Piper Cub. Learn the cockpit and you can be a world traveler! (And that learning can come gradually, but daily exposure is the key.)

### D. NuMa often learns from YOU as you use it <!-- t:26-10-03 -->

*Search terms: autocomplete, history, remembered choices, faster, speed.*

While we don't yet have on-board local [AI](#gloss-ai) to help you with NuMa and your food questions, we do have NuMa remembering recent entries you've made to text input boxes, and a number of different options you've selected. Rather quickly, this will make use of the program easier and quicker.

One huge asset is the [Food cache](#FoodCache) [database](#gloss-database) you'll set up. This serves as a memory of every food you've looked up or put into your Pantry. Saved is the food name, [ID](#gloss-id) number, and nutrition data. Data retrievals from the online [databases](#gloss-database) take time; retrievals from you personal Food cache are essentially instant.

### E. Stuck? You have help nearby, and an on-call expert to assist you. <!-- t:26-10-03 -->

*Search terms: support, contact, bug, error, not working, ask a question, can't find.*

It happens to us all! You can first look in this manual's [Part 8 — Troubleshooting and feedback — reporting problems and offering ideas](#feedback) to see if your problem has an identified fix.

If you're wondering how to do something, search the Manual for one or two key words. For an especially efficient search, click the "Only show things you can do" checkbox that is right below the Manual's search text input box.

Still stuck? You need help...and it's readily available. Learn more...[here](#quickhelp).

### F. You can start food inputs with estimates, in many cases, but... <!-- t:26-10-03 -->

*Search terms: weigh, weighing, food scale, grams, cups, spoons, measuring, eyeball, guess, amounts, portion size.*

Use a kitchen scale to determine food quantities, if at all possible. It's easier than you may think, and much more accurate.

Regardless of how you eat, you will have to tell the program WHAT you are eating and HOW MUCH. The absolute best way to do this is to give it a weight. Sometimes you can just give it a "portion" or a volume measure instead, and the program will figure out the weight for you from that so it can keep going. However, remember that approximations are better than nothing, so if you can do nothing else, try to give NuMa an approximate amount.

Without the program you're flying blind. With it, even if you only use volume measures, there will be some errors of measurement, but you're still much better informed about what's happening than before. In some cases, though, a volume measure just doesn't work well. If that happens to you, [get in touch](#feedback) and we'll figure it out together. All in all, it's by far best to have and use a kitchen scale. I have had a small Oxo scale for years. It's excellent. There are others you can consider as well, but I do suggest that you get one.

### G. Setting NuMa up: first time, or after losing your data <!-- t:26-10-03 --> {: #first-setup}

*Search terms: first run, initial setup, setup checklist, configuration, getting started, reinstall, new computer.*

Use this list the first time you run NuMa. Use it again if your computer was wiped or replaced and your NuMa data wasn't saved.

**Lost your data? Check this first.** If you have a backup of NuMa's two data folders, restore it — see [Backing up your data](#backup). Everything comes back, and you can skip the rest of this list. Only without a backup do you need the steps below.

**Starter foods and recipes.** A fresh install doesn't start empty. Your Food Cache and Recipes list already hold a small set of starter items: common foods, most with full amino acid data, and a few recipes showing protein complementing at work. Their names begin with an asterisk and a space (for example, `* Quinoa, cooked`), so you can always tell them apart from anything you've added yourself. Keep them or remove them as you like — see Step 2.

#### Step 1 — Settings you must address before you start

*Search terms: required settings, personal details, vegan, configuration, blank percentages, empty targets.*

Go to **Settings**. Until these three are done, NuMa's results are either blank or quietly misleading.

1. **Your Profile (section 1).** Enter your age, sex, weight, height and activity level. Without them, every "% of daily target" column is blank. On the same form, also set:
    - **Your glucose tolerance** — choose impaired glucose tolerance if you have diabetes, pre-diabetes or insulin resistance, normal if you don't. It sets which [GI](#gloss-gi) values the lookup shows first, and tailors the note NuMa shows beside a [GI](#gloss-gi) [measured in people with diabetes](#gi-impaired);
    - the **oxalate lookup** checkbox, if oxalates matter to you (for kidney stones, say);
    - optionally, a **daily glycemic load target**, if you want each day's [GL](#gloss-gl) checked against a ceiling ([more](#gl-target)).
2. **Dietary Preferences (section 3).** Choose all foods, vegetarian, or plant-based only. This filters *every* search and suggestion in NuMa, so a wrong setting hides foods you'd expect to see.
3. **[USDA](#gloss-usda) [API](#gloss-api) Key (section 6).** NuMa gets most of its food data from the US government's FoodData Central website. That site asks every program that uses it to identify itself with a **key**: a long code, like a password, that USDA gives out free to anyone who asks. Until you enter your own, NuMa uses one shared key for all its users, and when that shared key gets overused your food searches can fail for a while. Getting your own takes about a minute and costs nothing — see [how to get a USDA key](#food-data).

Then open **Computed Daily Targets (section 2)** and glance at the targets calculated for you, to check they look sensible.

#### Step 2 — Settings worth doing at some point

*Search terms: optional settings, preferences, configuration, default browser, recommended targets.*

- **Protein Digestibility Overrides (section 4):** nothing to do now. It's for later, if you find a better digestibility figure for a particular food.
- **Nutrient Targets - Researched (section 5):** click **Load recommended Revised Optimal targets**, and add Max limits for anything you need to keep low.
- **Glycemic Index Reference Table (section 7)** — only if you plan to track glycemic index (see Step 4): build the 2021 table ([how](#gi-editions)). Do this before Step 4 below, so your values come from the better table.
- **Meals & Log columns (section 10):** choose which nutrient columns your meal lists show.
- **Starter Data (section 11):** decide whether to keep the starter foods and recipes, or clear them.
- **Browser to Launch (section 13):** pick a browser, if you run more than one and don't want to be asked which each time.

#### Step 3 — Set up your pantry

*Search terms: staples, groceries, everyday foods, favorite foods, kitchen cupboard.*

Your pantry is the list of foods you actually keep at home and use often. NuMa looks there first when it suggests foods to fill a protein gap, so a good pantry makes those suggestions practical ones.

**Getting the foods you often use into your pantry database, with complete nutritional information, is critical.**

Here's the problem: NuMa cannot work with data it doesn't have. Foods from reliable online databases often lack protein amino acid data, have incomplete Omega fatty acid data, and always lack GI (glycemic index) data. Getting this information into the foods you eat most often is the most important focus to have. Use the Foods menu item 9 to find problems with you pantry foods (and others). The, use the Analysis menu item 3 to identify the foods you use most often. Any foods with problems which are frequently used should get cleaned up first.

1. Look through [Appendix B](#appendix-plant-proteins) and note the foods there that you have, or would buy. Make a list!
2. **Check the starter foods first.** Some of the foods you want are probably already in your Food Cache as starter foods — the ones whose names begin with `* `. They come with their nutrient data already checked, so using them saves real time. Go to **Foods → Food Cache**, type `*` in the filter box to list them, and add the ones you want to your pantry from there.
3. For anything not among them, go to **Foods → My Pantry** and add it **by search**, picking a result from the list. Only a search-and-select brings in the food's nutrient data, including its amino acids.
4. Prefer results with a ✓ in the **[AA](#gloss-aa)** (amino acid) column. Only foods with amino acid data can be used in protein suggestions, and plain, unbranded [USDA](#gloss-usda) entries are the likeliest to have it.
5. Can't find a food right away? Open **Can't find it? Save just the name for now** under the search box to save just its name, and link it to real data later with **Link a food**.

#### Step 4 — Glycemic index values for your core foods (optional)

*Search terms: blood glucose, diabetic, carbs, low GI, insulin.*

**Most people can skip this step.** It's only for those who want to track glycemic index (GI) — for example, because of diabetes or pre-diabetes, or to manage blood sugar swings. If that isn't you, you're done.

NuMa never fills in GI values by itself; each one is a choice you make from the reference table. You don't need GI for everything, only for the **carbohydrate foods you eat most often**: grains, bread, rice, pasta, oats and breakfast cereals; potatoes and other starchy vegetables; beans and lentils; fruit; sweeteners. Skip foods with little carbohydrate (oils, most nuts, tofu, meat, fish, eggs, cheese) — a GI number means little for them.

For each food, go to **Foods → Annotate**, click **Edit**, and use **Look up a GI value from the published reference table**. When choosing between results (fuller guidance: [Choosing a GI value](#choosing-gi-values)), prefer, in this order:

1. **The same food, prepared the same way.** Boiled versus baked, whole grain versus flour, and cooking time all change GI a lot.
2. **The population that matches you** — normal or impaired glucose tolerance ([which to use](#choosing-gi-values)).
3. **Rows not flagged as "non-ISO method"** — that is, studies that didn't follow the international measuring standard, [ISO](#gloss-iso) (International Organization for Standardization) 26642 ([more](#gi-method-quality)).
4. **More recent studies, with more people tested and a smaller ± (standard error).**

If nothing is a genuine match, leave the value blank. No value is better than a wrong one. See [How to read a lookup result](#gi-result-row) for what each part of a result means.

Adding a food to your pantry or a meal also offers to ask you for its GI, so if you're tracking GI, say yes there too.

#### After an update: new starter items

*Search terms: upgrade, what's new, release notes.*

From time to time, a new version of NuMa adds starter foods or recipes, or improves ones you already have. **NuMa tells you.** The **UPDATE AVAILABLE** message says what an update will change in them before you install it, and the first time the new version runs, a **NEW STARTER ITEMS** message on the home page says what it added or improved. Nothing in your data changes on its own; you choose, in [Settings → 11. Starter Data](#starter-data).

### H. Skim Part 2, A and F, just to know they exist. <!-- t:26-10-03 -->

While looking at section A, make a few notes about what you'd like to try first.

Seriously consider what is suggested in section F - looking at the workflows can quickly show you major program features.

### I. Consider investing some time with Part 4 <!-- t:26-10-03 -->

*Search terms: jargon, terminology, glossary, definitions, unfamiliar words, nutrition basics.*

This program necessarily uses some specialized vocabulary. You have two options:

1. Learn the basics before diving into the program's functions and output.
2. Dive in first, and use the "Learn more..." links you'll see to immediately jump to the relevant manual section, so you can understand whatever's in front of you right when you need to.

---

## Part 2 — Introduction to NutriMagnus, a tool for intelligent eating: what you can do with this tool and why it matters

*(Reading time: 12 minutes)*

---

### A. What a user can do with NutriMagnus — brief overview

*Search terms: features, what it does, capabilities, menus.*

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
    - **What-if: meals**: see how your average daily nutrition over a set of days would change if you removed, added, replaced or cut down foods and recipes — without changing anything — see [What-if: Meals](#whatif)
    - **What-if: recipes**: the same for your recipes — how each one's nutrition per serving would change if you removed, added or replaced an ingredient — see [What-if: Recipes](#whatif-recipes)
- **Settings**
    - Color theme
    - Personal profile (age, sex, weight, height, activity level)
    - Dietary preferences
    - Editor command
    - Advanced options: your personal [USDA](#gloss-usda) [API key](#food-data) (a free code from USDA's website that increases how many food searches you can do), and protein digestibility overrides

**Detailed how-to guides for each menu area follow later in this manual.** If you prefer to learn by example before reading explanations, skip ahead to [Sample Workflows](#sample-workflows) at the end of this introduction — it points you to a set of annotated walkthroughs.

### B. NutriMagnus addresses two serious problems

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

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

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

In very brief summary, as we age, we tend to lose muscle mass, utilize dietary protein less efficiently, and simply eat less. These factors compound to create a perfect storm of vulnerability to general ill-health and the often dire consequences of falls. And these issues affect women more than men. Put simply - getting enough of the right sort of protein matters far more than most people realize. A good diet is utterly necessary, but not by itself sufficient. It must be complemented with adequate resistance exercise.

There is very little discussion of the problem in the mass media. So, it is up to use as individuals to self-educate and then make carefully considered decisions about our diet. But this is almost impossible to do without serious technical help, as the nutritional factors involved go well beyond simple arithmetic or the naively simple view offered to us by the first major statements about plant protein complementarity in the very early '70s.

### D. NutriMagnus is the missing helper

*Search terms: plant-based, why NuMa, purpose, other nutrition apps, Cronometer, MyFitnessPal.*

These are technical problems that are beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far toward solving this problem. This is what this project is about.

Nutrition analysis programs, both paid and free open source, already exist but none that we've seen focus on the problems faced by vegetarian and vegan folks. And none have the rich features and readily modifiable design that we want. The NuMa program addresses both problems in detail. It also suggests complementary foods that can be combined with a food or recipe or meal to create [complete proteins](#gloss-complete-protein) in one's diet.

NuMa has been under intense development and is still being developed. Over time, new users will experience unanticipated needs and the program can be further developed to meet them. This is one reason why [reporting problems](#feedback) is so important - feedback drives program development.

### E. Data, testing, and validation: Why you can trust NutriMagnus (NuMa) {: #data-testing-validation}

#### Reliable data sources

*Search terms: where the numbers come from, trustworthy, accuracy, reliability.*

**[NuMa](#gloss-numa) draws on multiple data sources, and tells you which ones it is using.** Wherever the program makes a suggestion, it shows you which sources it consulted.

- **[USDA](#gloss-usda) FoodData Central**[^2] — the primary nutrient [database](#gloss-database), one of the most comprehensive public nutrition sources in the world. Used for most food searches.
- **Open Food Facts**[^3] — supplements [USDA](#gloss-usda) for branded and international foods, especially packaged products with a barcode.
- **Canadian Nutrient File** — Health Canada's reference [database](#gloss-database); particularly good amino acid coverage, which helps with [DIAAS](#gloss-diaas) calculations.
- **UK CoFID** (Composition of Foods Integrated Dataset) — ~2,900 UK foods from Public Health England/[DHSC](#gloss-dhsc); strong on macros, minerals, and vitamins, but has no amino acid data of its own.
- **Australian AFCD** (Australian Food Composition Database) — ~1,600 Australian foods from [FSANZ](#gloss-fsanz); also has real amino acid coverage, like Canadian Nutrient File.
- **French [CIQUAL](#gloss-ciqual)** — ~3,480 French/European foods from [ANSES](#gloss-anses) (2025 edition); like CoFID, no amino acid data. 

See [Food data — where it comes from and how it is stored](#food-data) in Part 7 for more on all six of NuMa's sources.

In addition, the following internal data sources are used:

- **Harvard T.H. Chan School of Public Health oxalate table**[^11] — a 433-food reference table used to fill in [oxalate](#gloss-oxalate) content when [Oxalate data](#oxalate) is switched on in Settings. (This is optional and is off by default.)
- **Atkinson/Brand-Miller international glycemic index tables**[^8] — a published reference table of about 2,500 foods, used to fill in [Glycemic Index](#gi) estimates automatically, rather than requiring you to type them in from scratch. A newer edition of over 4,000 foods can be added to your own copy of NuMa in a few minutes — see [Upgrading to the 2021 tables](#gi-editions).
- **NuMa's own curated protein-complement table**[^10] — a built-in list of 25 common protein sources used as a fallback for amino-acid data in complement suggestions, when your own data doesn't cover a gap.
- **Your own data** — foods saved to your [Pantry](#pantry), and [recipes you have analyzed](#recipes-menu-web), are consulted ahead of every other source above.


#### Extensive code testing

*Search terms: quality control, accuracy, reliability.*

**[NuMa](#gloss-numa) has an extensive, fully automated test process.** As of this writing (2026-09-30), there are 1,311 automated checks the program must pass after every single change before it ships — everything from "does this page load" to "does this specific nutrition calculation come out to exactly the right number." Some of these don't just check a handful of hand-picked examples: they generate hundreds of realistic, random inputs and confirm a mathematical rule holds true for every one of them, and a newer, smaller set actually drives the app in a real browser window, end to end, rather than only checking the code in theory.

**NuMa is also periodically checked with a technique called mutation testing** — a way of testing the tests themselves. It works by deliberately planting a small, wrong change somewhere in the code (say, swapping a plus for a minus) and rerunning the test suite to see whether anything notices. If nothing does, that's a real, measurable blind spot — a piece of logic nothing is actually watching, something an ordinary "all tests passed" report can't reveal on its own. This has already found and closed several genuine gaps in NuMa's most complex code, the protein-quality math in particular, including places where a test was checking the right general idea but not the exact number, and places where one path through the code was covered while a nearby one wasn't covered at all.

**The protein-complement suggestion engine and the Claude AI fetch/import workflow each have their own extensive, dedicated test coverage**, on top of everything above. What each of those actually does is explained in plain language in [Protein Complement Suggestions](#comp) through [Two-step combinations](#comb), and in [Fetching missing data with Claude AI](#fetch).

*(For technically skilled users: the full file-by-file test breakdown, the specific tools used, and mutation-testing methodology/results are documented in README-numa-documentation.md's Test Suite and Maintenance sections.)*

#### Validation you can replicate yourself

*Search terms: check the math, verify, reproduce, proof.*

**Appendix F has a fully worked out validation example.** You can do this yourself, if you like. Data are brought in from outside the program and run through the official correct computation process. Full source references are given. You can run the same computation in [NuMa](#gloss-numa) and compare the result.

#### Reasonable expectations: bugs remain

*Search terms: mistakes, wrong results, report a problem.*

**Problems may appear anyway.** As professional programmers will tell you, all programs have bugs. This is more likely for new ones than for those which have been around for years. This is why you should report any result you are getting which doesn't make sense to you. There is a small chance you've found a "bug", but a greater chance that the program simply needs to explain itself to you more clearly. Either problem will be fixed ASAP, and all such fixes benefit everyone who uses the program.

**How to report suspected errors or problems with the program:** see [Getting more help](#feedback) in Part 8.

---

### F. Sample Workflows {: #sample-workflows}
**If you'd prefer to learn by example before reading explanations,** fully worked, step-by-step walkthroughs are provided later in this manual — see [Sample Workflows](#sample-workflows-web) in Part 3. You don't need to read Part 4 or Part 5 first.

---

## Part 3 — Using the Web App

*(Reading time: 48 minutes)*

NuMa's web app runs in your ordinary browser. This makes program development, which is ongoing, easier, and also provides the user with an interface they are already at least partly familiar with.

### A. Opening NutriMagnus

*Search terms: start the program, open NuMa, page won't load.*

Launch NuMa the way it was set up on your computer — a desktop icon, an Applications-menu entry, or a shortcut someone set up for you. It opens automatically in your browser, normally at a browser address like `http://127.0.0.1:8000` — this just means "this computer, talking to itself," not an address on the internet, so don't worry if the exact numbers you see differ. If the page doesn't load right away, wait a few seconds and reload — the program is still starting up.

#### What you see on the home page {: #home-page-tour}

*Search terms: start page, dashboard.*

The home page opens with a short reminder that NuMa is not medical advice, then the **Welcome to NutriMagnus** heading, a one-line description of NuMa, and these status lines:

- **Dietary preferences** — your current setting (e.g. "All animal foods"), with a link straight to Settings to change it.
- **Active profile** — a one-line summary of your profile (age, sex, weight, height, activity level), or "not set" with a link to configure one if you haven't yet.
- **Current manual version / Current program version date** — the date of the manual you're reading and of the exact build you're running, both as `yyyy-mm-dd:hhmm`, followed by a **see what changed** link into the [Recent program updates log](#updates-log), whose newest release summary opens with a short *Version overview*. Right after it, a **Check for updates now** link re-checks GitHub immediately instead of waiting for the periodic check — useful right after dismissing an UPDATE AVAILABLE banner if you change your mind, since it also undoes that dismissal. It only appears when no update is currently showing.

Above the heading, a few one-time or conditional banners can appear when relevant: a **Your profile isn't set yet** message until your profile is saved (it links to Settings and to the [setup steps](#first-setup), and has a **Don't remind me about this again** checkbox), a **NEW STARTER ITEMS** message the first time a new version runs, if it added or improved starter foods or recipes (see [Starter Data](#starter-data)), a [database](#gloss-database)-integrity warning, an "update installed" confirmation right after using Update Now, an update-failed message, and an **UPDATE AVAILABLE** banner when a newer release exists on GitHub. If you're running the packaged Linux install, this shows an **Update Now** button that installs the update in place; otherwise (Windows, or a non-packaged Linux checkout) it shows a **Download NutriMagnus** button that goes straight to the new installer file. That banner says what the update would add to or improve in the [starter foods and recipes](#starter-data) you have, and has a **Don't show this again for this version** checkbox — same idea as the System Issues banner's "Got it" checkbox below. While it is showing, the separate **New user manual available** banner is left out, since the program update brings its own manual with it. The very bottom of the page gives the release and build numbers, e.g. *NutriMagnus 0.1.0-rc.26 (build 2026-10-17:0722)*.

**When does NuMa actually check for a new release?** Every time the home page loads — at launch, on a manual reload, or by navigating back to it from anywhere else in the program — it asks whether a newer version exists. That check itself is cached for a few hours, so bouncing back to the home page repeatedly doesn't re-contact GitHub every time; it just reuses the last answer until the cache expires. Once a newer version is available, the **UPDATE AVAILABLE** banner shows on every single page load — it never disappears on its own — until you either install the update or check the "Don't show this again for this version" box; a later, different release always shows regardless of what you've dismissed.

### B. Finding your way around {: #web-shortcuts}

*Search terms: hotkeys, menu bar.*

Every page has the same navigation bar across the top: **NuMa** (takes you home), **Foods**, **Recipes**, **Compare**, **Meals & Log**, **Analysis**, **Settings**, and **Manual** (this document). **Foods**, **Recipes** and **Analysis** open as drop-down menus with several choices each; the others go straight to their page.

If you'd rather use the keyboard, each nav item has a shortcut — hold **Alt+Shift** and press the item's first letter (`F` for Foods, `R` for Recipes, `C` for Compare, `M` for Meals & Log, `N` for Analysis, `S` for Settings, `A` for Manual), using the underlined letter shown in each menu item and Settings section heading (e.g. `Alt+Shift+3` jumps to Dietary Preferences within Settings; section 10, Meals & Log columns, is `Alt+Shift+0`; sections 11 to 15 use an underlined letter of their name: `T` for Starter Data, `K` for Keyboard Shortcuts, `B` for Browser to Launch, `D` for Data Quality Reminder, and `Y` for System Issues, since `S` already belongs to Settings). This works the same way in any desktop browser (Firefox, Chrome, Brave, Edge, and the rest) — it's NuMa's own page script listening for the key combination, not a browser-specific feature, so it isn't limited to whichever browser you happen to be using. For a dropdown menu item (Foods, Recipes, Analysis), the shortcut also moves keyboard focus straight to the first item in the menu that opens — from there, ArrowUp/ArrowDown moves between items, Enter or Space picks one, and Escape closes the menu, all without touching the mouse. On any page with a search box (a meal's or a recipe's add search, Foods: Search, Pantry, Food Cache, Compare, and the rest), `Alt+Shift+I` puts the cursor in that search box with its text selected, ready to type a new search — opening the section it sits in first if that's closed. It's unrelated to, and does not affect, anything stored in your NuMa data. Turn it on or off in **Settings → Keyboard Shortcuts**; the setting is stored in your browser (not synced across devices) and takes effect immediately, with no page reload needed.

Most detail pages (a food, a recipe, a meal) show a collapsible outline down the side — click a heading there to jump straight to that section. Forms that have unsaved changes mark their Save button so you can tell at a glance whether you've edited something, and the browser will warn you before you navigate away from an unsaved form. On the pages with a substantial edit form — Edit Recipe, a meal, Edit Custom Profile, Annotate a Food — NuMa goes further, with the "Data-entered safety" note at the top of each: click a link elsewhere in NuMa with unsaved edits and NuMa offers to save them for you first, or to leave without saving, or to stay and keep editing. On Edit Custom Profile, Edit Recipe and a meal page, running a search (or re-sorting its results) while you have unsaved edits saves them for you first, and a note at the top of the results offers to undo that save. (Closing or refreshing the browser tab is the one case NuMa can't step into — only your browser's own "leave this page?" warning appears there, so save first if you're closing the tab.)

#### Search boxes remember your last search {: #search-memory}

*Search terms: search history, previous search, restore search.*

On a meal's "Add Food or Recipe" search, a recipe's "Add Ingredient" search, and the Foods: Search page, if you follow a link away to look something up elsewhere and then come straight back to that exact page, your last search and its results are restored automatically — you don't have to retype it. This only applies to a plain link back to the page (the browser's own Back button already preserves it); it's scoped per page, so it never leaks a search from one meal into another.

**Adding from the results keeps them.**{: #search-keeps-results} When you add a result to a meal, a recipe or your pantry, the same search results stay on screen, with a green **Added …** line naming what you just added, so you can go straight on and add another from the same list. They change only when you run a new search, or click **Clear search**.

There's no time limit on this — it holds for as long as your browser tab stays open, not just for a moment after you step away. Clicking **Clear search** (shown next to the search box whenever a search is active) or closing the browser tab clears it back to the page's clean, empty-search state.

The main navigation bar goes further than any one page: clicking **Recipes**, **Meals & Log**, **Compare**, **Settings**, or **Manual** returns you to the exact page you were last on in that section — e.g. the specific recipe you were editing, or the exact set of items you had lined up on Compare — instead of always landing on its list/default page. That only happens when you arrive from a *different* section: click **Meals & Log** (or press `Alt+Shift+M`) while you're already working on a meal, and you go to the Meals & Log list itself. When that memory is what brought you back, the page's breadcrumb is highlighted, with a one-click "All recipes" / "All meals" link in case you actually wanted the plain list. **Foods** and **Analysis** are drop-downs of separate destinations (Search, Pantry, Daily summary, and more), so they work a little differently: a small "↩" quick-return link appears next to the drop-down whenever there's a page you've viewed in it, showing that page's name, so you can jump back to it in one click after wandering off elsewhere — the drop-down itself always opens normally. Following a breadcrumb link (e.g. **Recipes** at the top of a recipe page) back to the list always starts fresh, clearing any remembered search or position.

**Long pages also come back the way you left them.** On the Daily Summary, a meal, a recipe, and a food's own page, NuMa remembers how far down you had scrolled and which collapsible sections you had open, and puts both back when you return to that page. Like the search memory above, this lasts as long as the browser tab stays open. Two things are deliberately left out of it: inline **Edit** panels never reopen by themselves, since closing one is how you discard what you typed in it, and a link that points at a specific spot on a page (any link ending in `#something`) still takes you to that spot rather than to where you last were.

### C. Sample Workflows {: #sample-workflows-web}

*Search terms: walkthrough, examples, learn by doing.*

**Use this as a tutorial!** With NuMa open in your browser, work through these step by step, paying close attention to what appears on your screen. Each workflow is self-contained — you don't need to read Part 4 (nutrition concepts) or Part 5 (reference) first; terms are briefly explained in place.

**Workflows 1–3 are a single connected thread, not a tour of every menu.** They follow one feature end to end — protein complementarity — because it's NuMa's most distinctive capability. Right after them, a short "a few more things worth trying" section highlights a few other Foods and Recipes features these three don't touch, and Workflow 4 does the same connected-thread treatment for Meals & Log paired with Analysis.

---

#### Workflow 1 — Looking up a single food and finding its protein gaps

**What this shows:** how to search for a food, read its nutrient profile, and get automatic protein complement suggestions drawn from the built-in protein source list.

**Step 1 — Open the Foods menu.** Click **Foods** in the top navigation bar. A dropdown appears with nine numbered items.

**Step 2 — Search for a food.** Click **2. Analyze a food portion**. A search box appears. Type `brown rice cooked` and click **Search**. NuMa queries [USDA](#gloss-usda) FoodData Central and returns a ranked list of matches. Click the Foundation Foods entry — Foundation Foods have the most complete amino acid data.

**Step 3 — Choose a portion.** The food detail page opens. Near the top you will see a portion input field. Type `1 cup` (or select it from the named portions dropdown if it appears) and click **Recalculate nutrients**.

**Step 4 — Read the nutrient table.** The page now shows the full nutrient profile scaled to your chosen portion. Click the **Nutritional Analysis** section header to expand it — you will see macronutrients, minerals, vitamins, and amino acids.

**Step 5 — Read the protein quality section.** Click **Protein Quality** to expand it. NuMa shows a per-amino-acid score table. Brown rice is low in lysine — its lysine score will be well below 1.0 (the [FAO](#gloss-fao) reference floor). This is the [limiting amino acid](#gloss-limiting-amino-acid).

**Step 6 — Read the complement suggestions.** Click **Protein Complement Suggestions** to expand it. Because a gap exists, NuMa lists the amino acid(s) you're short on under **Gaps**, then shows foods that can close them under a **Suggestions** heading (or **Other options** if pantry items also qualified — see Step 5 of Workflow 2). Suggestions are ranked by smallest amount needed. You might see, for example, that adding 45 g of lentils would close the lysine gap and bring the combined protein to a complete profile.

**What you learned:** NuMa can tell you BOTH what is in a food AND what is missing — and exactly what to add to fix it.

---

#### Workflow 2 — Analyzing a meal with pantry items as complement candidates

*Search terms: tutorial, complements.*

**What this shows:** how recording your own protein sources in the Pantry makes complement suggestions personal and practical, drawing on foods you actually have.

**Before you start, set up your profile.** Click **Settings**, fill in your age, sex, weight, height, and activity level, and save. This is what lets NuMa compare your protein intake against a target built for you, rather than a generic default — you'll see it reflected in the % goal figures later in this workflow and in Workflow 4.

**Step 1 — Add a food to your Pantry.** Click **Foods** in the navigation bar, then click **6. My Pantry**. On the Pantry page, type `hemp seeds` into the search box under "Add a pantry item — search for full amino acid data" and click **Search**. A results table appears — click **Add to pantry** next to the best match. (The **Can't find it? Save just the name for now** link just under the search box skips the search and saves just the name, with no nutrient data — use it only when you can't find a match.)

**Step 2 — Create a meal.** Click **Meals & Log** in the navigation bar. Click **New Meal**, give it a name (e.g., "Lunch today"), and a date. The meal page opens with a search box. Type `brown rice cooked`, click **Search**, then click the matching food and enter `1 cup` as the portion. Repeat with `black beans cooked` at `½ cup`. Both foods now appear in the meal's item list.

**Step 3 — View the meal's nutrition analysis.** Scroll down on the meal page. The **Nutritional Analysis**, **Meal-Level Protein Analysis**, and **Protein Complement Suggestions** sections are collapsed by default — click each header to expand it. NuMa aggregates the nutrients across both foods and shows a combined profile.

**Step 4 — Read the protein analysis section.** Rice and beans together improve each other's amino acid profile significantly — this is protein complementarity in action. The combined score will be higher than either food alone.

**Step 5 — Read the complement suggestions.** Because you now have a pantry item, the suggestions are organized into two headings: **From your pantry & recipes** (hemp seeds will appear here if it qualifies as a gap-closer for this meal) and **Other options** (the same built-in list from Workflow 1). Suggestions drawn from your pantry reflect a food you actually have, not just a theoretical option.

**What you learned:** Building even a small pantry of protein sources you keep on hand transforms complement suggestions from generic advice into a practical shopping and cooking guide.

---

#### Workflow 3 — Using an analyzed recipe as a complement candidate

*Search terms: tutorial, recipe as complement.*

**What this shows:** how recipes you have analyzed become available as complement options for other foods and meals, so NuMa can suggest "add 250 g of your lentil soup" rather than just "add lentils."

**Step 1 — Create and analyze a recipe.** Click **Recipes** in the navigation bar, then click **New recipe**. Give it a name such as "Lentil soup" and fill in the servings count. On the recipe edit page, add ingredients one at a time — for example, lentils (200 g), onion (80 g), garlic (10 g), and vegetable broth (500 g). Save the recipe details, then add each ingredient via the ingredient search box. The recipe detail page shows its Nutritional Analysis and [Complete Protein](#gloss-complete-protein) Analysis, computed automatically. Expand those sections to see the full protein profile and [DCP](#gloss-dcp).

**Step 2 — Look up a food with protein gaps.** Click **Foods** in the navigation bar, then click **2. Analyze a food portion**. Search for `corn tortilla`. Click the result, then enter `46 g` (about 2 tortillas) in the portion field and click **Recalculate nutrients**. Expand **Protein Quality** — corn is low in lysine and tryptophan.

**Step 3 — Read the complement suggestions.** Expand **Protein Complement Suggestions**. Under **From your pantry & recipes**, your lentil soup recipe appears as a candidate, tagged with its recipe [code](#gloss-code) (R followed by a number) next to its name so you can tell it apart from a plain food. NuMa shows how many grams of the recipe would close the gaps in the corn tortillas — for example, "Serve alongside: 180 g."

**Step 4 — Note what changes as you build up data.** The more recipes you analyze and the more pantry items you add, the more the complement suggestions reflect your actual kitchen — each qualifying recipe or pantry item appears as its own candidate card under **From your pantry & recipes**.

**What you learned:** NuMa's suggestions become progressively more useful as you add your own data. The built-in list ensures you always get suggestions even on day one; your pantry and recipes make those suggestions yours.

---

#### A few more things worth trying

*Search terms: more features, what else, what-if, tips.*

Workflows 1–3 follow one thread — protein complementarity — since it's NuMa's most distinctive feature. A few other things worth a look, once you've got the basics down:

**Compare** (in the navigation bar). Add up to eight foods and recipes side by side in one table (checkboxes in the search results, an amount for each) — a quick way to answer "which of these is actually better for me" instead of flipping between separate detail pages. A comparison can be saved under a name and reopened later.

**Foods → Custom food profiles.** Enter a homemade dish, a supplement, or a product NuMa's [databases](#gloss-database) don't have (or have incompletely) — either from scratch, or by copying an existing cached food as a starting draft and editing its nutrients from there.

**Recipes: use one recipe inside another.** A recipe can be added as an ingredient of another recipe — a lentil sauce used inside three different dinners, say. Editing and saving the base recipe keeps every recipe built on it up to date automatically — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 6.

**Recipes → Archive/Restore.** Hide a recipe (or a food, or a pantry entry) you're not using right now without deleting it — see [Archiving](#archive) in Part 5.

---

#### Workflow 4 — Logging several days, then spotting a pattern in Analysis

*Search terms: tutorial, logging days, trends, patterns.*

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

*Search terms: food search, find a food, look up food.*

Type any part of a food name, an [FDC ID](#gloss-fdc-id) number, a 12/13-digit barcode ([UPC](#gloss-upc)-A or [EAN](#gloss-ean)-13), or a food's or recipe's [code](#search-by-code) — see [Your own data is always checked first](#search-ranking) in Part 6 for how results are sourced and ordered. Next to the search box, a row of Source checkboxes (Pantry, Food Cache, Recipes, [USDA](#gloss-usda), Open Food Facts, the Canadian Nutrient File, and the UK, Australian and French tables) lets you narrow results to any combination of sources before or after you search — see [Source filter](#food-search) in Part 5 for details. Click a result to open its full [Nutritional Analysis](#nutrients), [Protein Quality](#protein-quality), and complement-suggestion page.

#### Analyze a food portion / Analyze a saved recipe portion

*Search terms: portion analysis, analyze an amount, how much protein in.*

Shortcuts into Search that take you straight to entering an amount once you've picked a food or recipe, rather than seeing the per-100g view first.

#### Convert

*Search terms: unit conversion, convert units, grams to cups, ounces to grams, measurement conversion.*

A pure unit-conversion tool — search for a food (with the same [Source filter](#food-search) as every other search box), then type any amount (`3 oz`, `1/4 cup`, `150 g`) to see its gram/mL equivalent and the closest named portion size. No nutrient analysis is shown here; use Search for that.

#### Compare

*Search terms: compare foods, comparison, which is better.*

**Compare** has its own place in the navigation bar, rather than in the Foods menu. Add up to eight foods and/or recipes (checkboxes in the search results, filterable by [Source](#food-search) the same as any other search) and set an amount for each to see them side by side in one nutrient table. Comparisons can be saved under a name and reopened later, renamed, or deleted.

#### Food Cache {: #food-cache-web}

*Search terms: cached foods, saved foods, food list, stored foods, my foods.*

Every food NuMa has ever fetched from [USDA](#gloss-usda) or Open Food Facts[^3] lives here — see the [Food Cache column guide](#cached) in Part 5 for what each column means. A **Sort by** dropdown orders the list by Name, Code, Type, [DIAAS](#gloss-diaas), or [GI](#gloss-gi) estimate. A misspelled filter offers a ["Did you mean"](#search-suggestions) correction, same as any other search box. The box at the top has two buttons: **Filter this list** narrows the foods already in your cache, and **Search online** opens [Foods → Search](#food-search) with the same words, to look in USDA, Open Food Facts and the other sources. After filtering, a **Not here? Search online** link next to the count does the same. Per-food actions: **Add to pantry** (adds the food to your [Pantry](#pantry) and returns you to the same row; a food already there shows **In pantry** instead, which opens the Pantry), **Portions** (add or edit named portion sizes), **Refresh** (fetch USDA's current copy of the food and [choose which changed values to take](#review-incoming)), **Archive/Restore** ([hide without deleting](#archive)), and **Delete** — refused if a pantry entry, recipe, or meal still uses that food, since deleting it anyway would leave that entry pointing at nothing; the refusal names and links every blocking pantry entry, recipe, and meal by id (e.g. "pantry: 34 | recipe: 12 | meal: 9, 72") so you can go straight to the place to remove or replace it, or use Archive instead. **Prune unused foods** removes cache entries no pantry entry, recipe, or meal is currently using — with a checkbox per food (checked by default) so you can uncheck anything you'd rather keep before pruning. Each row also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) above — for jumping straight into [Comparison](#comparison) with the checked items.

**Check [database](#gloss-database) integrity.**{: #db-check} *(This page — Foods → 9 — runs several checks: broken references, below; [missing nutrient data](#data-completeness); [food data problems](#calorie-checks); [amounts that no longer match](#stale-amounts); [amounts converted with a generic density](#generic-density); foods you use with no amino acid data or no portion weights; [duplicate foods](#duplicate-foods); and [old USDA copies](#old-copies). [Checking your data](#checking-your-data) lists every data check NuMa makes.)* The first scans for pantry entries, recipe ingredients, or logged meal items that still point at a food or recipe no longer in the cache — leftover from before Delete started refusing to remove still-used foods, or from a manually edited [database](#gloss-database) file. Opening a food page for one of these fails, since NuMa treats the missing food as never-cached and tries to re-fetch it from USDA by [ID](#gloss-id) — which errors outright for an Open Food Facts food (its ID isn't a real USDA ID) and can return the wrong food for a reused-looking one. The check page lists every problem found, grouped into up to five kinds, **each with its own fix button and a plain-language note on what that fix actually does** — they're kept separate because the consequences are not equivalent:

- **Pantry entries** — low impact; removing one only takes it off your pantry list.
- **Recipe ingredients** — removing one deletes that ingredient line from its recipe; the recipe's nutrient totals recalculate without it.
- **Logged meal items** — removing one deletes that food/recipe from a day's logged meal history; that day's totals recalculate without it, same as if it had never been logged.
- **Sub-recipe references** — non-destructive; nothing is deleted, the ingredient is just flagged "recipe (deleted)" (the same label used everywhere else a referenced recipe is gone) instead of erroring.
- **Unreadable nutrient/portion data** — never auto-repaired; each food gets its own **Refresh** (re-fetch from USDA) and **Delete** buttons so you decide.

**Check for missing nutrient data.**{: #data-completeness} The same page (Foods → 9) has a section, **Missing nutrient data**, listing every cached food that has *no* values at all for one of six nutrient groups — the five blocks of a Nutritional Analysis table (Macronutrients, Omega Fatty Acids, Minerals, Vitamins, Phytonutrients) plus Amino Acids. Macronutrients count as missing if even one of calories, protein, carbohydrate, or fat is absent; amino acids only for a food that has protein. A group with *some* values is normal for real data and isn't listed.

Not every gap matters. Basil doesn't need macronutrients — too little goes into a recipe to count. For a gap like that, check **not needed** under it and click **Save "not needed" and "has none" choices**: NuMa stops listing it for that food, stops warning about it on the food's own page, and leaves it out of any Claude AI prompt (which tells Claude it's not needed). To mark a whole group at once, click **Mark column not needed** under that column's heading (click it again — it then reads **Unmark column** — to clear them), then save. **Refresh list** checks every food again and redraws the list, picking up anything you've filled in elsewhere since the page loaded; it asks first if you have "not needed" changes you haven't saved. To undo one, tick **Also list foods whose only gaps are marked "not needed"**, uncheck the box, and save again — or, quicker, open that food's own page, where each group marked not needed has its own **(undo)** link. **Groups to check** narrows the list to the groups you care about. Omega Fatty Acids and Phytonutrients start out unchecked: most ordinary food records were never measured for them, so checking them lists nearly every food. Tick them if you want them anyway. NuMa remembers both settings.

**When a food has none.**{: #data-completeness-has-none} Some gaps aren't missing data at all: meat has no phytonutrients, a vitamin pill has no macronutrients, sugar has no omega fats. For a gap like that, check **has none (0)** under it instead and save. NuMa asks you to confirm, then records 0 for each of that group's missing values in that food, leaving any values it already has alone, and updates the meals and recipes using it. The food then counts, as 0, everywhere, rather than just being skipped. **Mark column has none** under a column's heading ticks the box for every food in that column, for when a whole column is foods you know have none. Amino acids have no "has none" box: every food in that column has protein, so it has amino acids. Use **has none** only when you know. A food that does contain some is better left **not needed**, which keeps it blank and honest. To change a recorded 0 later, edit the food's values. To deal with one nutrient rather than a whole group, use the list of foods with no data under [Top Contributors](#contrib-no-data-answers).

To fill real gaps, check **ask AI** under each gap you want help with — one food, a few, or a whole group at once with the **all** link under that column's heading — and click **Build a Claude AI prompt for the gaps checked "ask AI"**. The prompt covers only the gaps you checked. See [Fetching missing data with Claude AI](#fetch) below. A food's own page offers the same thing: if it's missing core macronutrients you'll see a warning with **Ask Claude AI for the missing data** and **Macronutrients not needed for this food** buttons, and any other missing group is named in a short line under it.

**Calorie checks.**{: #calorie-checks} Calories are the one figure NuMa can check against the rest of a food's data: protein and carbohydrate supply about 4 kcal per gram and fat about 9, so a food's protein, carbs and fat imply roughly what its calories should be. NuMa uses that in two ways.

- **Missing calories are filled in.** When a food arrives — from USDA, Open Food Facts, a [CSV](#gloss-csv) file, Claude AI, or typed in by you — with protein, carbs and fat but no calories, NuMa works the calories out from those three and marks the figure as an *estimate*. If the food's source later supplies a real figure (a Refresh from USDA, say), that replaces it. If you change the food's protein, carbs or fat, the estimate follows. A food missing even one of the three can't be estimated; it stays missing. The same happens whenever a food that was missing one of the three gets it later, so filling in a missing fat figure (from another food, Claude AI, **Has none — record 0**, or an edit) also fills in its calories.
- **Calories that don't add up are flagged.** A stored figure far from what the food's own protein, carbs and fat imply (more than about a quarter off) is flagged, never changed. Sometimes the gap is real: alcohol, sugar alcohols and very high fiber all carry energy that the 4-4-9 rule doesn't model. Otherwise it usually means the food's data is wrong. When you know a food's calories are right, the **These calories are right — stop flagging them** button on its page, or beside it in Foods → 9's **Food data problems** list, turns this check off for that food (**Check them again**, on its page, turns it back on).

**Turning the calorie check off for a food.**{: #calorie-check-off} For some foods calories don't matter — a vitamin or mineral supplement, a herb or spice used by the pinch. To stop NuMa listing such a food in a **Calories** note, open the food's page (click its name in the note) and use whichever button it shows:

- **Macronutrients not needed for this food — stop flagging**, if the food has *no* calorie value (or no protein, carbs or fat). NuMa then stops checking that food's calories altogether, and it no longer counts toward the "no calorie value" warning on any meal, recipe or day. This is the one for supplements.
- **These calories are right — stop flagging them**, if the food has calories that NuMa calls doubtful but you know are correct.

Each has an undo on the same page: an **(undo)** link beside a group marked not needed, or **Check them again**. A food whose calories are only *estimated* needs nothing turned off — that line is information, not a warning.

The same page (Foods → 9) has a section, **Food data problems**, listing every food in either situation (along with any food holding an [impossible value](#data-checks-list)), plus every food whose calories are estimated, for information. Foods whose macronutrients you've marked "not needed" (a supplement, a spice) aren't checked for calories. A meal, recipe or daily summary that includes such a food shows a short **Calories** note above its Nutritional Analysis table: it leads with how much of the calorie total comes from measured values, then names each food, so you know when the total is approximate or too low. See [Checking your data](#checking-your-data) for every other check. To fix a food, open it and use **Refresh from USDA** (for a USDA food), **Fill in nutrients from another food**, or edit its values directly.

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

Under each food's name are the ways to fix it by hand: **Refresh from USDA** (USDA foods), **Fill in from another food** (already searching for this food's name), and **Edit values** (your own custom foods only).

**Every fix is recorded.** The food's page then lists it under **Corrected on Foods → 9**: which value, from what, to what, why, and when. On a USDA or other outside food a corrected value counts as yours, so a later **Refresh from USDA** shows the source's figure beside it, unticked, marked as your correction, rather than quietly putting the old figure back. Every recipe and meal using the food is recalculated straight away.

**Fetching missing data with Claude [AI](#gloss-ai).**{: #fetch} Some foods — especially branded or prepared items — arrive without amino acid data, and a few arrive missing even calories or protein. Check the boxes next to the foods you want (or click "Select all missing [AA](#gloss-aa) data" to grab every food currently missing it), then click **Fetch missing data from Claude AI**. (You can also start from the [missing nutrient data check](#data-completeness), or from the warning on a food's own page.) This builds a ready-to-send prompt and shows it on its own page with a **Copy prompt to clipboard** button.

The prompt asks only for what each food is missing — the specific values, food by food — and says nothing about groups you've marked "not needed" except that they're not needed. A food with nothing missing is left out (the page tells you which).

**Asking for GI and DIAAS too.**{: #fetch-gi-diaas} Tick **Also ask for each food's glycemic index (GI) and DIAAS** at the top of the prompt page and the prompt is rebuilt to ask for those as well, for each food that doesn't already have them (a food whose Annotate page is set to stop asking is skipped). A food with no missing nutrients is then included if it still lacks GI or DIAAS. Importing the reply saves them to the food's [annotation](#annotate), just as if you'd typed them on **Foods → Annotate**, with Claude's cited source kept beside the GI. Like the nutrients, they only fill blanks unless you tick **Also replace the values these foods already have**.

From there:

1. Go to [claude.ai](https://claude.ai) — open a **new chat** (not an existing one) — paste the prompt, and send.
2. **Check the reply for gaps.** Claude's first answer often sticks to USDA data and leaves out anything USDA doesn't have. If many values are missing, or Claude says they're unknown, ask it in the same chat: *"Please do a literature review for the missing values and give me all the food blocks again, complete and in the same format."* That usually turns up more, from published studies and other countries' food tables. (The prompt asks for this already, but Claude doesn't always do it the first time.)
3. Copy Claude's latest complete reply with the **Copy** button under it, rather than by selecting the text (all of it, including every fenced `json` block — if Claude splits its answer across multiple messages, copy each one and paste them together). If you did select the text instead, NuMa will usually still find the data and say so; nothing else to do.
4. Back in NuMa, click **Import Claude response** (also reachable directly from the Food Cache page), paste the reply into the box, and click **Review**.
5. NuMa shows you a table of what it understood from the reply — name, [FDC](#gloss-fdc) ID, calories, protein, how many of the 11 tracked amino acids were found, and what importing will do — plus any warnings about data it couldn't use. Check it over, then click **Import** to save it to your cache.

**Importing only fills gaps.** For a food already in your cache, importing adds the values it was missing and nothing else — every value it already has stays, and so do its name, portions, and notes. If Claude's reply includes a different value for something the food already has, the review table names it, and a checkbox, **Also replace the values these foods already have**, lets you take Claude's value instead. Leave it unchecked unless you mean it.

#### My Pantry

*Search terms: foods on hand, staples, groceries.*

Foods you keep on hand — see [My Pantry](#pantry) in Part 5 for the column guide. Pantry foods are checked first for complement suggestions and search results. Add a food with full nutrient data via search (with the same [Source filter](#food-search) as every other search box), or use **Can't find it? Save just the name for now** for something you haven't looked up yet (link it to real data later with **Link a food**). Only the search-and-select route caches the food — see [Only a search-and-select adds a food to your Food Cache](#pantry) in Part 5. Searching for a food already in your pantry shows a **Remove from pantry** button right on its search-results row, so you don't need to scroll down to find the matching row in the pantry list to take it out. Each pantry item with a linked food also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) above — for jumping straight into [Comparison](#comparison) with the checked items; a quick-add item with no linked data can't be compared. Search results have Compare checkboxes too, with their own button, so you can compare foods before deciding which to add. Matches from your pantry and Food Cache appear at once; results from the online sources fill in a few seconds later (a red **Online search in progress…** note shows until they do), as on [Foods → Search](#food-search). The search box at the top looks for *new* foods to add. To narrow the pantry list you already have, use **Filter my pantry list** just above it: it keeps only the items whose name or notes contain every word you type.

#### Custom food profiles

*Search terms: homemade food, own food, create food, label data.*

Create a food NuMa doesn't already have — a homemade dish, a supplement, or a product with an incomplete [database](#gloss-database) entry. Either start from scratch, or **copy a cached food as a draft** and edit its nutrients from there — both of the page's "copy from another food" searches have the same [Source filter](#food-search) too, and can now reach Open Food Facts as well as your cache and [USDA](#gloss-usda). A misspelled "copy a cached food as a draft" search also offers a ["Did you mean"](#search-suggestions) correction. See [Entering custom foods and dietary supplements](#custom-foods) below.

#### Annotate

*Search terms: GI estimate, DIAAS estimate, annotation, food notes.*

A list of cached foods where you can enter a glycemic index estimate, a [DIAAS](#gloss-diaas) estimate, prep-context notes, or check "don't ask again" for a specific nutrient. NuMa also opens this automatically as a follow-up prompt right after certain actions when data is missing — you can skip it for now or skip it permanently for that food. The filter box offers a ["Did you mean"](#search-suggestions) correction on a misspelled name, same as any other search box.

### E. Opening a food's detail page

*Search terms: food page, food details, nutrition facts, food analysis.*

A food's page shows, in order: its **Notes**{: #food-notes} (only if it has any: the notes saved with the food, such as where its figures came from, and the prep context you gave it on the Annotate page; they're also an option on its printout), a line with its [GI](#gloss-gi) (if you've recorded one) and [glycemic load](#glycemic) per 100 g and for the amount you're analyzing, **Protein Summary** ([DCP](#gloss-dcp)), **Nutritional Analysis** (type any amount, or pick a named portion, then click **Recalculate**), **Protein Quality** ([DIAAS](#diaas) and the per-amino-acid table), **Anti-nutrients**, **Complement Suggestions** (pantry foods first, then general suggestions, then two-food pairs and combos — each can be [ignored and recalculated](#ignore-complement)), and an **Add to Pantry** form at the bottom. If the food has no amino acid data, you'll see a suggestion to search for a Foundation or [SR](#gloss-sr) Legacy equivalent instead — those datasets are the ones most likely to have complete amino acid profiles.

**Renaming a food.**{: #rename-food} Every food's page, a [USDA](#gloss-usda) food's included, has **Rename this food** just under its name. Type the new name and click **Save the new name**. Only the name changes, but it changes everywhere: every recipe, meal and pantry line using the food shows the new name. A USDA food stays linked to USDA, so **Refresh from USDA** still works; when it does, it shows USDA's own name beside yours, unticked and marked as yours, rather than putting it back. Tick it there if you do want USDA's name again.

Right below the title, every food's page also has a **Copy as custom-food draft** button — no detour through Food Search or Custom Food Profiles needed to start editing a copy of what you're already looking at. See [Entering custom foods and dietary supplements](#custom-foods) for what to do with the copy.

### F. Using the Recipes menu {: #recipes-menu-web}

*Search terms: recipe list, edit recipe, copy recipe, archive recipe.*

The **Recipes** page lists every recipe, with filter/sort options and a **Show archived recipes** / **Hide archived recipes** button. A misspelled filter offers a ["Did you mean"](#search-suggestions) correction, same as any other search box. Row actions: **Edit**, **Copy**, **Archive/Restore**, **Delete**. **Recompute [DCP](#gloss-dcp) for all recipes** refreshes every recipe's protein score at once, and **Broken recipe references** finds any recipe whose sub-recipe ingredient was since deleted — see [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) in Part 6. Each row also has a **Compare** checkbox — see [Compare selected](#compare-checkboxes) in Part 5 — for jumping straight into [Comparison](#comparison) with the checked recipes.

Editing a recipe's ingredients or servings recalculates its own [DCP](#gloss-dcp) automatically, and cascades to every recipe that depends on it too — see [Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it](#recipe-dcp-cascade) in Part 6. You don't need **Recompute DCP for all recipes** just because you changed one recipe; it's there for after a bulk import, or if you suspect stale numbers from before this cascading recalculation existed.

- **New recipe** — a short form (name, description, servings, total yield) that drops you straight into editing.
- **Edit** — a details form plus an ingredients table, with a single **Save recipe details** button (on the "Recipe details" heading row) that saves every field in that form at once. The details form includes an **Introduction** field for background — where the recipe came from, why you like it, serving notes — anything that isn't the step-by-step instructions — and, below Instructions, a **Notes and documentation** field for anything you want on record: sources you consulted, substitutions you have tried, changes to make next time. Notes print at the very bottom of the recipe's nutritional analysis, go into the recipe [CSV](#gloss-csv) export, and are included in the [AI](#gloss-ai) translation. Add an ingredient by searching — the results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns and the "Fetch full details for selected" [AA](#gloss-aa)-confirmation button — then typing a portion (`150 g`, `1/2 cup`, or a saved preset like `p1`) — NuMa saves it as grams at that moment, so later changes to the food's portions don't alter it (see [Editing or changing a food](#food-edit-consequences)); reorder ingredients with the up/down controls, or edit or remove one inline. A **Running totals** card at the side updates live as you add ingredients, showing calories, protein, and DCP for the whole recipe and per serving.
- **Detail** — mirrors a food's detail page (Introduction right after the title, Protein Summary, Ingredients, Instructions, Nutritional Analysis, [Complete Protein Analysis](#meal-diaas) with per-ingredient digestibility, Missing AA Profiles, Complement Suggestions — [ignorable and recalculable](#ignore-complement) here too, [Glycemic Load](#glycemic), Anti-nutrients), plus a servings field to re-analyze at a different batch size. **Print/save recipe** opens a stripped-down, print-friendly version in a new tab, with Introduction included as one of the "Include on this printout" checkboxes. Above those checkboxes, a **Print layout** choice (Full sheet or Half sheet — Half sheet shrinks the title and tightens line spacing throughout, including the Ingredients list) and a **Paper size** choice (US Letter or A4, which sets the exact page dimensions your browser's Print/Save-as-[PDF](#gloss-pdf) preview paginates against) are both remembered for next time. This printable page — and the same layout/paper choices — is also available from a food's, a meal's, and a day's own detail page, not just a recipe's.

### G. Using the Meals & Log menu

*Search terms: food log, food diary, logging meals, meal list, journal.*

The **Meals & Log** page has a **New Meal** form at the top (name + date), filters for date and sort order, a **Search meal history** box, on its own line, that finds every meal that contains, or doesn't contain, a food or recipe, by name or [ID](#gloss-id) (a misspelled search there also offers a ["Did you mean"](#search-suggestions) correction), and a batch button to calculate DCP and calories for all meals, or just the last 10 or 30 days. The list itself shows each meal's completeness, item count, Meal DCP, Day DCP (combined across all meals on that date), % of your daily goal, and calories.

Open a meal to add foods or recipes (search box at top — for a recipe you can log the whole thing or just individual ingredients), edit or remove items inline (a food's amount is saved as grams the moment you enter it, so later changes to that food's portions don't alter it — see [Editing or changing a food](#food-edit-consequences)), mark the meal complete/incomplete, rename it or change its date, or merge it with other meals logged the same day. Below the item list: [Nutritional Analysis](#nutrients), [Meal-Level Protein Analysis](#meal-diaas) (with a **Refresh from [USDA](#gloss-usda)** button if amino acid data needs updating), Missing [AA](#gloss-aa) Profiles, Complement Suggestions ([ignorable and recalculable](#ignore-complement)), [Glycemic Load](#glycemic), and Anti-nutrients.

<span id="full-day"></span>If more than one meal is logged on the same date, **Analyze full day** rolls all of them into one combined analysis — total nutrients, pooled protein quality, and complement suggestions across everything you ate that day. It has the same sections as a meal's own page (Top Contributors, Missing Amino Acid Profiles, glycemic load, anti-nutrients and the rest), pooled over the whole day. It is also the page Daily Summary opens for that date: the two differ only in the breadcrumb at the top, which leads back the way you came.

### H. Using the Analysis menu {: #analysis-menu-web}

*Search terms: reports, trends.*

- **Daily summary** — a table of recent days with Day [DCP](#gloss-dcp) and % of goal; pick a date to see that day's full analysis (same sections as the full-day meal view). From here, follow the **Nutrient averages across days** link to see 7/14/30-day averages — useful for catching a chronic shortfall that a single good or bad day would hide.
- **Food use in meals** — see how often you've eaten a given food or recipe. Everything you actually ate is counted: foods logged on their own, recipes, the sub-recipes inside them, and foods you only eat inside recipes. Choose either a date range or a specific list of meal IDs, optionally limit results to protein-containing foods, and get a sortable table with a visual frequency bar.
- **Food use in recipes** — the same idea, but for your recipe book: see how many of your recipes use a given food or sub-recipe as an ingredient. This doesn't measure what you eat: a recipe you log in meals but never use inside another recipe won't appear. Choose all recipes, a date-created range, or a specific list of recipe IDs.

- **What-if: meals** — see how removing, adding, replacing or cutting down foods would change your daily nutrition over a set of days, before changing anything — see [What-if: Meals](#whatif).
- **What-if: recipes** — the same for recipes: change an ingredient and see each recipe's nutrition per serving, before and after — see [What-if: Recipes](#whatif-recipes).

Both Food Use pages have a **Substitute a food or recipe** panel for bulk-replacing one food or recipe with another across whatever's currently selected — see [Substituting a Food or Recipe](#fooduse-substitute).

### I. Using the Settings menu {: #settings}

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

Settings is organized into fifteen numbered, collapsible sections:

- **1. [Your Profile](#profile-setup)** — age, sex, weight, height, activity level (this drives all your daily nutrient targets), plus a checkbox enabling [oxalate](#oxalate) lookup, your [glucose tolerance](#gi-impaired) (the [GI](#gloss-gi) lookup default, and which advice [GI](#gloss-gi) notes give you), and an optional [daily glycemic load target](#gl-target).
- **2. Computed Daily Targets** — see [Part 6](#daily-nutrient-targets).
- **3. Dietary Preferences** — affects complement suggestions, [B12/iron/zinc guidance](#diet-bioavailability), and (see [Dietary Preferences](#diet)) every search and lookup in the program.
- **4. Protein Digestibility Overrides** — custom digestibility numbers for specific foods.
- **5. Nutrient Targets - Researched** — optional per-nutrient [Revised Optimal (Recent Research)](#optimal) targets and [Max limits](#maxlimits), with a one-click button to load recommended defaults.
- **6. [USDA](#gloss-usda) [API](#gloss-api) Key** — lets you use your own free personal code from USDA's website instead of the one NuMa shares with every user by default, so your searches are less likely to get temporarily blocked when many people are using NuMa at once (see [Food data](#food-data) for how to get one); also has the [search result depth](#search-ranking) setting.
- **7. Glycemic Index Reference Table** — which [GI](#gloss-gi) table lookups search, and building the 2021 one (see [Upgrading to the 2021 tables](#gi-editions)).
- **8. Glycemic Load** — show or hide every [glycemic load](#gl) figure: on food, meal, recipe and day pages (with the [estimated GI](#mixture-gi)), the day's [GL](#gloss-gl) so far under a meal's and a day's title, the [GL](#gloss-gl) columns and sort on Meals & Log and Recent Days, the [GL](#gloss-gl) trend and plot series, Compare, What-if, Top Contributors' [GL](#gloss-gl) ranking and swaps, printouts, and your daily [GL](#gloss-gl) target in Settings → 1. On unless you turn it off. [GI](#gloss-gi) values are still shown and kept, and nothing is deleted: turning it back on brings everything back, including a daily target you'd set. This is separate from **I do not record glycemic index data** in Settings → 7, which only stops NuMa asking you for GI values.
- **9. Water Tracking** — show or hide everything about [water](#water): the drinks / food split, the drink tick-boxes, the water fill-in and the check for a wet food picked in place of a dry one. On unless you turn it off; turning it off deletes nothing. From age 65, a day's page also warns when its drinks fall below the minimum that ESPEN (the European Society for Clinical Nutrition and Metabolism) recommends for older people.
- **10. [Meals & Log columns](#meal-columns)** — which nutrient columns your meal lists show.
- **11. [Starter Data](#starter-data)** — curated foods and recipes to explore or build on.
- **12. Keyboard Shortcuts** — see [Finding your way around](#web-shortcuts).
- **13. Browser to Launch** — see below.
- **14. Data Quality Reminder** — the Home page note about new data problems (see [Checking your data](#data-check-reminder)).
- **15. System Issues** — see [below](#system-issues-howto).

#### Your Profile {: #profile-setup}

*Search terms: personal details, body measurements.*

Age, sex, weight, height, and activity level. This is the one form that everything else in NuMa's nutrient-target system depends on: your [RDA](#rda) values (Part 4, Section P), the age/sex-adjusted [Daily Nutrient Goals](#goals) (Part 4, Section Q), and — where you've set them — your [Revised Optimal targets](#optimal) and [Maximum Nutrient Limits](#maxlimits) all key off the age, sex, weight, height, and activity level you enter here. Also on this form: a checkbox enabling [oxalate](#oxalate) lookup, off by default.

Leave this form empty and NuMa still works — you can search, log, and analyze foods and recipes — but every nutrient table's "% of daily target" column is blank, since there's no profile to calculate a target from. Fill it in whenever you're ready; every already-logged meal is re-evaluated against your new targets immediately, nothing needs to be re-entered.

#### Browser to Launch

*Search terms: default browser, which browser opens.*

Starting NuMa opens a browser tab automatically. If you have more than one browser running at the time (Firefox, Chrome, Chromium, Brave, Vivaldi, Opera, Edge, or GNOME Web), NuMa normally asks which one to use via a small dialog. Setting a **Browser to Launch** here skips that dialog and always uses the one you pick — leave it on "Ask each time" (the default) if you're fine being asked, or don't run more than one browser at once.

#### Starter Data {: #starter-data}

*Search terms: sample data, demo data, example recipes, preloaded.*

This is a small set of curated content: foods, and recipes made from them. The foods come from [USDA](#gloss-usda) and NuMa's other sources, and a few are custom foods; many carry full amino acid data, and a food may come with a glycemic index value already filled in (only ever one NuMa is permitted to share). Several of the recipes show protein complementing at work, pairing foods so that the amino acids each is short on are covered by the other. Many of the starter foods are there only because a starter recipe uses them: a recipe can't be loaded without its ingredients, which is why everyday items like salt, vanilla and cinnamon are in the set. **Settings → 11. Starter Data → View all starter data** shows, beside each food, which starter recipes use it. Their names all start with `* ` so you can always tell them apart from anything you've added yourself. A brand-new install loads this automatically the first time you launch it, so your Food Cache and Recipes aren't empty on day one — this section is for anyone who cleared it and wants it back, or an existing install that never had it. Clearing it is never permanent: **Load starter data** reappears here to put it all back, and **Restore individual starter items** brings back just the ones you pick. Your pantry starts empty: it's the list of foods *you* keep at home, so only you can fill it (see [Set up your pantry](#first-setup)).

Loading starter data never touches anything already in your cache, pantry, or recipes: a starter food you already have is simply skipped. It's tracked separately, so **Clear starter data** (which appears once it's loaded) removes only what was added, and nothing else. Loading again while it's already loaded does nothing.

**Clear keeps whatever you've made your own.** A starter food or recipe you've renamed (including taking the `*` off its name), edited, re-portioned, or given a glycemic index or [DIAAS](#gloss-diaas) value is yours from then on, and Clear leaves it alone. So does anything you're still using: a starter recipe you've logged in a meal or used inside one of your own recipes, and a starter food that a meal, one of your recipes, or your pantry still uses. After clearing, Settings says how many items were kept, and why.

**When a new version changes the starter set.** NuMa remembers which starter foods and recipes the version you ran before came with, so after an update it can tell you exactly what's different:

   - **New items** are marked **(new in this version)** in the **Restore individual starter items** list, which opens by itself when there are any, with a short description: a food's type, calories and protein per 100 g, and whether it has amino acid figures; a recipe's ingredients. Check the ones you want and click **Restore selected**. Something you deleted on purpose is never presented as new; only items the new version actually added are.
   - **Improved items** — starter foods or recipes you already have, which the new version has corrected or improved — are listed under **Improved in this version of NuMa**. Under each one, NuMa shows exactly what updating would change in *your* copy: for a food, each value side by side (yours now, the new version), with any value you edited yourself marked **your edit**, and portions that would be added or removed; for a recipe, changed servings, name, description or instructions, and ingredients added, removed or with a new amount. Check the ones you want and click **Update the checked items to the new version**. Updating replaces your copy with the new one, *including any changes you made to it yourself*, so leave unchecked anything you've edited and want to keep. Meals, recipes and pantry entries that use an updated item keep working, and their figures are recalculated. **Keep all my copies as they are** stops NuMa offering the improved versions.

These lists stay until you act on them, even after you dismiss the home-page message about them. If you skip a version, nothing is lost: the next version's lists include the skipped one's changes.

#### Computed Daily Targets

*Search terms: nutrient goals, my targets.*

This section of Settings shows your personalized nutrient targets. See [Your computed daily nutrient targets](#daily-nutrient-targets) in Part 6 for what it contains and how it's kept current.

#### System Issues {: #system-issues-howto}

*Search terms: stale scores, outdated DCP, recalculate, out of date, refresh totals.*

*One of NuMa's data checks — see [Checking your data](#checking-your-data) for the rest.*

Every recipe caches its protein-quality score (DCP) so it doesn't have to be recalculated every time you view it, and every meal saves its DCP, calories and nutrient totals for the list views. Whenever a food or recipe changes — editing a food's nutrients, bringing in amino acid data via "estimate it from a similar food," refreshing a food from [USDA](#gloss-usda), editing a recipe's ingredients — NuMa automatically recalculates DCP for every recipe that depends on the thing that changed, including recipes-of-recipes, all the way up the chain, and then every meal that logs any of them. You never have to trigger this yourself — see [Editing your data, and what changes as a result](#editing-consequences).

**System Issues is where NuMa tells you when that automatic recalculation itself broke.** This is not the same as a recipe showing "NC" (not computed) — NC just means DCP genuinely can't be calculated yet (a significant ingredient is missing amino acid data, or the recipe has 0 servings), which is an expected, normal state and isn't logged here at all. System Issues is specifically for the rarer case where the recalculation *should* have run and produced a real answer, but something went wrong internally (a software error) — the kind of failure that would otherwise silently vanish and leave a recipe's protein score stale with no indication anything was ever wrong.

**You can't miss one.** While a failure is outstanding, a red alert sits at the top of every page, Home included, linking here. Tick **Got it. Don't remind me again.** to hide it (you stay on the page you were on); it comes back only if another recalculation fails, and the failure itself stays listed here until it's fixed.

Each entry shows when it happened, which recipe or meal it affects, and the error itself. Click **Retry** to have NuMa recompute it again right now:

- If the retry succeeds, the entry clears — you'll see a confirmation, and the recipe's DCP is now current.
- If it fails again, the entry stays (with a fresh error message) and NuMa tells you so — Retry never just makes an entry disappear while the recipe underneath it is still broken. A repeat failure usually means a real bug that needs fixing in the code, not something you can resolve by clicking around; consider reporting it.

If you'd rather fix the underlying recipe yourself instead of using Retry, re-editing it (or opening it and saving again) triggers the same recalculation that Retry does, and clears the System Issues entry the next time it succeeds.

A one-time banner also appears on the home page whenever there's a System Issues entry you haven't seen yet, with a **Got it. Don't remind me again.** checkbox — checking it hides the banner (the entry still stays listed under Settings until it's actually resolved), and any *new* failure after that brings the banner back.

**The home page also checks GitHub for a newer NuMa release**, showing an **UPDATE AVAILABLE** banner with a link to what's new if one exists, and its own **Don't show this again for this version** checkbox — same idea as the System Issues checkbox just above. This check is quick (a couple of seconds at most) and fails silently if you're offline or GitHub is unreachable — it never blocks the home page from loading. See [What you see on the home page](#home-page-tour) for exactly where the current build's version stamp appears and how often the check itself runs.

**If you installed NuMa via the Linux installer, the banner also has an Update Now button** that downloads and installs the new version for you — no terminal, no manual download. Click it, confirm, and NuMa fetches the latest release and swaps itself in place; your data is completely untouched (it lives in a separate location the update never touches). You'll see a message telling you to close the browser tab and relaunch NuMa once it's done — the version you're currently running keeps working right up until you do. If you're running NuMa from source instead (a developer checkout), the button doesn't appear — you'll see the plain "what's new on GitHub" link instead, since there's no packaged install for it to replace.

### J. Entering custom foods and dietary supplements

Go to **Foods → Custom food profiles → Create**. See [Entering custom foods and dietary supplements](#custom-foods) in Part 6 for the fields, the supplement/tablet mechanism, and the barcode-first tip — they work identically here.

### K. A note on amino acid data {: #aa-note-web}

*Search terms: missing amino acids, AA data, refresh food, no amino acid data.*

New foods are cached automatically the first time they turn up in a search, comparison, or pantry lookup — no separate import step needed. If a food is still missing amino acid data, you'll see a **Refresh** button (Food Cache) or a **Refresh from [USDA](#gloss-usda)** link (a meal's Protein Analysis section) to fetch it — both only [fill in what's missing unless you choose otherwise](#review-incoming) — and wherever data is missing you'll usually see a suggestion to search for a Foundation or [SR](#gloss-sr) Legacy equivalent instead. You can also enter [GI](#gloss-gi) or [DIAAS](#gloss-diaas) estimates yourself via **Foods → Annotate**.

---

## Part 4 — Core nutrition concepts {: #coreNutrition}

*(Reading time: 1 hour, 59 minutes)*

### A. Essential Amino Acids {: #aa}

*Search terms: EAA, indispensable amino acids.*

Amino acids are the building blocks of protein. Nine of them are "essential", for our bodies cannot make them, so they must come from food every day[^60]:

> Histidine, Isoleucine, Leucine, Lysine, Methionine, Phenylalanine, Threonine, Tryptophan, Valine

Two others — Cystine and Tyrosine — can be made from Methionine and Phenylalanine respectively[^60]. Because of that, cystine in food spares some of the need for methionine, and tyrosine spares some of the need for phenylalanine. So the official scoring pattern judges each pair as one combined figure, and NuMa does the same: it evaluates [Met+Cys](#gloss-met-cys) and [Phe+Tyr](#gloss-phe-tyr) as combined pairs when scoring protein quality, following [FAO](#gloss-fao) 2013 guidelines[^16].

See [Protein Completeness](#complete) and [Amino Acid Gaps](#gap) for how completeness is scored and what a gap means.


### B. Protein Complement Suggestions {: #comp}

*Search terms: complements, protein combining, combine foods, pairing proteins, complementary proteins, protein pairing.*

When amino acid gaps are detected, NuMa suggests foods that can improve the protein quality of the base food or meal. Two separate tiers are shown, and they use different methods:

#### WHEN DOES NUMA SUGGEST PROTEIN COMPLEMENTS? {: #comp-threshold}

*Search terms: when complements appear, no suggestions shown.*

The composite [DIAAS](#gloss-diaas) for a meal is defined as the lowest of the nine individual amino acid ratios — the ratio for the [limiting amino acid](#gloss-limiting-amino-acid)[^16]. This means the meal [DIAAS](#gloss-diaas) and the complement-suggestion threshold are directly connected: if the meal [DIAAS](#gloss-diaas) is 0.95 or above, every single amino acid in the meal is also scoring 0.95 or above, and no suggestions will appear.

NuMa uses **0.95** as its threshold because gaps smaller than that are nutritionally trivial to close — the math works out to needing only a gram or two of additional food, which is not a practical suggestion worth presenting. A meal [DIAAS](#gloss-diaas) of 0.95–0.99 means the [limiting amino acid](#gloss-limiting-amino-acid) is present but slightly below the [FAO](#gloss-fao) ideal; the deficit is real but small, and the protein still falls within what the [FAO](#gloss-fao) calls a "good" quality protein source (a score of 0.75 to 0.99)[^16].

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

*Search terms: close a gap, fix amino acid shortfall, how much to add.*

These foods can mathematically close a specific amino acid gap with a practical amount (up to 300 g). A gap closer has a high enough ratio of the [limiting amino acid](#gloss-limiting-amino-acid) to protein that adding it to the base food brings that amino acid's score to 1.0 (the [FAO](#gloss-fao) reference floor).

To work out the amount, NuMa counts each food at its own digestibility: your meal at its own, and the added food at its own. A well-digested food like soy protein isolate therefore isn't undercounted when it's added to a less digestible meal. NuMa tries the gaps in order, most limiting first, and the amount shown is for the first gap that food can close. If a food can't close the main gap in a practical amount, but can close another one, the suggestion says which gap its amount is for.

**How much of a food NuMa will suggest.** Every suggestion stays within a most-per-meal amount for that food, so you're never told to add four cups of nutritional yeast. If you've saved your own limit for the food, that's what's used. Otherwise it's three of the food's label servings (two servings for a recipe). Failing that, it's a default for the kind of food: 15 g for seasonings and nutritional yeast, 40 g for protein powders and for seeds and nuts, 60 g for cheese, and 300 g for anything else. If closing the gap would take more than that, the suggestion shows the food at its limit, says how much full closure would take, and shows how far the limit gets you. A **Use the full amount this time** box lifts the limit for that page only. To set the limit for good, type it in the **Most I'd add to a meal** box under the suggestion and press **Save limit for this food**. Clear the box and save to go back to the default. The booster steps under DIAAS-Boosting Options stop at the same limit.

Each suggestion shows:
  - The food's or recipe's name, linked to its own page (it opens in a new tab, so the analysis stays as it was; a generic estimate from the built-in list has no page and isn't linked)
  - Grams to add
  - Which gaps it closes, with scores before and after
  - Digestible protein added
  - Total bioavailable [complete protein](#gloss-complete-protein) — the base food protein plus the complement protein, multiplied by the combined (pooled) [DIAAS](#gloss-diaas) of the pair. This is higher than just adding each food's individually-digestible protein, because the complement's amino acids improve the usability of the base food's protein too.
  - **% increase** — how much that total is up on your meal's (or day's, or recipe's) [DCP](#gloss-dcp) as it stands now; the line under the table names that starting figure. When a food is held to its per-meal limit, its last row says "per-meal limit" rather than "full".

#### RANKING

*Search terms: sort suggestions, best suggestion, order of suggestions.*

A **Sort by** dropdown above the list lets you pick how Tier 1 options are ranked:

  - **Greatest [DCP](#gloss-dcp) achieved** (the default) — the option that leaves the most total bioavailable complete protein after adding it, at the amount shown. The ranking uses exactly the figure each option displays as its total digestible complete protein. On a meal, day or recipe that figure is recalculated from every ingredient's own amino acids and digestibility. A note under the list says how it was worked out.
  - **Most digestible protein added** — the option contributing the most digestible protein on its own, regardless of how well it targets the limiting amino acid.
  - **Greatest effect on amino acid gap** — the option closing the most amino acid gaps, then (as a tiebreaker) improving the limiting amino acid's score the most.
  - **Smallest addition (in grams)** — the option needing the fewest grams.

In every mode, one refinement applies: an option that fully completes the amino acid profile is always moved to the front of its tier, regardless of how many grams it takes. (Tier 3 two-food combinations, described below, apply a similar promotion but only when the combined serving is 50 g or less — see that section.)

#### TIER 2 — DIAAS-BOOSTING OPTIONS

*Search terms: DIAAS booster, raise digestibility, improve protein quality.*

Sometimes the digestibility of the base food is low enough that no practical amount of any single food can "close the gap" mathematically. This happens when the food's raw amino acid ratios are already near the [FAO](#gloss-fao) reference — the gaps are digestibility-driven rather than composition-driven. Adding even a very good complement raises the pool's digestible amino acids but can't fully overcome the base food's own digestibility penalty via the gap-closer formula.

For those situations, [DIAAS](#gloss-diaas)-boosting options are shown instead. These foods raise the combined meal [DIAAS](#gloss-diaas) score toward 0.90 by contributing digestible amino acids that pool with the base food's amino acids. The calculation uses each food's own true [ileal digestibility](#gloss-ileal-digestibility) (not just the [DIAAS](#gloss-diaas) score), so a high-digestibility food like soy protein isolate (95%[^86]) contributes disproportionately more digestible amino acids than its raw content alone would suggest.

Each [DIAAS](#gloss-diaas)-boosting suggestion shows a progression of serving sizes — 15 g, 30 g, 60 g, and up to 120 g (roughly 1/2 cup) for meal, food, and daily-summary analyses. Each step shows the meal [DIAAS](#gloss-diaas) before and after adding that amount, so you can choose a realistic portion rather than being given a single impractically large target. Recipe analysis uses larger steps (up to 300 g) because recipe quantities serve multiple people.

#### TIER 3 — TWO-FOOD COMBINATIONS

*Search terms: two foods, pair of foods, second gap.*

When a single food can close the primary gap but in doing so dilutes another borderline amino acid, a two-food combination is offered. The logic follows a gap-cascade:

  Food A closes the primary (most-limiting) gap. It may open a smaller secondary gap by diluting a borderline amino acid that was already close to the threshold.

  Food B is chosen specifically to close whatever gap Food A left behind, without opening further gaps.

Together the pair clears all amino acid gaps. The output shows the individual gram amounts for each food, the cumulative amino acid effects, and whether the combination achieves "closes all gaps" status.

Three combinations are shown initially. The app offers to show more if available.

Combinations are ranked by total weight (lighter is ranked first). A combination that closes all gaps is promoted to the front, but only when its combined weight is 50 g or less — a combination needing 90 g to close everything won't outrank a 30 g combination that only partially closes the gaps, which prevents a barely-adequate pairing from dominating the list just because enough of it eventually fixes everything.

#### WHICH TIER IS RIGHT FOR YOU?

*Search terms: which suggestion, choose a suggestion, tiers compared.*

If single-food gap closers (Tier 1) are available, they are the most targeted choice: they fix a specific deficiency with a single food.

If single-food options open a secondary gap, Tier 3 two-food combinations show how to close everything in one practical step.

If only [DIAAS](#gloss-diaas)-boosting options are shown (Tier 2), the underlying problem is that the base food is not highly digestible. Adding a well-digested, amino-acid-rich food improves the overall protein quality of the meal even without closing any single gap definitively. This is nutritionally meaningful — a meal [DIAAS](#gloss-diaas) of 0.90 means 90% of the protein is both complete and digestible.

You do not need to eat [complement foods](#gloss-complement-food) at the same meal — meeting daily totals is sufficient for healthy adults[^14]<sup>,</sup>[^15]. See also [DIAAS](#diaas) and [limiting amino acid](#gap) for background.

#### RECIPE ANALYSIS: AMOUNTS ARE SIZED TO THE WHOLE BATCH {: #comp-recipe-scale}

*Search terms: recipe suggestions, amounts too large, scale suggestions.*

When you analyze a recipe (its own page, not a portion-analysis or meal/day view), every gram amount in this section — gap closers, [DIAAS](#gloss-diaas)-boosting steps, two-food combinations, two-step combinations — is calculated against the recipe's full total protein across **all of its servings**, not one serving. This is deliberate: the only way to act on a suggestion is to add an ingredient to the whole recipe batch, so the math solves for the whole batch's amino acid gap, not a single portion of it.

This is why a recipe suggestion can look large — for example, 80+ g of soy protein isolate to close a lysine gap in a 4-serving recipe. That is not a serving-size recommendation; it is how much to add to the pot so that every serving, once divided out, ends up amino-acid-complete. Each recipe suggestion also shows the per-serving equivalent alongside the whole-batch amount, so you can see what one serving actually gets.

Data sources, checked in this order: your [pantry](#pantry) (Foods → [My Pantry](#gloss-my-pantry)) and any [recipes you have analyzed](#recipes-menu-web); then your broader food cache (any food you've ever looked up, matched by name against the built-in reference list below); then that built-in list itself[^10], filtered by your dietary preferences (see [dietary preferences](#diet)). The suggestion header tells you exactly which sources were considered for that run. See [amino acid estimates in suggestions](#comp-estimate) for what it means when a suggestion is tagged "(estimated)" or "(generic estimate)".

Don't want a particular suggestion? See [ignoring a complement suggestion](#ignore-complement) in Part 6.


### C. Amino acid estimates in complement suggestions {: #comp-estimate}

*Search terms: estimated amino acids, estimated tag.*

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

*Search terms: complete protein, incomplete protein, all essential amino acids, plant protein quality.*

A protein is "complete" when it supplies all nine essential amino acids at or above the [FAO](#gloss-fao) 2013 reference amounts, adjusted for digestibility[^16]. Essential amino acids cannot be made by the body — they must come from food.

Most animal proteins are complete. Most plant proteins are not, but combining plant foods across a day can produce a complete profile — see [Protein Complement Suggestions](#comp).

The score shown in completeness tables is the ratio of each amino acid to the [FAO](#gloss-fao) reference level. A score of **1.0 or above** for all nine means the protein is complete. The most-[limiting amino acid](#gloss-limiting-amino-acid) (the one with the lowest score) is identified as the bottleneck.


### F. Digestible Complete Protein (DCP) {: #dcp}

*Search terms: effective protein, protein quality, bioavailable protein, digestible protein.*

[DCP](#gloss-dcp) — digestible [complete protein](#gloss-complete-protein) — is the grams of protein in a food or meal that are both digestible (absorbed by the body) and complete (supply all essential amino acids at or above reference levels).

It is more meaningful than raw grams of protein because it accounts for:

- **Digestibility:** how much protein is actually absorbed (from [DIAAS](#gloss-diaas))
- **Completeness:** whether the amino acid profile meets all requirements

A food with 30 g of protein but a [DIAAS](#gloss-diaas) of 0.70 and several amino acid gaps contributes less usable protein than those numbers suggest. [DCP](#gloss-dcp) captures that.

[DCP](#gloss-dcp) is also called "bioavailable complete protein" or "usable protein" in nutrition literature — these terms mean the same thing. NuMa uses [DCP](#gloss-dcp) throughout.

NuMa shows [DCP](#gloss-dcp) in the bioavailability section of food and recipe analysis. See also [DIAAS](#diaas) and [Protein Completeness](#complete).

#### Protein per meal {: #protein-per-meal}
<span id="protein-distribution"></span><span id="protein-per-meal-amount"></span>
*Search terms: protein per meal, protein distribution, how much protein in one meal, leucine threshold, muscle protein synthesis, older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

For **when** to eat it — around exercise, before sleep, at breakfast — see [When to eat protein](#protein-timing).

How much protein you eat in a day matters most. But how it's spread across the day matters too: muscle is built and repaired in bursts after each meal, and a meal with too little protein triggers only a small burst. So besides the daily target, it helps if most meals carry a worthwhile amount.

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

**Why it uses DCP.** The studies behind these figures used high-quality protein — dairy, egg, meat, soy. [DCP](#gloss-dcp) is NuMa's measure of exactly that: the protein that's both digestible and complete. So a meal of 30 g raw protein from foods with a low [DIAAS](#gloss-diaas) can fall short while its raw figure looks ample. Where a meal's [DCP](#gloss-dcp) can't be worked out (its foods lack amino acid data), NuMa compares raw protein instead and says so. Leucine is the amino acid most closely tied to switching on muscle building, which is why it's shown alongside; it's the raw amount in the meal's foods.

**What it doesn't do.**

- **It never flags a meal as "too much".** The long-held idea that the body can only use 20–25 g of protein at once has been overturned: a large dose produces a larger and longer-lasting response[^68]. A big meal is fine; the point is not to have meals with too little.
- **It doesn't check timing.** The sports guidance suggests such meals every 3–4 hours[^65], but NuMa doesn't record what time you ate, so it counts meals, not hours. What the research says about timing is in [When to eat protein](#protein-timing).
- **It's about muscle, not your daily total.** Meeting the per-meal amount doesn't replace your daily protein target — see [Daily Nutrient Goals](#goals).

These figures come mostly from studies of muscle protein synthesis in healthy adults, many of them active. They're a sensible guide for anyone wanting to keep or build muscle — especially older adults — not a medical prescription. If you have kidney disease or another condition that limits protein, follow your clinician's advice instead.


### G. DIAAS — Digestible Indispensable Amino Acid Score {: #diaas}

*Search terms: protein score, protein quality score, PDCAAS, digestibility score.*

[DIAAS](#gloss-diaas) measures how well your body can actually use the protein in a food. A score of **1.0** means the protein fully meets the [FAO 2013 amino acid reference standard](#fao) after accounting for digestibility[^16]. Scores above 1.0 are excellent; below 1.0 means one or more amino acids fall short.

Animal proteins typically score 1.0 or above. Most plant proteins score below 1.0, though some (pea protein, soy) come close. Digestibility matters because some protein in food is never absorbed — it passes through unchanged or is broken down by gut bacteria rather than used by your body.

A note on terminology: the [FAO](#gloss-fao) uses the term "indispensable amino acids" ([IAA](#gloss-iaa)) where this manual uses "essential amino acids" ([EAA](#gloss-eaa)) — both refer to the same nine amino acids. The "I" in [DIAAS](#gloss-diaas) stands for "Indispensable."

NuMa uses [DIAAS](#gloss-diaas) to calculate digestible [complete protein](#gloss-complete-protein) ([DCP](#gloss-dcp)), which is a better indicator of actual protein quality than raw grams. See [Digestible Complete Protein (DCP)](#dcp).

#### Estimating DIAAS by hand for a packaged food {: #diaas-estimate-table}

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


### H. Limiting-Amino-Acid Scoring {: #aa-scoring}

*Search terms: limiting amino acid, two adjustments, two-stage calculation.*

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

*Search terms: DCP cap, absorbed protein limit, DCP lower than expected.*

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

*Search terms: reference pattern, amino acid requirements, WHO.*

The [FAO](#gloss-fao) (Food and Agriculture Organization of the United Nations) published a reference amino acid scoring pattern in 2013 that defines the minimum amounts of each essential amino acid per gram of protein needed to meet adult human requirements. This is a ratio, not an absolute quantity — the requirement scales with how much protein you eat, so a small meal and a large meal must both hit the same per-gram proportions. See [Appendix A](#appendix-protein-quality) for the full worked explanation of why this ratio, not total protein, determines what your body can use.

NuMa uses this pattern as the benchmark for all protein quality scoring: completeness, gaps, and complement calculations. A score of **1.0** for an amino acid means the food exactly meets the [FAO](#gloss-fao) reference for that amino acid; above 1.0 exceeds it; below 1.0 falls short.

The [FAO](#gloss-fao) 2013 pattern replaced an older 1991 standard and is the current international reference for protein quality assessment.

#### The reference values {: #fao-reference-values}
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

**How to read it.** A protein meets the reference for leucine if each gram of it supplies at least 61 mg of leucine — after [digestibility](#gloss-tid) is taken into account. Divide what a food actually supplies by these figures and you get the score for each amino acid; the lowest score is the food's [DIAAS](#gloss-diaas), and that amino acid is its [limiting amino acid](#gloss-limiting-amino-acid). [Appendix F](#appendix-diaas-validation) works a real meal through every step.

**Why pairs.** Methionine and cysteine are scored together, as are phenylalanine and tyrosine, because the body makes cysteine from methionine and tyrosine from phenylalanine — what matters is the pair's total.

**One pattern, for everyone over 3.** The report also gives higher patterns for infants and for children from six months to three years, whose growth needs more of each amino acid per gram of protein. NuMa uses the over-3 pattern throughout; it isn't meant for planning a young child's diet.


### K. Amino Acid Gaps {: #gap}

*Search terms: shortfall, deficiency, low amino acid score.*

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

*Search terms: phytates, oxalates, lectins, mineral absorption, anti-nutrients.*

Most people have never encountered this term, yet [antinutrients](#gloss-antinutrient) are present in virtually every plant food. Understanding them is especially important for anyone eating a plant-predominant diet, because the same foods that supply the most fiber, minerals, and [phytonutrients](#gloss-phytonutrients) are often the ones that contain the highest [antinutrient](#gloss-antinutrient) loads.

#### What is an antinutrient?

*Search terms: definition, what antinutrients are, absorption blockers.*

The word sounds alarming, but it simply means a naturally occurring compound in a food that partially blocks the absorption or use of a nutrient your body would otherwise receive. The effect is not binary — it is a matter of degree, and it can usually be reduced or eliminated by how you prepare the food.

They are not contaminants or the result of farming practices; they are part of the plant's own biology. Some are defenses against insects and animals that would eat the plant, such as lectins and trypsin inhibitors[^107]. Others have different jobs: phytate is the main way seeds store phosphorus[^102].

#### The main antinutrients that appear in NutriMagnus output

*Search terms: trypsin inhibitor, tannin, goitrogen, oxalic acid.*

**Phytates** (phytic acid). Found in legumes, whole grains, nuts, and seeds. Phytate binds tightly to minerals — especially iron, zinc, calcium, and magnesium — forming a complex the body cannot easily absorb[^102]. A meal of lentils or whole-wheat bread may contain all the iron the label shows, but much of it may pass through unabsorbed if phytate is high. The effect depends on the rest of the meal: vitamin C eaten at the same meal counteracts phytate's effect on iron, and more vitamin C counteracts more of it[^103]. Preparation methods that reduce phytate: soaking legumes or grains overnight before cooking; sprouting; fermentation[^102]. In one study, sourdough fermentation cut the phytate in whole wheat bread by about 62%, against about 38% for ordinary yeast bread, and by about 90% when the bran was fermented first[^104]. Tempeh and other fermented soy products are low in phytate.

**[Oxalates](#gloss-oxalate)**. Found at high levels in spinach, Swiss chard, beet greens, rhubarb, and almonds; at moderate levels in many other plant foods. [Oxalates](#gloss-oxalate) bind calcium in the gut, meaning the calcium shown on a food label for spinach is largely unavailable — in a direct comparison, people absorbed about 5% of the calcium in spinach against about 28% of the calcium in milk[^105]. For most people this is simply a reason not to rely on spinach as a calcium source, not a reason to avoid it. For people prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly. See [oxalate data](#oxalate) for the detailed data NuMa tracks on this.

**Lectins** and **trypsin inhibitors**. Found in raw legumes (beans, lentils, chickpeas, soybeans). Lectins interfere with the gut lining; trypsin inhibitors block a key digestive enzyme. Raw kidney beans contain enough lectin to cause acute food poisoning: as few as four or five raw beans can cause symptoms. The US Food and Drug Administration advises soaking dried beans for at least 5 hours, pouring the water away, and boiling them in fresh water for at least 30 minutes, and warns that slow cookers don't get hot enough to destroy the lectin[^106]. Trypsin inhibitors are more resistant to heat; ordinary cooking removes most of their activity, though not necessarily all[^107]. Canned beans are already cooked. Tofu and tempeh are also safe because both involve prolonged heat treatment or fermentation. This is the one [antinutrient](#gloss-antinutrient) on this list that is not just about partial reduction — with raw legumes, proper cooking is required.

**Bound niacin** (in corn). Untreated corn contains niacin in a chemically bound form the human body cannot absorb. Populations who ate corn as a dietary staple without treatment historically developed pellagra (severe niacin deficiency), and outbreaks still occur where untreated maize is the staple food[^108]. The traditional solution — practiced for thousands of years by Mesoamerican cultures and still used today — is nixtamalization: soaking dried corn in an alkaline lime solution. This releases the bound niacin so the body can use it[^108]. Tortillas, masa, hominy, and grits made from nixtamalized corn are fine. Plain cornmeal (not nixtamalized) retains the problem.

#### How these appear in NutriMagnus output

When you view a food with known [antinutrient](#gloss-antinutrient) concerns, a note appears in the Bioavailability section of the analysis. The note names the compound, describes the specific problem, and lists the preparation method(s) that reduce it.

#### Examples of what you may see

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

These notes appear only for foods where NuMa has a curated flag — the list is not exhaustive, and absence of a note does not mean a food is free of [antinutrients](#gloss-antinutrient). NuMa recognizes a food by whole words in its name (beans, lentils, oats, cornmeal…), with exclusions for names that only look like a match — jelly beans, coffee beans, goat cheese, nutmeg, cornstarch, sweet corn — so a note means the food really is of that kind. The dried-bean note is left off beans that are already cooked or canned.

**Dried beans in a slow cooker.**{: #slow-cooker-beans} When a recipe uses dried beans (directly or in a sub-recipe) and its instructions mention a slow cooker or Crock-Pot, the recipe page shows a red **food safety** warning at the top, and the printed recipe carries it above the instructions. A slow cooker doesn't get hot enough to destroy the lectin in dried beans; boil them first, as described above, or use canned beans. If your instructions already say to boil the beans first, the warning doesn't apply — NuMa only sees the words "slow cooker", not what happens before it.

#### What these notes do not mean

*Search terms: should I avoid, safe to eat, healthy foods, reassurance.*

They are not a reason to avoid these foods. Legumes, whole grains, nuts, and leafy greens are among the most nutritious foods available. The minerals and protein they supply — even after [antinutrient](#gloss-antinutrient) reduction — are substantial, and their other benefits (fiber, [phytonutrients](#gloss-phytonutrients), cost, sustainability) are undiminished. The notes exist so you can make informed preparation choices and avoid assuming that every labeled nutrient is fully absorbed.

The practical message is: soak legumes, prefer sourdough or sprouted grains when possible, cook beans fully, pair iron-rich plant foods with vitamin C, and do not rely on spinach as your primary calcium source.


### M. Oxalate Data {: #oxalate}

*Search terms: low-oxalate diet, Harvard oxalate table.*

[Oxalates](#gloss-oxalate) are one of the [antinutrients](#gloss-antinutrient) discussed in [antinutrients](#antinutrients). The section here covers the detailed data NuMa tracks and how to use it. For general background on what [oxalates](#gloss-oxalate) are and how they compare to other [antinutrients](#gloss-antinutrient), read [antinutrients](#antinutrients) first.

[Oxalates](#gloss-oxalate) (oxalic acid) bind calcium in the gut, reducing its absorption from high-[oxalate](#gloss-oxalate) foods. They are found at very high levels in spinach, Swiss chard, beet greens, and rhubarb, and at notable levels in almonds and some other nuts. For most people the main consequence is that these foods are poor calcium sources despite their labels. For anyone prone to calcium-[oxalate](#gloss-oxalate) kidney stones, total dietary [oxalate](#gloss-oxalate) matters more directly.

NuMa includes the Harvard T.H. Chan School of Public Health [oxalate](#gloss-oxalate) table (433 foods, November 2023 edition), credited to Dr. John Knight of the University of Alabama School of Medicine, whose laboratory measured many of its values[^11]. This data is optional and disabled by default.

**To enable it:** Settings → Your Profile → check "Look up oxalate content for foods," then Save profile.

Once enabled, viewing a food or analyzing a recipe automatically looks it up in the Harvard table by name and links the best match — no confirmation prompt. That link is saved the first time and reused after, so the lookup only runs once per food.

#### Correcting a wrong match {: #oxalate-link-correction}

*Search terms: wrong oxalate match, fix oxalate match, correct oxalate.*

Since the match is automatic and name-based, it's sometimes wrong. A food's page marks an unconfirmed automatic match with "auto-matched — correct if wrong"; click that link to open a search page over the same Harvard reference table. Search for the right entry, select it, and save — or, if the food genuinely isn't in the Harvard table at all, choose "This food is not in the oxalate reference table" instead, which stops NuMa from re-matching it on future lookups. Either choice marks the food as user-confirmed, so the "auto-matched" warning won't reappear for it.

#### How to read a reference entry {: #oxalate-row}

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

Pick the row whose description best matches the food you actually eat — same preparation (raw vs boiled matters a great deal for [oxalate](#gloss-oxalate)), same form, same sort of product. A near-miss on the name with the wrong preparation is a worse match than a slightly different name with the right one.

#### What the categories mean {: #oxalate-categories}

*Search terms: oxalate bands, low oxalate, oxalate levels.*

NuMa bands every value into one of five categories, and colors it accordingly on a food's page. The Harvard table gives values only, with no bands; these cut-offs are NuMa's own, chosen to separate the foods that matter for oxalate from those that don't. Where a per-100 g figure exists, the band comes from that:

| Category | Per 100 g |
|---|---|
| Very high | 300 mg or more |
| High | 100–299 mg |
| Moderate | 25–99 mg |
| Low | 5–24 mg |
| Negligible | under 5 mg |

Rows that have only a per-serving figure are banded on that figure instead, using a lower set of cut-offs — 100 mg or more for very high, then 26, 10 and 2 mg. The two scales aren't interchangeable, which is worth remembering when comparing a volumetric row against a weighed one.

For scale: anyone managing calcium-[oxalate](#gloss-oxalate) kidney stones is often advised to stay under 40–50 mg of total [oxalate](#gloss-oxalate) a day[^109] (some guidance uses a looser 100 mg; follow your own clinician's figure), so a single "very high" serving can exceed a day's allowance on its own. For everyone else the categories are best read as a guide to which foods are poor calcium sources rather than as a budget.

#### Measured or estimated {: #oxalate-measured}

The Harvard table marks some values with an asterisk to say they were **measured directly** in that food; the rest were **estimated** from measurements of a similar food. NuMa shows which is which on both the match page and the food's own page (235 of the 433 entries are direct measurements).

An estimated value is still worth having — it's a reasoned inference by the people who compiled the table, not a guess — but it carries more uncertainty than a measured one. When two candidate rows fit your food about equally well, the directly-measured one is the better pick.

#### What NuMa saves from a match {: #oxalate-what-is-stored}

*Search terms: confirmed match, oxalate choice saved.*

Saving on the match page records your choice of reference entry against that food, marked as confirmed by you. Two consequences: the "auto-matched" warning stops appearing, and NuMa never re-runs name-matching for that food, so your choice can't be silently replaced later.

Choosing "This food is not in the oxalate reference table" is saved the same way, and means the food contributes no [oxalate](#gloss-oxalate) figure at all — which is the honest outcome when nothing in the table matches, and better than carrying a wrong number into every recipe total the food appears in.

Note that this is *your* map from food to reference row, stored in your own [database](#gloss-database). The Harvard table itself is a bundled read-only file that NuMa never writes to, so nothing you do here changes the reference data — only which row your food points at.

#### Important limitations

*Search terms: oxalate limitations, accuracy.*

- [Oxalate](#gloss-oxalate) values in the Harvard table are reported per serving, not per 100 g. For foods measured in ounces (fish, nuts, meat), NuMa automatically converts to per-100g. For foods measured in cups, pieces, or tablespoons, only the per-serving value is available. Volumetric servings cannot be converted to per-100g without knowing the food's density — that conversion must be done manually if needed.

- For recipe analysis, NuMa sums [oxalate](#gloss-oxalate) only for ingredients where a per-100g value is available. Volumetric-only items are excluded from the total and noted as such.

- [Oxalate](#gloss-oxalate) content varies with preparation method (cooking reduces [oxalate](#gloss-oxalate) in spinach, for example) and growing conditions. All values should be treated as estimates.

- Matching by food name is approximate. "Spinach, raw" in the Harvard table maps reasonably to [USDA](#gloss-usda) spinach entries, but processed or branded foods may not match well. Always verify the match makes culinary sense before confirming it.

For background on [oxalates](#gloss-oxalate) and kidney health, see the Harvard Health references in the source data; the table's source (Harvard T.H. Chan School of Public Health) is named under every oxalate table NuMa shows.


### N. Glycemic Index {: #gi}

*Search terms: blood sugar, low GI, high GI, carbohydrate quality.*

<!-- t:26-10-10 -->

The glycemic index ([GI](#gloss-gi)) measures how quickly a carbohydrate-containing food raises blood glucose compared to pure glucose ([GI](#gloss-gi) = 100). Low-[GI](#gloss-gi) foods (55 or below) produce a slower, more gradual rise; high-[GI](#gloss-gi) foods (70 and above) cause a faster spike.

**Every [GI](#gloss-gi) figure NuMa shows is one you put there.** Nothing looks [GI](#gloss-gi) up automatically, because no nutrient [database](#gloss-database) NuMa draws on carries it — so a food shows a [GI](#gloss-gi) if, and only if, you supplied one, either by typing it in or by picking a row from the bundled reference table (see [Where GI values come from](#gi-source-para) below). Choosing which published value fits a food is a judgment call, and it stays yours; NuMa won't make it for you. Once saved, the value appears in the **GI** column wherever that food is listed — Food Cache, Pantry, food search, a meal's add-food panel — on the food's own page, and in any glycemic load NuMa computes from it.

**What it's good for.** [GI](#gloss-gi) is at its most reliable comparing like with like, where the two foods differ in one respect you're choosing between — this bread against that bread, parboiled rice against sticky rice. But it is genuinely useful across categories too, whenever two foods are candidates for the same job: bread and rice at breakfast really do behave differently, largely because of physical form, and [GI](#gloss-gi) is what tells you so. What *doesn't* survive the comparison is quantity. [GI](#gloss-gi) is measured on a fixed dose of available carbohydrate (usually 50 g) rather than on a serving of food, so two foods with the same [GI](#gloss-gi) can have very different effects at the amounts you'd actually eat. That's what the glycemic load number is for — see [Glycemic Load](#gl).

**What it doesn't capture.** [GI](#gloss-gi) describes a food eaten alone. Combining foods in a meal (especially adding fat, protein, or fiber) physiologically blunts the blood glucose response to the carbohydrates present, by slowing gastric emptying and glucose absorption. However, this effect is not fully captured by glycemic load ([GL](#gloss-gl)) either — see [Glycemic Load](#gl) for why.

NuMa displays [GI](#gloss-gi) for reference only and does not use it in protein quality calculations.

**Where [GI](#gloss-gi) values come from.**{: #gi-source-para} Neither [USDA](#gloss-usda) nor Open Food Facts[^3] tracks [GI](#gloss-gi), so NuMa can't look it up automatically the way it does for calories or protein — you have to supply it, but NuMa makes that easy. Every food's [Food Cache](#food-cache-web) → **Annotate** page has a **"Look up a GI value from the published reference table"** section: type the food's name (already pre-filled for you), pick which subject population you want — normal glucose tolerance, impaired glucose tolerance/diabetes, or both — and NuMa searches the full published reference table[^8] — about 2,500 foods as shipped, or over 4,000 if you [add the newer edition](#gi-editions) — and lists every plausible match, not just its single best guess. Click **Use this GI value** next to whichever one actually matches your food and its value fills the [GI](#gloss-gi) field; nothing is written until you save the annotation.

When you add a food to your Pantry or a meal and it has no [GI](#gloss-gi) or [DIAAS](#gloss-diaas) estimate yet, NuMa offers to take you to its Annotate page to add them — and keeps offering each time until you save that page once (leaving a value blank on purpose counts). Adding a food to a recipe doesn't prompt. That way your data builds up naturally through normal use, even without visiting Annotate directly.

#### Normal and impaired — which people a value was measured in {: #gi-populations}

Every search result is labeled with the subject group the value was actually measured in, taken from that row's own entry in the table[^8] rather than inferred from anything else:

* **Normal glucose tolerance** — ordinary healthy volunteers. This is the bulk of the table and the default assumption behind any [GI](#gloss-gi) figure you see quoted anywhere.

* **Impaired glucose tolerance** — people with type 1 or type 2 diabetes, gestational diabetes, or diagnosed impaired glucose tolerance ([what this covers, and how to use such a value](#gi-impaired)). Where the table gives the number of subjects, NuMa shows that too (`Type 2, n=9`), because a nine-person study and a thirty-person study do not deserve equal weight.

* **Subject group not stated** — the table didn't record who the value was measured in. These appear in *both* the normal and impaired lists rather than being hidden from both, since a value with an unrecorded population is still a real measurement; the label tells you to treat it cautiously.

Which of these to pick for your own foods is covered next.

#### Choosing a GI value — which result to use for a food {: #choosing-gi-values}
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

See also the [GI](#gloss-gi) caveats in [Appendix C](#appendix-gl-comparison).

#### Foods with no GI anywhere and little carbohydrate {: #gi-low-carb}
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

#### Daily glycemic load target {: #gl-target}

*Search terms: GL target, daily GL limit, glycemic load ceiling, blood sugar limit.*

An optional personal ceiling for a whole day's [GL](#gloss-gl), set under **Settings → 1. Your Profile** (**Daily glycemic load target**; leave it blank to turn it off). It's a *limit*, shown the way a nutrient's maximum is: under it is good. Not sure what number to use? **Help me choose a target**, right under the box, offers three starting points with their reasons — see [Choosing a daily glycemic load target](#gl-target-choose).

Where it shows, once set:

- **A day's pages** (the day view, the Daily Summary for a date, the day printout) — under the Glycemic Load figure: "Your daily target: 80 — 64%", or "— over it" in the over-limit color, or "close to it" from 80% up.
- **Recent Days** — the **Day GL** figure is colored against the target; hover for the percentage.
- **Nutrient averages across days** — how many days in the window were over it.
- **[What-if: Meals](#whatif-gl)** — days over it *before and after* your changes. An average can sit comfortably under the target while several days are over it; this count shows those days, and whether a change fixes them.

**Days with missing GI values.** A day's [GL](#gloss-gl) counts only foods with a [GI](#gloss-gi), so it's a lower bound when some are missing. If that lower bound is already over the target, the day is over for certain and is shown so. If it's under, NuMa says it can't tell yet rather than calling it under — the missing foods could push it over.

Like the rest of your profile, the target is [pinned to each day](#day-profile) as it's logged, so changing it later doesn't rewrite how past days were scored.

#### Choosing a daily glycemic load target {: #gl-target-choose}

*Search terms: GL target, what number, recommended GL.*

**There is no official number.** No diabetes or nutrition guideline sets a daily [GL](#gloss-gl) target. The American Diabetes Association's Standards of Care set none, and the UK's NICE (National Institute for Health and Care Excellence) and Diabetes Canada recommend low-[GI](#gloss-gi) carbohydrate choices without giving a figure[^64]. The research shows a slope, not a line: across large long-term studies, the risk of type 2 diabetes rises steadily with daily [GL](#gloss-gl), with no level below which it stops mattering[^63]. So any target is a point you choose on that slope — lower is better, on average — and the useful question is which starting point suits you.

**Help me choose a target**, under the target box in [Settings](#settings) → 1. Your Profile, offers three. Click one to fill the box, then save.

1. **Scaled to your calorie target (recommended).** 80 × your daily calorie target ÷ 2,000 — for example, 96 for 2,400 kcal, 64 for 1,600. *Who it suits:* most people. It starts from the University of Sydney GI Foundation's description of a "moderate" [GL](#gloss-gl) diet, an average daily [GL](#gloss-gl) under 80 per 2,000 kcal[^61], and scales it to how much you actually eat, so a large or active person isn't held to a small person's number. NuMa takes your calorie target from your profile (see [Daily Nutrient Goals](#goals)). *Limits:* the Foundation states the figure without saying what study it comes from.
2. **The common convention: 80.** *Who it suits:* anyone who wants the figure most often quoted for a "low glycemic load day", the same for everyone. *Limits:* it's widely repeated — for example by the UK's advertising regulator — but nobody cites a study for it[^62], and it doesn't allow for body size or activity. For someone eating well over 2,000 kcal, option 1 is fairer.
3. **A step down from where you are.** Your own average daily [GL](#gloss-gl) over the last 30 days, minus 10–20% (NuMa fills in the middle of that range). *Who it suits:* someone who wants a gradual, achievable change rather than a jump to an outside number — and whose current average is already near or below the others, who'd learn nothing from them. *Limits:* it's not a published target; it rests only on the finding that lower is better on average[^63]. It needs at least 7 days in those 30 with a complete [GL](#gloss-gl) (every food with carbohydrate has a [GI](#gloss-gi)); fewer, and NuMa doesn't offer it, since the average would mean little.

**If you have diabetes, pre-diabetes or insulin resistance**, set the number with your doctor or dietitian. Any of the three can be a starting point for that conversation, but none is a treatment target, and your own glucose readings ([CGM](#gloss-cgm), if you use one) are the better guide — see [Appendix C](#appendix-gl-comparison).

#### What "impaired glucose tolerance" means here, and using such a value {: #gi-impaired}

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

**If you do have diabetes, pre-diabetes or insulin resistance**, these are the values measured in people like you — prefer them, and the closer the match (type 2 rows if you have type 2), the better. Whatever group a value comes from, your own response is the final word: see [Continuous Glucose Monitoring](#appendix-gl-comparison) in Appendix C.

**Where NuMa reminds you.** Once you've saved a value picked from an impaired-tolerance row, NuMa marks it wherever it matters: a note under the value on the Annotate page and the food's own page; a **†** beside its [GI](#gloss-gi) in Top Contributors ranked by glycemic load and in [lower-GI swap](#gl-swaps) suggestions; and, under a meal's, recipe's or day's Glycemic Load figure, a line naming each food whose [GI](#gloss-gi) came from such a row. What the note says depends on **Your glucose tolerance** under [Settings](#settings) → 1. Your Profile: set to impaired, it tells you the value fits you (best when the study's subjects had your own type); set to normal, it tells you to treat the value as an approximation and prefer a normal-tolerance one where the table has it; not set, it gives both readings and offers a link to set it. A value you typed by hand, or picked from a normal-tolerance or not-stated row, isn't marked.

By default the lookup searches both populations at once. If you'd rather it default to just one — say, you have diabetes and always want the impaired-tolerance values shown first — set **Your glucose tolerance** under [Settings](#settings). You can still switch populations for any individual lookup regardless of that default.

#### Method quality, and why some rows are flagged {: #gi-method-quality}

*Search terms: study quality, flagged rows.*

Subject group is one axis; how well the study was run is a separate one, and the table[^8] splits its rows on exactly that. There is an international standard for measuring [GI](#gloss-gi) — [ISO](#gloss-iso) (International Organization for Standardization) 26642:2010 — which sets out how much carbohydrate the test portion must contain, how many people must be tested, and when blood must be sampled.

* Rows from studies that **met** that standard carry no flag. They are the bulk of what you'll see, and they are the ones to trust.

* Rows from studies that **deviated** from it are marked **non-ISO method**. The deviation might be fewer than ten subjects, a test portion with an unusual amount of carbohydrate, an unrepeated reference food, or results whose [standard error](#gloss-standard-error) was wide enough that the average is shaky.

A **non-ISO method** flag is not a warning about the food — it's a warning about the *evidence*. Be especially wary when a flagged value looks extreme, since an implausibly low or high figure is exactly what a tiny or high-variance study tends to produce.

Note that the two things are genuinely independent: most non-ISO rows were still measured in normal-tolerance subjects, and an unflagged row can still have been measured in people with diabetes. That's why NuMa shows them as two separate pieces of information rather than rolling them into one tag.

#### How to read a lookup result {: #gi-result-row}

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

#### What NuMa keeps from a lookup {: #gi-what-is-stored}

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

#### Upgrading to the 2021 tables {: #gi-editions}

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

#### Why these tables instead of the University of Sydney database {: #gi-why-foster-powell}

*Search terms: GI database, why not Sydney.*

Two candidate sources exist for bulk [GI](#gloss-gi) data, and they're related but not the same. Brand-Miller — a co-author of the published tables[^8] — also runs the University of Sydney's GI research group, and a great many entries in those tables came from the Sydney group's own lab testing, so there's real lineage and overlap between the two.

But they differ in ways that matter for a bulk local lookup table. The published tables are a fixed, peer-reviewed, citable snapshot: a static document that can be read into a file once and then work offline and identically every time — and in the 2008 edition's case, explicitly Creative Commons licensed, so NuMa can ship it outright. The Sydney [database](#gloss-database) (glycemicindex.com) is a live, continuously updated, searchable website — larger and more current, but a site to query rather than a table with a clear bulk-redistribution license; scraping it for a local table would be a licensing gray area at best.

That's why NuMa's built-in table comes from the published tables, and why glycemicindex.com is listed in [Internet resources](#internet-resources) as a manual look-up fallback rather than something NuMa imports from directly.

### O. Glycemic Load {: #gl}

*Search terms: blood sugar, carbohydrate amount, carbs.*

Glycemic load ([GL](#gloss-gl)) improves on the glycemic index by accounting for both the quality and the quantity of carbohydrate in a serving[^69]. The formula is:

```
GL = (GI × grams of available carbohydrate) / 100
```

For a meal combining multiple foods, the total [GL](#gloss-gl) is the sum of the [GL](#gloss-gl) calculated separately for each component:

```
Meal GL = GL(food 1) + GL(food 2) + GL(food 3) + ...
```

Adding more carbohydrate-containing foods will always increase the meal total. The reason combining foods physiologically blunts the blood glucose response — as noted in the [GI](#gloss-gi) section — is not reflected in this calculation. Protein, fat, and fiber slow gastric emptying and glucose absorption, reducing the actual blood glucose rise. Gram for gram, protein lowers the rise about twice as much as fat does[^89], and the thick (viscous) kinds of fiber in foods such as oats and legumes do it best[^90]. But because [GL](#gloss-gl) is calculated from fixed [GI](#gloss-gi) values measured for each food in isolation, it has no way to represent that interaction. [GL](#gloss-gl) is therefore a reliable tool for comparing meals of broadly similar macronutrient composition[^91], but becomes less accurate when meals differ significantly in their fat or protein content[^92].

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

NuMa shows [GL](#gloss-gl) for every food (per 100 g, and for the exact portion you are analyzing — halve the portion and the [GL](#gloss-gl) halves with it while the [GI](#gloss-gi) stays put, which is the whole point of the measure), every recipe (per serving) and every meal and day. When some foods have no [GI](#gloss-gi) value the figure is marked incomplete rather than hidden — see [Glycemic Load Output](#glycemic). Recipes, meals and days also get an [estimated GI](#mixture-gi), worked out from their foods' own values. Like [GI](#gloss-gi), it is shown for reference and does not affect protein quality calculations.

**Averages beat single days.** A single day's [GL](#gloss-gl) swings with whatever happened to be eaten. **Nutrient averages across days** (from Analysis → Daily summary) shows your average daily [GL](#gloss-gl) across the last 7, 14 or 30 days, and the [Nutrient Plot](#nutrient-plot) offers **Daily glycemic load** as a plottable series so you can see the pattern — weekends, late evenings, stressful weeks — instead of a snapshot. The average skips any day whose [GL](#gloss-gl) is incomplete rather than counting it as a low day, and tells you how many days actually contributed. The plot is a little more forgiving: it also draws an incomplete day once foods with a GI make up at least 80% of that day's carbohydrate, as a hollow point meaning "at least this much", and leaves out the rest; a note under the plot counts both.

For a discussion of how [GL](#gloss-gl) compares to other approaches for evaluating the blood glucose impact of different meal choices — particularly relevant for people managing diabetes — see [Appendix C: GL and Blood Glucose Comparison](#appendix-gl-comparison).


#### What you can do with GI and GL {: #gl-uses}

*Search terms: using GI, using GL, lower blood sugar, practical use.*

[GI](#gloss-gi) values are only worth entering if they help you choose. Here's how NuMa puts them to work, roughly in the order you'd use them.

1. **Read a meal's or recipe's [GL](#gloss-gl) and its band.** It's under **Glycemic Load** on the meal or recipe page (one serving for a recipe), against the per-serving scale; a whole day's, on the day's pages and in the **Day GL** column of Recent Days, against the larger day scale. A line under every band says which scale it's on.
2. **See which foods drive it.** The **Which foods drive it, and lower-GI swaps to try** link under the figure ranks the foods by their share of the [GL](#gloss-gl) ([Top Contributors](#top-contributors)). Usually one or two foods carry most of it.
3. **Change one of those.** Three levers, in rough order of effect: a **smaller portion** of the top food ([GL](#gloss-gl) halves when the portion does); a **swap** to a similar food with a lower [GI](#gloss-gi) — NuMa [suggests some](#gl-swaps) from your own foods; or **pairing** it with fat, protein, fiber or acid (vinegar, lemon), which slows absorption[^89]<sup>,</sup>[^90]<sup>,</sup>[^93] — real, but not something the [GL](#gloss-gl) number can show (see [why](#gl)).
4. **Check the whole picture before you commit.** Every swap suggestion opens [What-if](#whatif-gl) with the swap filled in: [GL](#gloss-gl) before and after, and every other nutrient too, for one meal, the last 30 days, or a recipe. Nothing changes until you choose to apply it.
5. **Compare candidates side by side.** [Compare](#compare-gl) shows [GI](#gloss-gi) and [GL](#gloss-gl) per 100 g for up to 8 foods and recipes, lowest [GL](#gloss-gl) highlighted.
6. **Set a daily target, if it helps.** An optional [daily glycemic load target](#gl-target) checks every day against a ceiling of your choosing — and What-if counts the days over it before and after a change.
7. **Watch the trend, not the day.** Average daily [GL](#gloss-gl) over a week or more ([Nutrient averages across days](#trend)), or the [GL](#gloss-gl) line in the Nutrient Plot, says more than any single day.
8. **Keep the figures honest.** A [GL](#gloss-gl) only counts foods with a [GI](#gloss-gi); "at least" and "covers N% of the carbohydrate" mean some are missing. [Foods you use with no GI](#missing-gi) on Foods → 9 lists them, most-used first. And a value measured in people with diabetes is marked — [what that means for you](#gi-impaired).

**A worked example.** Say a dinner is 200 g of cooked white rice with chicken and broccoli. Chicken and broccoli have almost no carbohydrate, so the rice is the whole story. Cooked white rice is about 28 g carbohydrate per 100 g ([USDA](#gloss-usda)), so 200 g is about 56 g. The bundled table's "Medium grain white rice, boiled 12 mins" has a [GI](#gloss-gi) of 75: [GL](#gloss-gl) = 75 × 56 ÷ 100 ≈ **42 — High** (20 or more).

Cooked pearled barley also has about 28 g carbohydrate per 100 g, and the table's "Barley, pearled, boiled 60 min" has a [GI](#gloss-gi) of 35. The same 200 g: 35 × 56 ÷ 100 ≈ **20** — less than half, on the High/Medium line. Same amount of food, same carbohydrate; only the kind of carbohydrate changed. (Halving the rice to 100 g instead would give about 21 — similar, but by eating less.)

To try it on your own data: give both foods a [GI](#gloss-gi) from the lookup on their Annotate pages, rank the meal's Top Contributors by glycemic load, and follow the barley suggestion's **see the full effect in What-if** link — it shows the same drop in [GL](#gloss-gl), plus what the swap does to fiber, protein and the rest. Your figures will differ a little with the exact foods and values you pick.

### P. Recommended Dietary Allowances {: #rda}

*Search terms: recommended daily allowance, daily requirements, adequate intake.*

[RDA](#gloss-rda) values in NuMa come from the Dietary Reference Intakes ([DRI](#gloss-dri)) published by the U.S. National Academies of Sciences, by way of the **NIH** (National Institutes of Health) **ODS** (Office of Dietary Supplements)[^9]. Here is the ODS's own definition, word for word:

> "Recommended Dietary Allowance (RDA): Average daily level of intake sufficient to meet the nutrient requirements of nearly all (97–98%) healthy individuals[^9]."

**Read that carefully — an RDA is not a bare-survival minimum.** It's set high enough that following it meets the needs of nearly everyone in your age/sex group, with margin built in. (The government's actual bare-minimum figure, the amount that meets only the *average* person's need with no safety margin, is called the EAR — Estimated Average Requirement — and NuMa doesn't use it for anything, since it's a population-statistics tool, not a personal target.) NuMa still labels this tier "minimum" in a few places in the interface — meaning "meet or exceed this amount," a directional instruction, not a claim about how large the number itself is — see the color-coding note below and [Daily Nutrient Goals](#goals) for exactly what "minimum," "target," and "limit" each mean as goal types.

When you set a user profile (Settings → User profile), NuMa uses your age, sex, weight, height, and activity level to estimate personalized targets — see [Daily Nutrient Goals](#goals) just below for the age/sex bands behind every mineral and vitamin RDA, not just the two formula-based ones (calories, protein) described here. The calorie estimate uses the Mifflin-St Jeor equation with an activity multiplier. The protein target uses 0.8 g per kg body weight as a baseline minimum, rising to 1.0 g/kg at moderate activity and 1.2 g/kg for active and very active people. That 0.8 g/kg figure comes from nitrogen-balance research underlying the 1989 RDA and the 2005 Dietary Reference Intakes of the **IOM** (Institute of Medicine, the US body that sets these figures; renamed the National Academy of Medicine in 2015)[^60] — and it carries an assumption that matters a great deal to anyone eating mostly plants. The next few paragraphs explain it.

#### The protein target assumes high-quality protein {: #protein-rda-quality}

*Search terms: protein requirement, 0.8 g per kg, plant protein needs, vegans need more protein.*

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
                           such goal in Settings → 5. Nutrient Targets - Researched; a dash
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

*Search terms: daily goals, targets.*

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

*Search terms: energy, BMR, TDEE, metabolism, calorie needs.*

    Mifflin-St Jeor equation for Basal Metabolic Rate, multiplied by an
    activity factor based on your activity level setting:

        Sedentary (desk job, little exercise)           x 1.2
        Lightly active (light exercise 1-3 days/week)   x 1.375
        Moderately active (3-5 days/week)               x 1.55
        Active (hard exercise 6-7 days/week)            x 1.725
        Very active (physical job or twice-daily)       x 1.9

#### Protein (minimum)

*Search terms: protein goal, grams per kg, protein need.*

    Scaled to body weight and activity level:

        Sedentary or lightly active   0.8 g per kg body weight
        Moderately active             1.0 g per kg body weight
        Active or very active         1.2 g per kg body weight

#### Carbohydrates (minimum)

*Search terms: carbs minimum, carbohydrate need.*

    130 g/day — the brain's minimum glucose requirement (fixed for all).

#### Fiber (minimum)

*Search terms: fiber goal, fiber need.*

    Age- and sex-dependent Adequate Intake:

        Men under 50: 38 g/day     Men 50+: 30 g/day
        Women under 50: 25 g/day   Women 50+: 21 g/day

#### Sodium (limit)

*Search terms: salt.*

    2300 mg/day — standard Tolerable Upper Intake Level (fixed for all).

#### Omega-3 ALA (minimum)

*Search terms: omega-3 goal, alpha-linolenic acid, flax.*

<pre>
    1600 mg/day men, 1100 mg/day women — Adequate Intake for alpha-linolenic
    acid (<a href="#gloss-ala">ALA</a>), the plant-sourced omega-3. See <a href="#omega3">Omega-3 Fatty Acids</a>
    for why this is the only omega-3 with an official goal in NuMa.
</pre>

#### Omega-6 linoleic acid (minimum)
<pre>
    17 g/day men, 12 g/day women aged under 51; 14 g/day men, 11 g/day women
    at 51+ ("other": midpoint) — Adequate Intake for linoleic acid. Shown in mg
    like the other omega rows (17000 mg and so on).
</pre>

#### Minerals and vitamins — every age/sex band, in full

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

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

*Search terms: trends, several days, weekly average, chronic shortfall, multi-day.*

Every other [RDA](#gloss-rda) comparison in NuMa -- food, recipe, meal, daily summary -- looks at a single day. That's the right window for "did today's meals cover me," but it's the wrong window for a nutrient that's chronically a little short: one low day is unremarkable, but the same shortfall repeated for two weeks straight is exactly the kind of pattern a single-day view can never show you, because you'd have to remember and compare each day yourself.

**Access it via the "Nutrient averages across days" button on the Daily Summary page.** Choose a window -- last 7, 14, or 30 days -- and NuMa averages your total intake for every tracked nutrient across the days in that window that actually had a meal logged, then compares that average against your RDA (and Revised Optimal / max limits, if configured) using the exact same table, color coding, and diet-aware notes as the daily comparison.

**Only logged days count.** If you ask for a 30-day average but only logged meals on 12 of those days, the average is computed over those 12 days -- unlogged days are treated as "no data," not as a zero-intake day. Diluting the average with days you simply didn't track would understate your real intake and could hide the exact shortfall this view exists to surface. The screen tells you how many logged days went into the average (e.g. "Averaging over 12 logged day(s) out of the last 30").

This is the same B12/iron/zinc-aware analysis described in [Diet-Aware Bioavailability and Deficiency Notes](#diet-bioavailability) -- this averaged view is often where a B12 or iron pattern actually becomes visible, since a single low day rarely triggers concern on its own.

**Nutrient totals for a date range or a set of meals.**{: #range-totals} Below the 7/14/30-day buttons (and from the Daily Summary page's **Nutrient totals for a date range or meals** button) are two more ways to choose what to look at:

- **From / To** and **Add up this date range** — any range of dates, not just the last 7, 14 or 30.
- **Meal IDs** and **Add up these meals** — just the meals you list, by their [ID](#gloss-id) numbers (the number on each meal in Meals & Log), separated by commas or spaces. A range like `20-24` means meals 20 through 24. An ID with no meal behind it is named at the top and left out.

Either way the table gains a **Total** column — every nutrient added up across everything chosen — beside the per-day average, which is still the figure compared with your daily goals. Total [DCP](#gloss-dcp) appears under the average. When you pick meals by ID, the per-day average covers only those meals, not everything else eaten on the same days, so read its percentages accordingly; the meals included are listed under **Meals included**.

**Blocks of days.**{: #summary-blocks} The **Blocks of days** button (on the Daily Summary page and here) shows Recent Days' table a block at a time: each row is a run of days — 7 by default — with every column averaged per logged day in that block, most recent block first. Choose the **Days in each block**, the **Number of blocks**, and the **Last day of the most recent block** (today by default), then **Show these blocks**. The columns are the ones you chose for Recent Days, each with its share of the daily goal, plus Day [DCP](#gloss-dcp) and, if you track glycemic load, Day [GL](#gloss-gl). Each block's **Full nutrient totals** link opens the date-range totals above for just that block. Comparing one week with the next this way shows whether a change you made is holding.

This view does not offer protein complement suggestions -- complementation only matters within the roughly 24-hour window your body actually digests and pools amino acids together, so a suggestion pooled across a week or more of eating isn't something you could act on. For an actionable complement suggestion, use [Protein Complement Suggestions](#comp) on a specific day's summary, a meal, or a recipe.


### S. Nutrient Plot {: #nutrient-plot}

*Search terms: graph, chart, nutrient over time, trend line.*

A line plot of one or more nutrients across your logged days, day on the x-axis — useful for spotting a trend visually rather than reading a column of numbers.

**Access it from Analysis → Daily Summary → "Nutrient plot".** Check up to 8 nutrients from the full nutrient list (any nutrient NuMa tracks, not just the ones you've chosen as Meals & Log columns, plus Day [DCP](#gloss-dcp) itself) — Protein, Calories, Carbs, and Fiber are listed first; the checkbox list scrolls vertically below them. **Clear all nutrient checkmarks** above the list unchecks every box in one click, a faster starting point than unchecking a previous selection one at a time when you want to plot a completely different set. Then choose which days to include:

    (blank days-back)         Every logged day, oldest to newest.
    Days back + Ending on     The N days ending on the date you pick
                              (defaults to your most recent logged day).

**Every logged day appears, whether or not its meals are marked complete.** A day with no logged meal at all shows as a **break in the line**, not a false drop to zero, and the line picks up again at the next day with data; a note under the plot says how many such days its span has. Completeness only comes into play through "Always end on last complete day" below. **A nutrient with no data at all in the range** isn't drawn, and a yellow note under the plot names it so it doesn't just quietly go missing. **Daily glycemic load** has its own rule: a day where some carbohydrate food has no [GI](#gloss-gi) is drawn as a hollow point (its real [GL](#gloss-gl) was at least that high) when foods with a [GI](#gloss-gi) make up at least 80% of that day's carbohydrate, and left out below that; a note under the plot counts both kinds of day.

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

*Search terms: download plot, export plot.*

Both "Download [PNG](#gloss-png)" and "Download SVG" save the same plot as an image file you can keep, email, or paste into a document — they just store it differently.

**PNG** is a normal photo-style image, a fixed grid of pixels. It opens everywhere without a second thought, and is the safer default if you're not sure what a document or website will accept.

**[SVG](#gloss-svg)** stores the plot as the shapes and lines that drew it, not pixels — so it stays perfectly crisp at any size, whether you zoom way in on screen or print it on a large sheet of paper. PNG images can look blurry or blocky if enlarged; an SVG never will. The trade-off is that a few older programs don't open SVG files directly (most current web browsers, word processors, and image editors do).

**Rule of thumb:** downloading to look at, email, or drop into a typical document — PNG. Need to print it large, or want it to stay sharp if someone else resizes it — SVG.


### T. Per-Day Profile Tracking {: #day-profile}

*Search terms: profile changes, past days, history, rescoring, pinned profile.*

Your profile isn't fixed forever -- weight, activity level, or even which named profile is active can change over time (illness, travel, a deliberate weight change). But your logged meals stay put. If a past day's [DCP](#gloss-dcp) and RDA comparisons always used *today's* profile, an old day could silently get re-scored against numbers that weren't true of you back then.

**A new day follows your current profile.** The first time a meal is saved for a date, the day starts out with its **current profile** switch ticked (see below), so its goals follow your profile each time you save it. NuMa also keeps a full snapshot of the profile as it was that day -- your age, weight, activity level, and targets -- not just a name. Untick the switch and the day goes back to that snapshot and stays there: later edits to your profile (or a switch to another one) no longer change it. That's how to keep a day's comparisons true to the numbers you had back then.

**Today, even when unticked.** It's still in progress, so whenever you save your profile (in Settings → 1, or a nutrient target under Settings → Nutrient Targets - Researched), today is re-pinned to it at once — unless you've set today's profile by hand with **Change**.

**Applying a change to earlier days.** After you save your profile, Settings shows **Also score every logged day from [date] to today against this profile**. Pick a date and click **Apply profile to those days**: every logged day in that range is switched to your current profile, except days whose profile you set by hand. NuMa says how many days it switched.

**The "current profile" switch.** Each day's Summary and Full Day page has a switch beside "Profile:", **Score this day against my current profile**, and Meals & Log has the same switch, labeled **current profile**, under each day's date. Tick it and the day is scored against your profile as it is now, and keeps following it each time you save your profile. Untick it and the day goes back to the profile it was pinned to, exactly as it was: NuMa keeps that pinned copy for as long as the switch is on. Days switched by **Apply profile to those days** have the switch ticked, so you can put any of them back the same way.

**Where you see it.** If you maintain more than one named profile, a **Profile** column/line appears next to each day: on the Meals & Log list, the Recent Days list, and the Daily Summary / full-day view. With only one profile configured, this column is hidden since there's nothing to distinguish.

**Changing a day's profile.** Sometimes the automatic pin doesn't match reality -- illness or travel rarely starts exactly at midnight. Open that day's summary and use the **Change** control next to "Profile:" (on the day's Summary or Full Day page) to pick a different saved profile. The day is marked "(manually set)" afterward and its DCP/[RDA](#gloss-rda) numbers recompute immediately against the new pin.

**Nutrient averages across days.** The [Nutrient Averages Across Days](#trend) view spans many days at once, so it scores against the profile pinned to the *most recent* day in the window (today, for the usual "last N days"). If any day inside the window was pinned to a different profile, a note discloses which dates and profile differed, rather than silently blending two profiles' targets into one average.

**Existing data.** If you're upgrading from a version of NuMa that didn't have this feature, every day you'd already logged gets pinned to whichever profile is active the first time you open NuMa after upgrading -- you don't need to open or edit anything for this to happen.


### U. Omega-3 Fatty Acids {: #omega3}

*Search terms: fish oil, algae oil.*

NuMa tracks four omega fatty acids: [ALA](#gloss-ala), EPA, and DHA (all omega-3), and linoleic acid (omega-6). Of the three omega-3s, only ALA has an official Adequate Intake, and it appears as a Daily Goal: 1600 mg/day for men, 1100 mg/day for women[^60].

**Why not a goal for [EPA](#gloss-epa) and DHA directly?** No U.S. Dietary Reference Intake exists for EPA or DHA intake on their own -- the official guidance covers only total ALA[^60]. This matters because ALA is not itself the fatty acid your body mostly uses; it has to be converted into EPA and then DHA, and that conversion is inefficient -- estimated at under 5-10% for EPA, and only 2-5% for DHA[^87]. Two people can hit the same ALA target and land in very different places on EPA/DHA status depending on the rest of their diet, genetics, and sex (conversion is more efficient in women, possibly because of an effect of estrogen[^88]).

**Why this matters especially for plant-based eaters.** Direct dietary EPA and [DHA](#gloss-dha) come almost entirely from fish, algae, and other seafood. If ALA (from flax, chia, walnuts, hemp, canola and soy oils) is your only omega-3 source, meeting the ALA goal is necessary but may not be sufficient -- your actual EPA/DHA status depends on that inefficient conversion step, which is why total omega-3 needs may be higher for vegetarians than for people who eat fish[^87]. Common ways to address this without animal fish: algae-oil supplements (a direct EPA/DHA source independent of the ALA conversion pathway), or simply logging ALA-rich foods generously since the target itself already assumes real-world conversion losses are ahead of it.

**Setting your own EPA+DHA target.** Because there's no official [DRI](#gloss-dri) to compute automatically, NuMa can't put a Daily Goal on the EPA or DHA rows the way it does for ALA. If you want to track against a target anyway -- clinical guidance in the 250-500 mg/day combined EPA+DHA range is common[^13] -- set one yourself as a [Revised Optimal target](#optimal) for the EPA and/or DHA rows in Settings → Nutrient targets.

Linoleic acid (omega-6) also has an official [AI](#gloss-ai), and it too appears as a Daily Goal: 17 g/day for men and 12 g/day for women aged 19-50, and 14 and 11 g/day from 51 on[^60]. Read it more loosely than most goals. That AI was set at the typical (median) U.S. intake rather than from a measured need, so about half of people fall a little short of it, and deficiency is essentially unknown in people eating ordinary diets[^60]. Falling short is worth a look only if you're well under it day after day.


### V. Profile Revised Optimal (Recent Research) Targets {: #optimal}

*Search terms: research targets, above RDA, revised targets.*

**A word on terminology, since two different ideas both sound like "optimal":** the standard [RDA](#gloss-rda) (Part 4, Section P) is not a bare minimum — it's already defined to meet the needs of nearly all healthy people in your age/sex group[^9]. What's described in this section is a *different, second* tier: a small number of nutrients where specific, more recent research argues for a target meaningfully *above* even that generous RDA figure. To keep the two clearly apart, NuMa calls this second tier **Revised Optimal (Recent Research)** — never just "optimal" on its own — and the RDA is never relabeled to match it.

Vitamin D shows how this tier can change. The RDA is 15–20 mcg/day. A 2011 Endocrine Society guideline recommended 37.5–50 mcg/day for adults at risk of deficiency[^12], and NuMa used 50 mcg as its default. The Society's 2024 guideline replaced that advice: for healthy adults under 75 it suggests *against* going above the reference intakes, and it suggests more only for people 75 and older (and for children, pregnancy and high-risk prediabetes)[^101]. NuMa follows the 2024 guideline. Rather than change what "RDA" means, NuMa lets you set your own **Revised Optimal target** for any nutrient, on top of the standard RDA, and tracks both side by side.

Configure Revised Optimal targets in **Settings → 5. Nutrient Targets - Researched**. Pick a nutrient, enter your target amount in that nutrient's usual unit, and save. Leave the field blank and save again to clear it. This works for any nutrient NuMa tracks -- not just ones with a standard RDA. Amino acids, [EPA](#gloss-epa)/DHA, and [phytonutrients](#gloss-phytonutrients) have no official [DRI](#gloss-dri) but are still valid Revised Optimal target or [max limit](#maxlimits) candidates; amino acids in particular are more accurately evaluated by the app's [DIAAS](#diaas)-based protein quality scoring (which accounts for total protein intake), so a flat daily gram target here is a coarser measure than that -- useful mainly if you want a simple standalone tripwire for one specific amino acid.

**Loading recommended targets.** Typing values in from scratch is a lot to ask, so the Nutrient targets screen offers a **"load recommended Revised Optimal targets"** button that fills in a small curated set of commonly-cited targets for any of those nutrients you haven't already customized yourself:

| Nutrient | Built-in Revised Optimal default | Source |
|---|---|---|
| Vitamin D | 23 mcg/day, **age 75 and older only** (no default under 75) | Endocrine Society 2024 guideline[^101]: the average daily dose in the trials behind its 75+ advice |
| Omega-3 EPA | 250 mg/day | [ADA](#gloss-ada)/Dietitians of Canada position paper[^13] (250 mg EPA + 250 mg DHA = ~500 mg combined) |
| Omega-3 [DHA](#gloss-dha) | 250 mg/day | Same source[^13] |

These are general population guidance, not personalized medical advice, and every value it loads can still be reviewed and adjusted individually afterward. See [Omega-3 Fatty Acids](#omega3) for why EPA/DHA specifically has no official [DRI](#gloss-dri) to compute automatically. **About the vitamin D default (changed 14 October 2026).** Under 75 there is no vitamin D default: your target is the RDA. From 75, the default is 23 mcg. The 2024 guideline says the best dose "remains unclear" and names none; 23 mcg (about 900 [IU](#gloss-iu)) is the average daily dose in the trials its 75+ advice rests on, and it prefers a daily dose to occasional large ones[^101]. If you loaded the recommended targets before this date, your saved vitamin D target is still the old 50 mcg — change or clear it in Settings → 5 if you want to follow the 2024 advice. If you're pregnant or have high-risk prediabetes, the guideline suggests more than the RDA; ask your clinician how much.

Only these three nutrients have a built-in default. Magnesium, vitamin K2 and choline were assessed for one in October 2026 and not added — see [Expanding Revised Optimal (Recent Research) targets](#expand-revised-optimal) in Part 9 for why.

Once you have at least one Revised Optimal target set, every nutrient analysis table (food, recipe, meal, and daily summary) gains a second "Revised Optimal" set of columns next to the standard "RDA" columns -- the same meal %, day total %, and goal columns you already know, computed against your custom target instead of the RDA. Nutrients you have not customized show a dash ("–") in these columns rather than falling back to the RDA value, so it stays obvious which nutrients you've actually personalized.

Revised Optimal targets are per-nutrient, not per-day -- there is no single "optimal profile" to pick, only individual overrides you add nutrient by nutrient. A Revised Optimal target is always the two-sided "target" kind (see [Color coding](#color-coding)), not the "meet or exceed" kind used for the standard RDA: green in a comfortable range around your target, orange approaching that range from either side, blue if well short, red if significantly over — the same logic calories itself uses against the RDA.


### W. Maximum Nutrient Limits {: #maxlimits}

*Search terms: too much, toxicity, overdose.*

NuMa tracks three tiers of daily maximum, from broadest to narrowest:

- **Sodium's built-in [RDA](#gloss-rda)-tier limit.** Sodium is the one nutrient with a "limit" type right in the standard [RDA](#rda) calculation itself (Part 4, Section Q) — 2300 mg/day, the Chronic Disease Risk Reduction Intake. This is separate from the tier below and isn't configurable.
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

Configure your own max limits in the same place as Revised Optimal targets: **Settings → 5. Nutrient Targets - Researched**.

**Where you see it.** Every nutrient analysis table (food, recipe, meal, daily summary, trend, and the print/[PDF](#gloss-pdf) view) has a **UL** column, far right — whichever of the tiers above applies to that nutrient (your own custom limit if you've set one, otherwise the built-in UL), shown as a plain number when there's nothing to flag. Once a max limit is active for a nutrient — whether it's a built-in default or one you set yourself — NuMa watches your logged intake for the day: when today's total for that nutrient reaches 90% of the limit, the UL column shows a highlighted amber percentage and the whole row is tinted; at or over 100%, both turn red. This check applies to your **day total**, not to any single meal or food in isolation — a max limit is a daily budget, and a single meal being close to it isn't itself meaningful without knowing the rest of the day. On a page with no day-level context (a single food's per-100g view, for instance), the UL column still shows the numeric ceiling itself, just without a live percentage against it.

The max-limit warning is independent of the Revised Optimal target feature -- you can set one, the other, both, or neither for any given nutrient.


### X. Diet-Aware Bioavailability and Deficiency Notes {: #diet-bioavailability}

*Search terms: vegan.*

Your [dietary preference](#diet) setting (Settings → Dietary preferences) is used for more than filtering protein complement suggestions -- it also shapes two parts of your daily [RDA](#gloss-rda) comparison, because a vegetarian or plant-based diet changes not just *what* nutrients you're likely getting, but how much of certain ones your body can actually use.

**Iron and zinc targets are raised on vegetarian and plant-based settings.** Absorbable iron comes in two forms: heme iron (from meat, fish, and poultry, absorbed efficiently) and non-heme iron (from plants, absorbed far less efficiently, and further blocked by phytate in legumes and grains -- see [Antinutrients](#antinutrients)). Zinc absorption is reduced by the same phytate. Rather than silently under-representing this, NuMa raises the iron RDA by 1.8x[^4]<sup>,</sup>[^5] and the zinc RDA by 1.5x[^4]<sup>,</sup>[^6] when your dietary preference is set to Vegetarian or Plant-based only -- figures drawn from the Institute of Medicine's Dietary Reference Intake report and the [NIH](#gloss-nih) Office of Dietary Supplements' fact sheets for these two minerals. This appears as a normal, higher Daily Goal on the RDA comparison and Daily Nutrient Targets screens, with an explanatory note alongside it. Setting your preference back to "All animal foods" returns both targets to their standard values.

**A B12 warning appears for the Plant-based only setting when intake is low.** Vitamin B12 is almost exclusively animal-sourced[^7] -- unlike most nutrient shortfalls, a persistently low B12 reading on a fully plant-based diet isn't something more food logging or dietary variety fixes; it typically means a B12 supplement or B12-fortified food is needed.[^7] NuMa shows this warning only when your dietary preference is Plant-based only *and* today's B12 intake is under 50% of the RDA -- vegetarians (who still eat dairy and eggs) aren't flagged, since those foods are a legitimate B12 source and an occasional low day isn't a structural gap the way it is for a fully plant-based diet. The 50% figure is NuMa's own conservative trigger for surfacing the warning, not a clinical diagnostic threshold -- an actual B12 deficiency is properly diagnosed by a blood test (serum B12, methylmalonic acid, or homocysteine), not by a single day's logged intake.

Both of these are general population guidance based on your stated preference, not personalized medical advice -- if you have a diagnosed deficiency or absorption condition, follow your clinician's specific recommendations instead.

**The protein target is deliberately *not* raised, and that is not an oversight.** It is a fair question why iron and zinc get a multiplier on a plant-based diet while protein — the nutrient this whole program is most concerned about — does not. The difference is whether the penalty is visible in the data. A milligram of iron looks exactly like any other milligram of iron in a food record; nothing in the numbers reveals that the plant-sourced one is absorbed less well, so the only way to account for it is to raise the target. Protein's quality penalty is not hidden that way: it *is* the [DIAAS](#gloss-diaas) score, measured from the amino acid profile of the actual foods you logged, and it is already applied when NuMa computes your [Digestible Complete Protein](#dcp). Raising your protein target on top of that would charge you for the same shortfall twice.

This also answers the harder case, the vegetarian who eats both plant and animal protein and so fits neither rule cleanly. No rule is needed. The pooled meal calculation (see [How NutriMagnus scores meal and recipe protein quality](#protein-scoring)) evaluates whatever mixture you actually ate, so a diet that is half dairy and half legumes produces a quality score that genuinely reflects that mixture — not a category average. What you should watch, on any diet, is the [Digestible Complete Protein](#dcp) row against your protein target, rather than the raw protein row above it. [The protein target assumes high-quality protein](#protein-rda-quality) explains why that is the right comparison for everyone, omnivores included.

### Y. How NutriMagnus scores meal and recipe protein quality {: #protein-scoring}

*Search terms: meal protein quality, pooled DIAAS, recipe scoring.*

(This section explains the meal-level method. For background on single-food [DIAAS](#gloss-diaas) and how amino acid ratios work, see [Appendix A](#appendix-protein-quality).)

Single-food analysis and meal-level analysis use different methods. For a single food, NuMa computes a [DIAAS](#gloss-diaas) score directly from that food's amino acid profile and digestibility. For a recipe or logged meal, it uses the [FAO](#gloss-fao)'s endorsed method for mixed-food meals: it pools the digestible amino acids across all ingredients before scoring. The two approaches answer different questions and will give different results.

#### Why meals need their own calculation

A food that is short in one amino acid can be rescued by a companion food that supplies it generously — but only if you account for both foods together. A calculation that scores each food separately and then averages the scores misses this complementarity. The pooled method captures it correctly: amino acids from every ingredient in the meal are counted together before any ratio is computed.

#### The method, step by step

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

#### From DIAAS to digestible complete protein

*Search terms: DCP calculation, from DIAAS to DCP.*

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

*Search terms: missing amino acids, partial data.*

Not every food in the [USDA](#gloss-usda) [database](#gloss-database) has a complete amino acid profile. When an ingredient is missing that data, NuMa runs the meal-level [DIAAS](#gloss-diaas) calculation using only the ingredients for which data exists, and flags the result as an estimate. The digestible [complete protein](#gloss-complete-protein) figure is then computed against only the protein that comes from those data-complete ingredients — so the result remains meaningful rather than artificially inflated.

##### Filling missing AA profiles at analysis time

When a meal contains ingredients without amino acid data, NuMa tells you how many are affected and distinguishes two situations:

- **Inside a recipe**: the ingredient is part of a recipe you logged as a meal item. Fix these by opening the recipe's ingredient editor and replacing or re-fetching the ingredient there.
- **Standalone meal ingredients**: foods you logged directly to the meal (not inside a recipe). The meal's **Refresh from [USDA](#gloss-usda)** button fetches amino acid data for every such food that USDA has it for, filling in only what's missing (see [Reviewing incoming data](#review-incoming)). For a food USDA has no amino acid data for, replace it with a Foundation or [SR](#gloss-sr) Legacy equivalent — those datasets are the most likely to have full amino acid profiles — or [estimate its amino acids from a similar food](#drafted-foods).

Until then, an ingredient without amino acid data is simply left out of the protein-quality pooling, and named, so you know the figure is short. NuMa never goes online by itself during an analysis.

---

### Z. When to eat protein {: #protein-timing}
<span id="when-to-eat-protein"></span><span id="protein-timing-exercise"></span><span id="nutrient-timing"></span>
*Search terms: protein timing, when to eat protein, protein before or after exercise, anabolic window, workout, resistance training, endurance, protein before bed, pre-sleep protein, breakfast protein, time of day, meal timing.*

What the research says about *when* to eat protein, as distinct from [how much per meal](#protein-per-meal). Most of it comes from studies of muscle building in healthy, often young and trained, adults; where a finding is narrower than that, it says so.

#### First: the daily total matters most

*Search terms: total protein, daily protein total.*

Before any question of timing, the biggest single factor is how much protein you eat over the day. The International Society of Sports Nutrition (ISSN) puts meeting the daily total — "preferably with evenly spaced protein feedings" — as the primary emphasis[^70]. When studies of protein "timing" are corrected for the fact that the timed group often simply ate more protein, most of the timing effect disappears[^71]. And extra protein stops adding muscle at around 1.6 g per kg of body weight a day in people doing resistance training[^72]. So: get the daily total right first; timing is the refinement.

#### Spread it across the day

The best-supported timing advice is to **spread protein fairly evenly over your meals**, rather than eating most of it at dinner. In a controlled study, the same daily protein eaten as about 30 g at each of three meals produced 25% more muscle protein synthesis over 24 hours than the typical pattern of little at breakfast and a lot at dinner[^73]. The [ISSN](#gloss-issn) suggests 20–40 g every 3–4 hours[^70]. This is what NuMa's [protein per meal](#protein-per-meal) check helps with: aim for most meals to reach your per-meal amount.

#### Around exercise

*Search terms: workout, gym, after exercise, resistance training.*

- **After resistance exercise** (weights, bodyweight strength work): protein "immediately to 2 hours" afterwards strongly stimulates muscle building[^70]. But the old idea of a narrow "anabolic window" — a 30–60-minute window you must not miss — hasn't held up: once total protein is matched, protein eaten within an hour of training shows no clear advantage over protein eaten at other times[^71]. In practice, having a protein-containing meal within a couple of hours either side of a session covers it.
- **Before exercise**: protein (or protein with carbohydrate) before *or* after training can both support strength gains[^70]; if you train soon after a meal that already contained protein, there's no need for more right after.
- **After endurance exercise** (running, cycling, swimming): the priorities shift. Carbohydrate to refill muscle glycogen comes first, especially if you'll train again within the day; adding protein to it helps repair. When recovery time is short, the [ISSN](#gloss-issn) suggests carbohydrate with 0.2–0.4 g protein per kg per hour[^70]. In trained endurance athletes after a long ride, about 30 g of protein (roughly 0.5 g/kg) gave the maximum muscle-protein response, and more didn't help[^74]. Protein did not, however, increase the building of new mitochondria (the muscle's energy machinery) beyond what carbohydrate alone did — that adaptation comes from the training itself.
- **Does the kind of exercise matter?** Yes, in what you pair protein with and why. After strength work, the goal is muscle building, and protein is the main lever. After long or hard endurance work, refuelling with carbohydrate matters most, with protein supporting repair. For mixed training, a meal with both covers both.

#### Before sleep

*Search terms: bedtime, sleep protein.*

A dose of slowly digested protein before sleep can keep muscle building going overnight. The [ISSN](#gloss-issn) cites about 30–40 g of casein (the main protein in milk; cottage cheese and Greek yogurt are rich in it)[^70]. In young men doing a 12-week resistance program, about 27.5 g of protein each night before sleep led to greater gains in muscle size and strength than a placebo[^75]. Most of this evidence is from young, training men; it's a reasonable option if your evening meal was light on protein, not a requirement.

#### Time of day: is breakfast special?

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

There's emerging evidence that protein early in the day may matter more for muscle than the same protein late in the day, linked to the muscle's own daily (circadian) clock. In mice, protein at the first meal of their active period built more muscle than protein at the last, an effect that vanished in mice with a disrupted muscle clock; and among 60 women aged 65 and over, those who ate a larger share of their protein at breakfast had better muscle function[^76]. The human part of that evidence is observational, so it shows association, not cause. But it points the same way as the distribution advice above: since breakfast is usually the lowest-protein meal, raising it is a good first step.

#### What NuMa shows, and doesn't

*Search terms: timing not tracked, clock time, limitations.*

NuMa's [protein per meal](#protein-per-meal) check tells you which meals reached a worthwhile amount, and how many did each day — the practical heart of the advice above. NuMa doesn't record the time you ate or when you exercised, so it can't check timing around a workout or before sleep. A meal named for its role ("Post-workout", "Bedtime snack") at least lets you see those meals' protein at a glance in the day's per-meal list.

These are guides for keeping and building muscle, not medical advice. If you have kidney disease or another condition that limits protein, follow your clinician's advice.

### AA. Water: from drinks and from food {: #water}

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

NuMa counts the water you take in from everything you log, not just what you drink. (If you'd rather not track water, turn it off in Settings → 9; nothing is deleted, and turning it back on brings it all back.) Fruit and vegetables are mostly water (an apple is about 86%), and so are milk, soup and cooked grains, so food supplies a real share of each day's water.

**Where you see it.** Meal, recipe and day pages show a **Water** row with two rows under it: **Water from drinks** and **Water from food**. The two always add up to the Water total. A single food's page shows only its Water, since one food is either a drink or it isn't. Most branded drinks have no water value, since US labels don't list it; tick **This food is a drink** on one and NuMa estimates it as 100 g minus the drink's protein, carbs and fat, and the food's page says it's an estimate. Water from drinks and Water from food can also be chosen as columns in Meals & Log and Recent Days, and plotted in the [Nutrient Plot](#nutrient-plot). Amounts are in grams; for water, 1 g is 1 mL, so 250 g is a 250 mL glass.

**What counts as a drink.** You decide, with a **This food is a drink** checkbox on each food's page. Recipes have their own **This recipe is a drink** checkbox, and both can be ticked straight from the list on Analysis → Food use in meals. When NuMa first saves a food from [USDA](#gloss-usda), it ticks the box itself if USDA files the food under beverages (tea, coffee, juice, soft drinks, water). It doesn't guess for milk, soup or smoothies, so tick those yourself if you think of them as drinks. Changing the box updates every meal and recipe that uses the food. Ticking it on a food with no water value (true of most branded drinks, since US labels don't list water) fills in an estimate: 100 g minus the food's protein, carbs and fat. The food's page says it's an estimate, and a measured water value is never replaced.

A recipe counts its drink ingredients as drinks and the rest as food: a smoothie made with milk and banana splits its water between the two. Tick **This recipe is a drink** and *all* of its water counts as drinks, including any recipes used inside it.

**The daily goal.**{: #water-reference} The goal is the [Adequate Intake](#gloss-ai) for *total* water from the IOM (US Institute of Medicine, 2004): 3.7 liters a day for men and 2.7 liters for women. It covers drinks and food together, which is why it sits on the Water row rather than on Water from drinks. It's a guide, not a requirement. The figures are simply the typical (median) intakes of healthy Americans, not a measured need, and the Institute itself says intake below them may carry no added risk. European authorities, the European Food Safety Authority (EFSA), working the same way, set 2.5 and 2.0 liters[^84]. You choose whose figures NuMa uses, under **Water goals from** in Settings → 1, Your Profile; the IOM's are the default. Today's goals follow the change at once; earlier days keep theirs unless you apply your profile to them (see [Per-Day Profile Tracking](#day-profile)). Needs rise with heat, exercise, body size and illness.

Going past a water goal gains nothing, so NuMa never shows it as a success: below the goal, the percentage is colored like any other minimum, but at or above it the figure is plain, not green.

**A fluid limit from your clinician.** If you've been given one (for heart failure or kidney disease, say), set it as a [maximum limit](#maxlimits) in Settings → Nutrient Targets — on **Water from drinks** if the limit counts what you drink, as heart-failure limits usually do, or on **Water** if it counts everything. With either set, NuMa stops nudging you to drink more: the water goals lose their color, the warning about older people's drinks (see [Water and older people](#water-older)) goes, and so do both notes described next and under *Protein and water*.

**A weight-based figure, for comparison.**{: #water-weight} Neither the IOM nor EFSA scales its figures to body weight. The one weight-based figure in common use comes from NICE (the UK's National Institute for Health and Care Excellence): for adults in hospital on a drip, routine maintenance starts at 25–30 mL of water per kg of body weight a day, capped at about 3 liters, using ideal body weight rather than actual weight for people with obesity[^85]. A day's page shows what that comes to for you, under the Water rows, for comparison only. NuMa uses your profile's weight, or, if your body mass index (BMI) is 30 or more, an ideal body weight worked out from your height (the Devine formula). It is a figure for patients lying still in bed, not a goal for healthy people, and a per-kilogram rule misleads at both ends: a larger body needs only about 0.7 liters more water a day per extra 50 kg, so it overstates the need of heavier people and understates that of lighter ones. At 60 kg it gives only 1.5–1.8 liters, below both the IOM and EFSA goals, and the note says so whenever that happens; your goal stays the one you chose.

**A goal for drinks, too.** The Water from drinks row has a goal of its own: the drinks part of the IOM's total-water figures, 3.0 liters a day for men and 2.2 for women (the rest comes from food)[^77]. With EFSA's figures chosen, it's 2.0 and 1.6 liters, 80% of the total[^84]. From age 65, a day's page also warns you when that day's drinks come to less than the minimum recommended for older people. That minimum is a floor under the goal, not a lower goal; see [Water and older people](#water-older) below.

**What counts as water.** Coffee, tea, and beer or other dilute alcoholic drinks hydrate about as well as water: their mild diuretic effect is short-lived, and the Institute of Medicine counts them toward total water. Milk and juice are 85–90% water and count in full. Food's share of the day's water is shown beside **Water from food** (for example "23% of the total"). It's about a fifth on a typical diet, and much more on one rich in fruit, vegetables and soups.

**Protein and water.** Breaking protein down makes urea, which the kidneys clear in urine, so a high-protein diet raises the water your body has to pass. NuMa doesn't change the goal for it, but if you're eating well above the protein target, it's a reason not to run low on drinks. A day's page says so, under the Water rows, when that day's protein comes to one and a half times your protein goal or more (a judgment, not a figure from research). How much it adds is worked out under [Water and older people](#water-older).

**Gaps in the data.**{: #water-gaps} NuMa began recording water in October 2026. Foods you saved before then have no water value yet and show "no data". That makes a day's water total too low, never wrong in any other way. To fill them in:

- For all your USDA foods at once, go to Foods → 9, *Missing nutrient data*, and click **Fill in water for N USDA foods from USDA**. NuMa fetches only the water value, adds it only where a food has none, and changes nothing else; a few hundred foods take well under a minute. If it stops partway (USDA busy, or no internet), click it again and it carries on from where it stopped. A food USDA has no water value for is named afterwards; that's usual for branded (packaged) foods, because food labels don't list water. For those, click **Show these foods in the list below**: it turns on the Water column in the *Missing nutrient data* list (it stays on) and takes you there, where each food has **ask AI** and **not needed** boxes.
- For one food at a time, click **Find this data** beside it in the list of foods with no data under [Top Contributors](#top-contributors) (rank by Water), or **Fill in nutrients from another food** on its page, and copy the water value from a matching food in USDA or one of the other food tables ([which to try first](#key-sources)).
- For any other food, tick the **Water** group in that same section and ask Claude AI for the missing values (see [Checking your data](#checking-your-data)).

USDA, the Canadian Nutrient File and the UK, Australian and French tables bundled with NuMa all report water (the French table for most of its foods, not all). Most Open Food Facts products don't, since food labels don't list it.

#### A wet food picked for a dry one {: #water-wet-dry}

*Search terms: wrong food record, dry vs wet, water percentage.*

Water also shows when a food is the wrong record. The same food can come wet or dry, and a name doesn't always say which. [USDA](#gloss-usda)'s okara, for instance, is the wet pulp left from making soy milk, about 82% water. Okara *flour* is about 8% water, and has about five times the protein and calories. Pick the wet one for a recipe that uses flour, and every value from it is several times too low.

So when a food's name, or the name you gave it in a recipe or meal, says it's dry (*flour*, *powder*, *dried*, *dehydrated*, *dry*) but the food's data is over 40% water, NuMa marks it with a yellow **"82% water — but named flour?"** next to that ingredient or meal item, explains it in a note below the list, and lists every such food on Foods → 9 under **Named dry, but mostly water**, with the recipes and meals using it. Genuinely dried fruit stays under the line (prunes and dried apricots are about 31% water), and names like "prepared with milk", "packed in oil" or "dry white wine" aren't counted as dry. Every other food in a recipe or meal shows its water in gray, "(8% water)", so you can see at a glance which version you used. A food without a water value can't be checked until it has one. 

#### Water and older people {: #water-older}

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

Older people don't need less water than younger adults; if anything, they need to be more careful to get it. NuMa keeps the same goals from the US Institute of Medicine (IOM) at every adult age, for three reasons:

- **Less water from food.** Energy needs fall with age, so most older people eat less, and with less food comes less of the fifth or so of daily water that food usually supplies[^77]. More of it has to come from drinks.
- **Kidneys that save less water.** With age the kidneys become less able to concentrate urine, so the same waste takes more water to clear. In healthy men kept without water for 12 hours, the most concentrated urine the oldest group could make was roughly a fifth weaker than the youngest group's[^80]. Water-loss dehydration becomes correspondingly more common with age[^82].
- **More protein, more urea.** Older people are advised to eat more protein, not less: at least 1.0–1.2 g per kg of body weight a day from 65, against 0.8 g for younger adults ([PROT-AGE](#gloss-prot-age)[^67]). Each gram of protein leaves about 5.7 milliosmoles of urea for the kidneys to clear (its nitrogen, about 16% of its weight, divided by 28)[^83]. Going from 60 to 100 g of protein a day adds about 230 milliosmoles; at the urine concentration an older kidney can manage, that's roughly a quarter of a liter more urine a day at the least. That's a modest amount, but it points up, not down.

On top of all three, **thirst fades with age.** In one study, healthy men aged 67 to 75 kept without water for 24 hours felt less thirsty and drank less afterwards than young men did, so their blood stayed more concentrated[^81]. About one older adult in four living at home is mildly dehydrated from drinking too little[^79].

That last point is why a floor exists. ESPEN (the European Society for Clinical Nutrition and Metabolism) recommends that older people be offered **at least 1.6 liters of drinks a day for women and 2.0 liters for men**, unless a medical condition calls for otherwise[^78]. That is a minimum aimed at the many who drink far too little, not an estimate of what older people need, so NuMa doesn't use it as the goal. From age 65 it's a warning instead: when a day's drinks come to less than it, the day's Water from drinks row says so. If a clinician has given you a fluid limit, follow that instead, and set it as a [maximum limit](#maxlimits).


## Part 5 — Reading Your Results

*(Reading time: 1 hour, 21 minutes)*

This part explains what the columns, tables, and analysis screens mean.

### A. Getting help {: #help}

*Search terms: learn more links, support, where to find help.*

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
- [Replace a food or recipe everywhere (substitute)](#fooduse-substitute) — bulk-replace one food/recipe with another
- [What-if: meals](#whatif) — see how removing, adding or replacing foods would change your daily nutrition
- [What-if: recipes](#whatif-recipes) — see how changing an ingredient would change each recipe per serving
- [Saving, downloading and applying a what-if](#whatif-apply) — keep a scenario by name, download it as a spreadsheet file, or make its replacements for real
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

*Search terms: Food Cache columns, column meanings, food list columns.*

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

*Search terms: hide food, unarchive, hidden items.*

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

*Search terms: nutrient table, nutrition facts, nutrients list.*

Shows the nutritional content of a food, recipe, or meal portion, grouped by category (Macronutrients, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients)).

Columns:

    Nutrient     Name of the nutrient.
    Amount       Value for the portion you entered.
    Unit         kcal for calories; g for macronutrients (protein, fat,
                 carbs, fiber, omega fatty acids); mg or mcg for minerals
                 and vitamins.

**Every nutrient NuMa tracks gets a row, and "0" and "no data" mean different things.** **0** means the food's source measured it and found none (or, for a recipe or meal, that every ingredient reporting it has none). **no data** means nothing was ever recorded — the source didn't measure it, so the true amount is unknown, not zero. A meal or recipe shows a figure as soon as any of its ingredients has one, so a total can still be an underestimate when some ingredients have no data; [Missing nutrient data](#data-completeness) on Foods → 9 lists the foods with whole groups missing. Small amounts keep their decimals (0.3 mg, 0.04 mcg) rather than rounding down to a misleading 0.

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

If you have set a Revised Optimal target for any nutrient (Settings → 5. Nutrient Targets - Researched) — a higher daily goal of your own, for a nutrient where more recent research recommends more than the standard [RDA](#gloss-rda) — the table gains extra columns for it: **Revised Optimal goal**, plus the matching percentage columns (**% of Revised Optimal**, or **Rev. Opt. meal %** and **Rev. Opt. day %** on a meal). Nutrients you have not set one for show a dash ("–") in those columns. A note under the table explains them too. See [Revised Optimal Targets](#optimal) for details.

If you have configured a custom max limit for a nutrient, its row is highlighted (orange, then red) once today's total is within 10% of that limit. See [Maximum Nutrient Limits](#maxlimits) for details.

[Phytonutrients](#gloss-phytonutrients) (carotenoids, choline, isoflavones, etc.) appear only when [USDA](#gloss-usda) data for that food includes those values -- many foods have none. Amino acids are not in this table; see the Protein Quality section below it.

See [daily nutrient goals](#goals) to see how your daily goals are calculated. See [RDA](#rda) to see the Daily Intake vs. Recommended Values table.


#### Top Contributors Table {: #top-contributors}

*Search terms: which foods supply, biggest sources, main sources, ranking foods.*

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

**Recipes kept whole.**{: #contrib-by-item} On a meal page with a recipe in it, a second table, **By meal item, recipes kept whole**, sits under the first (which is then headed **By food, recipes split into their foods**; both headings are listed under Top Contributors in the page's contents sidebar) and ranks the meal's items as you logged them: each recipe is one row, linked to the recipe, and each food eaten on its own is another. It answers "was it the dal or the tofu?" where the first table answers "was it the lentils or the spinach?". It follows the same **Rank by** and **Show** choices. For **Protein**, a recipe's figure is its own standalone [DCP](#gloss-dcp): its foods pooled as if the recipe were the whole meal, so the recipe gets the benefit of its own protein complementarity and can score more than its foods' figures added up. For **Glycemic load**, a recipe's figure is the sum of its foods' (only foods with a [GI](#gloss-gi) count). A meal with no recipe in it shows only the first table, since the two would be the same.

A food logged more than once in the same meal — eaten twice on its own, or appearing both directly and inside a recipe in that meal — is grouped into a single row with its amounts summed, rather than listed as separate duplicate rows. This applies on both the per-meal page and the day-level Analysis rollup.

Ranking by **Protein** is special: instead of raw protein grams, it ranks each food by its own standalone [digestible complete protein](#dcp) ([DCP](#gloss-dcp)) — what that food alone would contribute after accounting for amino acid digestibility and completeness, using the same [DIAAS](#diaas) math as Protein Summary above it, applied to that one food in isolation. A note below the table explains this distinction and links back to Protein Summary. Because combining foods can raise a meal's *actual* DCP above what any single food scores alone — [protein complementarity](#comp) is the whole point of [DIAAS](#gloss-diaas) — this table's total will typically be lower than, and should not be read as equal to, the real meal DCP shown in Protein Summary. Foods with no amino acid data on file don't score a DCP and are omitted from the ranking when Protein is selected.


Ranking by **Glycemic load (GI × carbs)** (listed under Macronutrients, below Carbohydrate) ranks the foods by their [glycemic load](#gl): each food's [GI](#gloss-gi) times its carbohydrate grams, divided by 100, for the amount used. Each row shows the food's [GI](#gloss-gi) and how many grams of it are in the meal or recipe. Unlike protein quality, [GL](#gloss-gl) adds up, so these rows total the meal's or recipe's [GL](#gloss-gl). On a recipe, foods inside sub-recipes are listed individually, since a [GI](#gloss-gi) belongs to a food. Foods with carbohydrate but no [GI](#gloss-gi) can't be ranked; they're named underneath, each linked to its Annotate page so you can [look one up](#gi-source-para), with how much of the carbohydrate the ranking covers. The **Which foods drive it, and lower-GI swaps to try** link under a meal's or recipe's Glycemic Load figure opens this view directly.

**Foods with no data for the nutrient.** A food with no figure for the nutrient you ranked by can't be ranked, and adds nothing to the total. Under the table, **Show the N foods with no data for …** opens a second table listing them, heaviest first, with the amount used, so you can see what the total may be missing. No data is not the same as a stored zero: a food whose data says 0 counts as data, and isn't listed. When ranking by Protein (DCP), the list is the foods with protein but no amino acid data. Glycemic load already names its foods with no GI, so it has no such list. On a recipe's page the list goes down to the individual foods, even inside a sub-recipe.

**Getting the missing data.**{: #contrib-find-data} Beside each food in that list, **Find this data** (for DCP, **Find amino acid data**) opens **Fill in nutrients from another food** already searching for the food's own name, in [USDA](#gloss-usda), the other food tables and your Food Cache, with a note naming the nutrient you came for. Pick a match and copy the values the food lacks (see [Refreshing a food, or filling it in from another food](#review-incoming)). A custom food profile opens on its Edit page instead, which has the same search. Under the list, **where to find it** opens that nutrient's entry in [Appendix G](#nutrient-key), which says which sources to try and in what order ([the general order](#key-sources)).

**When the data doesn't exist, or doesn't matter.**{: #contrib-no-data-answers} Not every gap needs filling, so each food in that list also has two one-click answers. Both apply to that food everywhere it's used, not just this meal or recipe, and each brings you back to the list:

- **Has none — record 0** is for a food that truly contains none of the nutrient: no vitamin B12, [EPA](#gloss-epa) or [DHA](#gloss-dha) in a plant food, no lycopene in meat, no vitamin C in an oil. NuMa stores 0 as the food's value, so it leaves the list and counts, as 0, everywhere; meals and recipes using it are updated. When ranking by Protein (DCP), it reads **Has no protein — record 0** and appears only for a food with no protein figure at all — a food *with* protein has amino acids, so for that one use **Find amino acid data**, which copies a similar food's amino acids scaled to this food's protein, as an estimate. Use this button only when you know the answer is none. A guess of 0 for a food that does contain some makes the total too low, just as the blank did, but now without saying so. To change a 0 later, edit the food's values.
- **Not needed for this food** (for DCP, **Amino acids not needed**) is for a gap too small to matter: the iodine in a pinch of spice, the water in a spoonful of oil. The value stays blank and the total is still missing that food's share, but NuMa stops listing the food here, and leaves that nutrient out of any [Claude AI prompt](#fetch). The mark is for that one nutrient, so marking a spice's iodine not needed doesn't hide its missing iron. A whole group marked not needed on Foods → 9 (*Minerals*, say) counts too. Water and amino acids are each one group already, so for them it's the same mark as Foods → 9's.

Foods marked not needed move to a short line under the table, each with an **undo**. The food's own page lists them too, under "No data, marked not needed for this food", with the same **(undo)**.

Which to use, by nutrient: calories never need either button, because NuMa estimates them from protein, carbs and fat as soon as all three are there ([why](#calorie-checks)). Macronutrients, EPA/DHA, vitamin B12, vitamin D and the carotenoids are often truly 0, so **Has none** fits when you know. Minerals, most vitamins, choline, beta-sitosterol and water are rarely truly 0, so prefer **Find this data**, or **Not needed** when the amount used is small. Never record 0 for water unless the food is an oil, sugar or salt.

#### Lower-glycemic swaps {: #gl-swaps}

*Search terms: lower GI swaps, swap foods, alternatives, blood sugar swaps.*

When a meal's or recipe's [glycemic load](#gl) is Medium or High and you rank Top Contributors by glycemic load, NuMa suggests swaps for the one or two foods contributing most. A suggestion is a food in your own Food Cache that:

- has a [GI](#gloss-gi) recorded, at least 5 points lower (published [GI](#gloss-gi) values vary by a few points between tests, so a smaller difference isn't a real improvement);
- has similar carbohydrate per 100 g — within half again either way — so swapping the same weight changes the *kind* of carbohydrate, not how much you eat;
- cuts the [GL](#gloss-gl) by at least 0.5 for the amount used.

Foods that share a word with the original's name come first (brown rice for white rice), then the biggest cut. Each shows its [GI](#gloss-gi) and the [GL](#gloss-gl) it would have at the same weight.

NuMa only knows the numbers. Whether barley belongs in your risotto is your call — so each suggestion has a **see the full effect in What-if** link that opens [What-if](#whatif) with that Replace already filled in, for this meal or recipe (on a meal, also **last 30 days**, across every meal you logged). There you see every nutrient before and after — fiber, protein, calories, not just [GL](#gloss-gl) — and nothing changes until you choose to apply it. See [Glycemic load in a what-if](#whatif-gl).

Suggestions come only from foods you've given a [GI](#gloss-gi), and NuMa says so under them: how many foods that is, and how many foods you use have carbohydrate but no [GI](#gloss-gi), with a link to [that list](#missing-gi) on Foods → 9 so you can add some. If no suggestion qualifies, the same line appears in place of the suggestions.

#### Protein Quality Table {: #protein-quality}
Shows how a food's amino acid profile compares to the [FAO](#gloss-fao) 2013 reference pattern. Appears below the nutrient table when amino acid data is available.

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

A food can have every amino acid met in the food and still be incomplete. Buckwheat is an example: its amino acids are all in the right proportion, but only 79% of its protein is absorbed, so per gram eaten Leucine and Lysine fall short. When that happens, a note under the table explains it. In that case all of the absorbed protein still counts as digestible complete protein. What limits the food is digestibility, not any one amino acid.

See [DIAAS](#diaas) for the [DIAAS](#gloss-diaas) concept. See [limiting amino acid](#gap) to understand what "limiting" means. See [FAO reference values](#fao) for the [FAO](#gloss-fao) reference values used for each amino acid.


#### Meal Protein Digestibility Analysis {: #meal-diaas}

*Search terms: digestibility table, per ingredient protein, absorbed protein.*

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

*Search terms: suffix, estimated digestibility.*

<pre>
    ~est    Estimated from food category average; no measured value for
            this specific food.
    user    You set a custom value (Settings → 4. Protein Digestibility
            Overrides — see <a href="#dcp-overrides">Digestibility overrides</a>).
</pre>

Ingredients contributing less than 1 g of protein are omitted from this table as negligible; the totals row sums only the ingredients shown.

Note: the "Total digestible protein" here is step 1 of a two-step method. Step 2 (the [DIAAS](#gloss-diaas) limiting-amino-acid penalty) reduces it further. See [amino acid scoring](#aa-scoring) for the full step-by-step method. See [DIAAS](#diaas) for background on [DIAAS](#gloss-diaas) and true [ileal digestibility](#gloss-ileal-digestibility).


#### Meal Amino Acid Ratios Table {: #iaa-ratios}

*Search terms: pooled ratios, meal amino acids.*

Step 2 of the meal [DIAAS](#gloss-diaas) calculation. Shows the pooled amino acid supply across the whole meal, expressed as a ratio vs. the [FAO](#gloss-fao) 2013 reference.

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

#### Color coding
    Green    1.0 or above.
    Yellow   0.80-0.99.
    Red      Below 0.80.

The panel below this table shows the final Digestible [Complete Protein](#gloss-complete-protein) figure: total meal protein x the [DIAAS](#gloss-diaas) score.

See [DIAAS](#diaas) for the [DIAAS](#gloss-diaas) concept. See [amino acid scoring](#aa-scoring) for the step-by-step two-stage calculation method. See [digestible complete protein](#dcp) for Digestible [Complete Protein](#gloss-complete-protein).


#### Bioavailability Table {: #bioavailability}

*Search terms: absorption, digestible protein.*

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

#### RECIPE PER SERVING

A recipe's page uses the same per-ingredient table as a meal — Food, Protein (g), Digestibility, Digestible (g), [AA](#gloss-aa) data, [DCP](#gloss-dcp) (g) — figured for one serving; see [Meal Protein Digestibility Analysis](#meal-diaas) for what each column means. A summary below the table shows total digestible protein and the [pooled DIAAS](#gloss-pooled-diaas) score for one serving.

See [DIAAS](#diaas) for [DIAAS](#gloss-diaas) background. See [digestible complete protein](#dcp) for Digestible [Complete Protein](#gloss-complete-protein). See [complement suggestions](#comp) for [complement food](#gloss-complement-food) suggestions.


#### Meals and Log List {: #meals-list}

*Search terms: meals list, meal list columns, sort meals.*

The main Meals & Log screen lists your recent meals, 9 at a time by default, sorted by date (most recent first). Change the sort order — Date, Name, Meal [DCP](#gloss-dcp), Calories, or Glycemic load ([GL](#gloss-gl)) — via the sort dropdown; your choice is remembered as the default the next time you open Meals & Log. A **Number shown** field raises or lowers how many meals are listed, and a **Show meals on or before** date filter narrows the list to a cutoff date — both persist in the page's own controls, not as separate "older/newer" pagination links.

Columns:

    ID              The meal's number.
    Meal            Name you gave the meal (e.g. Breakfast, Lunch).
    Date            Date of the meal (YYYY-MM-DD).
    Complete        Checkmark when you have marked the meal finished
                    (a Mark complete / Mark incomplete button on the meal page).
    Items           Number of foods and recipes logged in this meal.
    Meal DCP        Digestible complete protein for this meal alone (g).
    Day DCP         Sum of DCP for every meal on this date with a computed
                    value — including meals not yet marked complete, since
                    DCP is auto-saved as you add items. If any contributing
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

You can add up to 6 more nutrient columns of your own choosing — see
[Meals & Log columns](#meal-columns). Under each meal's figure in those
columns, a percentage in parentheses — "(23%)" — shows that meal's share
of the day's goal for that nutrient, from the profile the day is scored
against. The figures are plain, not colored: one meal is only part of a
day. A nutrient with no daily goal (sugar, say) shows its figure alone.
Under each day's date, a **current profile** switch scores that day
against your profile as it is now — see [Per-Day Profile Tracking](#day-profile).

[DCP](#gloss-dcp) and Calories values start as -- and are computed on demand.
Opening and analyzing a meal also saves its DCP and calories automatically.

    --    Not yet computed. Use the "Calculate DCP and calories for" dropdown
          and Calculate button to compute for all complete meals, the last 30
          days, or the last 10 days (results are saved permanently).
    n/a   Computed but no amino acid data (DCP) or nutrient data (calories)
          was available.

% of goal requires a user profile (Settings → 1. Your Profile). Blank if no profile is set.

GL is worked out fresh each time the list is shown, so it never needs calculating and is never out of date. Sorting by GL puts the highest first; an incomplete figure sorts by the part that could be counted, and meals with no figure come last. See [Glycemic Load Output](#glycemic) for what the figure means.

Click a meal to view or edit it, or delete it from there. **Search meal history** (type a name or [ID](#gloss-id) in its box on Meals & Log; results open on a separate page) searches every logged food/recipe item by name or ID — no date filter, sort control, or pagination of its own. Pick **Meals that don't contain** in the box beside it to list instead every meal that food or recipe is *not* in. Results show a flat "All Occurrences" table (one row per time that food or recipe was logged, linked to its meal) and a "Summary by Food" table grouping those occurrences by name with times-used count, total grams, and first/last-seen dates. Ingredients inside a logged recipe aren't searched — only the recipe itself, by name.

See [digestible complete protein](#dcp) for a full explanation of digestible [complete protein](#gloss-complete-protein). See [daily nutrient goals](#goals) to see how your daily protein target is calculated.


#### Meals & Log Columns {: #meal-columns}

*Search terms: meal columns, choose columns, nutrient columns.*

The Meals & Log list always shows Calories, plus up to 6 more nutrients you
choose yourself — e.g. Sodium, Fiber, Vitamin D, or any amino acid.

To choose them: Settings -> section 10 "Meals & Log columns". Pick each nutrient's position (1 =
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

*Search terms: foods in a meal, edit meal.*

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

*Search terms: how often, most eaten foods, food usage.*

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

An expandable **Replace, remove or add a food or recipe in these meals**
panel above the results lets you replace one food or recipe with another,
remove one, or add one, across all the meals currently selected — see
[Substituting a Food or Recipe](#fooduse-substitute) and
[Removing or Adding a Food in Many Meals](#fooduse-remove-add).


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
foods. To find one food or recipe in a long table, type part of its name in
**Show only foods and recipes whose name contains**{: #fooduse-recipes-name}
(every word you type has to be in the name; capitals don't matter) and click
**Analyze**. Only the rows shown change: counts and percentages are still
taken over the whole selection, and the heading says how many rows match.
**Clear name filter** shows them all again.

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


#### Replace a Food or Recipe Everywhere (Substitute) {: #fooduse-substitute}

*Search terms: replace food everywhere, swap food, bulk replace.*

To replace one food with another in your meals or recipes — everywhere it was used, in one step — both Food Use in Meals and Food Use in Recipes have a **Substitute a food or
recipe** panel that bulk-replaces every occurrence of one food or recipe
with another, restricted to whatever's currently selected on that page (the
same date range(s) or [ID](#gloss-id) list you searched with).

You can also reach this replacement tool directly from a blocked deletion:
if Food Cache or Custom Food Profiles refuses to delete a food because it's
still used in a recipe or a meal, the "swap it for a different food" link in
that message brings you here with those exact recipes/meals already
selected and the food already filled in as the one to replace — you only
need to pick the replacement.

This is the tool for the common situation where a rename — or re-adding a
food from a search instead of reusing what was already in your cache — has
left what looks like two different foods, when really it's one food you
just want to consolidate under a single, newer entry.

On either Food Use page, after you've searched:

1. In the results table, tick the **Replace** box (on Food Use in Meals,
   **Replace or remove**) beside the food or recipe you want to get rid of. Only one can be ticked at a time — ticking another
   moves the tick. The Substitute panel opens and its "Replace this" box is
   filled in for you.
2. In **Replace it with**, type part of the replacement's name, then click it
   in the list that drops down, or move to it with the up/down arrow keys and
   press **Enter** (Enter alone picks the top one). The list
   covers your Food Cache and your recipes. A line under the button reads
   back what will be replaced with what.
3. Click **Substitute everywhere in this selection** (on Food Use in Meals,
   **Replace everywhere in this selection**) and confirm.

A dash instead of a tick-box means the item can't be reached from this
selection: on Food Use in Meals it was only eaten *inside* a recipe; on Food
Use in Recipes it's only used inside a sub-recipe that isn't itself selected
(add that sub-recipe to the selection, or use the "All recipes" choice). See
below for why. A food you've never added to NuMa won't be in the list; add it
through [Food Search](#food-search) first.

If you'd rather type, the two code boxes take codes directly:

    Replace this         The old item's code (U171477, UD4, R21, OFF3 ...).
    With this /
    Replacement (code)   The replacement's code.

The results table shows what's *currently used* in the selection — the item
you're replacing is marked "replacing this" when you arrive from a blocked
deletion. To find a replacement's code by hand, look it up on
[Food Search](#food-search) or the Recipes list (both open in a new tab from
links right above the form) — each shows the code in its results.

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

**Removing or adding a food in many meals.**{: #fooduse-remove-add} Food Use
in Meals can also take a food or recipe out of every selected meal, or put
one into every selected meal — say, you stopped adding salt to a week of
breakfasts you'd logged by copying, or forgot the nutritional yeast in all of
them. Pick the meals first (narrow them with **Meal IDs** if a date range
would catch meals you don't mean), then, in the panel, choose:

- **Remove from every meal**: tick the food or recipe in the table, then
  click **Remove from every meal in this selection**. Every line of it logged
  straight onto those meals goes; a food eaten inside a recipe stays, for the
  same reason as above.
- **Add to every meal**: type part of its name and pick it from the list,
  then give the **Amount in each meal**, the same way you would on a meal
  page: a food takes grams or a measure (`30 g`, `1/3 c`, `2 oz`); a recipe
  takes servings (`1 serving`, `1 1/2 srv`), a weight or a volume — a bare
  number for a recipe means grams. Click **Add to every meal in this
  selection**. Every selected meal gets one new line, even one that already
  has that food.

**Only some of the days.**{: #fooduse-pick-dates} Each row's **Days used**
count has a **pick dates** link beside it. Click it and the dates that food
or recipe was eaten open below its row, each with the meals it was in; tick
the dates you want (**tick all** and **untick all** help). A replace,
remove or add then reaches only the meals on those dates that the food
appears in — for an add, the new item goes in alongside it — and the panel
says which meals and dates it will touch. Untick every date to go back to
the whole selection. You can tick dates in more than one row; the change
reaches all their meals together.

Both write at once after the confirmation prompt, with no undo. To see first
what the change would do to your nutrition, try it in [What-if](#whatif),
which changes nothing.


#### What-if: Meals {: #whatif}

*Search terms: hypothetical, simulate, try a change.*

Analysis -> What-if: meals shows how your average daily nutrition over a set
of days would change if you ate differently — dropped a food, added a
supplement, swapped one food for another, or ate less of something. Nothing
is saved or changed: your meals stay exactly as logged.

1. **Which meals.** Type dates, one per line: a range
   (`2026-09-01:2026-09-30`) or a single date (`2026-09-03`). Or switch to
   **Meal IDs** to pick particular meals.
2. **What to change.** Each row is one change; add as many as you like with
   **Add another change** and they all apply together. In a food/recipe box,
   type part of a name and pick it from the list with the mouse, or with the
   up/down arrow keys and **Enter** (or type its
   [code](#fooduse), the one shown on Food Search or the Recipes list).
3. **Which days to average over.** Either every day in your selection that
   has a meal logged, or only the days when something you're removing,
   replacing or changing was actually eaten. Say your dates cover 119 days,
   112 of them logged, and the food you're removing was eaten on 47. The
   first choice averages over the 112 days and shows the effect on your
   overall diet. The second averages over the 47 days and shows what those
   particular days would have looked like. **Add** rows don't narrow the
   days, since an addition goes on every day.
4. Click **Show the effect**. Once results are showing, switching the day
   choice redraws them straight away.

The bold line above the results says exactly which days the averages cover,
and how many of them contained what you're changing.

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

To swap one food for another, you have two choices. **Replace** puts the new
food only where the old one was. A **Remove** row plus an **Add** row drops
the old food and adds the new one on every logged day.

What you see:

- A line for each change saying how many meals and days it was found in. A
  change that matched nothing is pointed out, so a typo in a code doesn't go
  unnoticed.
- A small table of calories, protein, Protein ([DCP](#gloss-dcp)),
  carbohydrate, sugars, fat and fiber per day, with rows labeled **Before
  (as logged)**, **After your changes** and **Change**. DCP is worked out
  for each day the same way as on the Daily Summary; if some days lack the
  amino-acid data it needs, a note says how many days it covers.
- A table of every nutrient that changed (a link shows the unchanged ones
  too): before, after, the change, % of your target before and after with
  its status (low / near / met / over, as on the
  [Daily Summary](#goals)), how many days fell short of the target before
  and after, and how many days went over a maximum. An average can look fine
  while several days fall short, which is why the day counts are there.
  **Largest change first** is the default order; **Grouped like the daily
  summary** puts them back in the usual groups.
- A **?** beside a nutrient means something you added has no value for it,
  so the "after" figure may be too low.

Targets come from the profile pinned to each day, as on the Daily Summary.
Days with nothing logged are never counted as zero; they're left out.
Glycemic load isn't recalculated here yet.

On [Food Use in Meals](#fooduse), the **try removing** link on each row opens
this page with that item already entered, for the same meals.

The page address holds the whole scenario, so you can bookmark it and come
back to it later.


#### What-if: Recipes {: #whatif-recipes}

*Search terms: what-if recipes, recipe scenario, change ingredient.*

Analysis -> What-if: recipes is the recipe-book version of
[What-if: Meals](#whatif): it shows how each recipe's nutrition **per
serving** would change if you removed, added, replaced or cut down an
ingredient. Nothing is saved or changed.

1. **Which recipes.** All recipes (the default), recipes created on certain
   dates, or a list of recipe IDs.
2. **What to change.** The same change rows as on What-if: Meals. Remove,
   Replace and Change amount reach the ingredient wherever it's used,
   including inside sub-recipes. **Add** puts an amount into each recipe like
   one more ingredient; choose whether that amount is for **each serving** or
   for **the whole recipe** (then each serving gets its share).
3. Click **Show the effect**.

The number of servings never changes, so removing an ingredient makes each
serving lighter and adding one makes it heavier. That is usually what you
want to know: "if I left the nutritional yeast out, what would one serving
give me?"

To swap one ingredient for another at a different amount — say, pumpkin
seeds in place of hemp seeds at 1.1 times the hemp weight — use a single
**Replace** row: hemp seeds, replaced with pumpkin seeds, **A multiple of the
old weight**, `1.1` (or `110%`). Every recipe gets 1.1 times whatever weight
of hemp it had. No Remove row is needed; Replace takes the old one out.

To use more or less of an ingredient that's already in a recipe, use
**Change amount (multiply: 1.5 or 150%)** with a multiplier, typed either way: 1.5 or
150% for half again as much, 0.5 or 50% for half. It changes the amount wherever the ingredient is used,
including inside sub-recipes. A **Remove** row plus an **Add** row does the
same job when you'd rather state the new amount outright (for example
"10 g per serving"), but remember that Add puts the ingredient into every
selected recipe, not just the ones that already had it.

The results are a grid with one column per recipe. Each cell shows the value
per serving **after** your changes, in bold, with the change below it. Tick
**Also show the before values** to add the old figure. The first column,
**Average change**, gives the average of each recipe's percent change for
that nutrient, over every recipe the change reaches, including any that
don't fit as a column. A recipe that had none of the nutrient before is left
out of that average (a percent change from zero means nothing), and a small
"over N" note shows when that happened. Only nutrients that
change are listed; a link shows the rest. Protein ([DCP](#gloss-dcp)) is
worked out the same way as on the recipe page; NC (not computed) means it
can't be, because an ingredient with 1 g or more of protein has no
amino-acid data.

Only recipes the change actually reaches are shown (with only Add rows,
every selected recipe is). At most 8 fit side by side: the 8 that change
most are shown and the rest are listed by name, so you can pick particular
ones with **Recipe IDs**.

If a changed recipe is used inside other recipes you didn't select, those
are listed under the grid, since they would change too, with a **Show them
too** link that adds them.

On [Food Use in Recipes](#fooduse-recipes), the **try removing** link on
each row opens this page with that ingredient already entered, for the
recipes that use it.


#### Glycemic load in a what-if {: #whatif-gl}

*Search terms: what-if GL, glycemic load before and after.*

Both what-if pages show [glycemic load](#gl) before and after your changes, worked out from the same changed foods as every nutrient, at every depth.

- **What-if: Meals** adds a **Glycemic load** column to the *Average per day* table: the average whole-day [GL](#gloss-gl), over the days that have carbohydrate. A line under the table gives its band on the day scale (Low under 80, Moderate 80–120, High over 120), before and after — and, if you've set a [daily glycemic load target](#gl-target), how many days were over it before and after, each day against its own pinned target.
- **What-if: Recipes** adds a **Glycemic load** row at the end of the Macronutrients rows: [GL](#gloss-gl) per serving for each recipe, with its band on the per-serving scale (Low 10 or below, Medium 11–19, High 20 or above), and "(was …)" when the band changed.

**Watch the coverage.** [GL](#gloss-gl) counts only foods with a [GI](#gloss-gi) value. Swap a food that has one for a food that doesn't, and the "after" figure drops — not because the new food is better, but because NuMa can't count it. So whenever some carbohydrate has no [GI](#gloss-gi), NuMa says how much of it the figure covers, before and after: "It covers 100% of the carbohydrate before and 0% after… the 'after' looks better than it is." The foods with no [GI](#gloss-gi) after the change are named, each linked to its Annotate page, where you can [look one up](#gi-source-para); on the Recipes page, a cell reads **≥** and "covers N% of carbs" (hover it for the foods). Add the missing [GI](#gloss-gi) and run the what-if again for a fair comparison.

A typical use: on What-if: Meals, replace a High-[GI](#gloss-gi) staple you eat often (white rice, say) with a lower one (barley, say) at the same weight, and see what it does to your day's [GL](#gloss-gl) band — and, in the same table, to fiber, protein and everything else.


#### Saving, downloading and applying a what-if {: #whatif-apply}

*Search terms: save scenario, apply changes.*

Once a what-if is showing results, on either What-if page, a bar under the
list of changes offers three things.

- **Save this scenario.** Give it a name and click the button. It appears
  under **Use a saved scenario** at the top of that page (meals and recipes
  each have their own list), where you can open, rename or delete it.
  Opening one brings back everything: the dates or recipes, the changes, and
  how the results were set out. Dates are kept as you typed them, so a
  saved scenario always covers the same days.
- **Download CSV.** The results as a CSV (comma-separated values) spreadsheet file: the changes, then
  every nutrient, including the unchanged ones. From What-if: Recipes, it
  has a column group for *every* recipe the change reaches, not only the 8
  shown on the page.
- **Apply these replacements for real…** This changes your actual meals or
  recipes, so it's only offered when doing it for real gives the same result
  you're looking at. That means every change is a **Replace**: a food for a
  food at the same weight, or a recipe for a recipe at the same servings,
  and no change replaces something with an item another change is
  replacing. If that isn't so, the bar says why instead.

Clicking it doesn't change anything yet. A page first lists what will
change: for each replacement, the meals or recipes it will be made in.
It also says where the old item will stay. On What-if: Meals, a food used
inside a recipe is left alone, because changing the recipe would change it
in every meal that uses it; use What-if: Recipes for that. On What-if:
Recipes, a recipe that has the old food only inside a sub-recipe changes
only if that sub-recipe is one of the ones listed. Click **Yes, make these
replacements** to go ahead, or go back. This is the same substitution as the
Replace box on [Food Use in Meals](#fooduse) and
[Food Use in Recipes](#fooduse-recipes). Every recipe changed has its
Protein ([DCP](#gloss-dcp)) worked out again.


#### Glycemic Load Output {: #glycemic}

*Search terms: GL bands, GL figure.*

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

**Where you see it:** a food's page shows [GL](#gloss-gl) per 100 g and for the portion you're analyzing; a recipe's page, for one serving (or however many servings you ask for); a meal's page, for the whole meal; and a day's pages, for the whole day.

**The day so far.** Under the title of a meal's page, a line gives that day's [GL](#gloss-gl) up to and including this meal — "Glycemic load for 2026-10-13 up to and including this meal (2 of 3 meals): 30.6" — counting the day's meals in the order you created them. The day's own page gives the whole day so far the same way. If you've set a daily target, the line says what share of it you've reached. "≥" means some foods have no [GI](#gloss-gi), so the true figure is higher.

To hide glycemic load everywhere, untick **Show glycemic load** in Settings → 8. A recipe's [GL](#gloss-gl) is worked out from its ingredients, including any recipes used inside it, so it changes as soon as an ingredient or a [GI](#gloss-gi) value does.

**When a figure reads "at least 14.2 — incomplete, missing GI data",** some foods in it have carbohydrate but no [GI](#gloss-gi) value, so their share couldn't be counted. The number is the [GL](#gloss-gl) of everything that *could* be counted, so the true figure is higher. A line says how much of the carbohydrate the figure does cover — "GL covers 72% of the carbohydrate here (28 of 39 g)" — so you can tell a nearly complete figure from a rough one; foods marked "don't prompt me" are left out of that share. The foods left out are listed underneath, each with the reason:

- **no GI recorded yet** — with an **add a GI** link to that food's Annotate page.
- **no GI (marked "don't prompt me")** — you've told NuMa not to ask for this food's [GI](#gloss-gi), or turned GI off in Settings. It still can't be counted, so the figure is still incomplete; **add one anyway** is there if you change your mind.
- **this food has no nutrient data** — NuMa can't tell how much carbohydrate it has.

A band (Low, Medium, High) is shown only for a complete figure, since the missing foods could move it — except when the incomplete figure is already High, which the missing foods can only push higher. If none of the foods with carbohydrate has a [GI](#gloss-gi), the output reads **Not available** and lists them.

**Foods with almost no carbohydrate don't need a GI.** A food with under 1 g of carbohydrate in the amount used (meat, eggs, oil, a pinch of spice) counts as zero, since its [GL](#gloss-gl) could be at most 1 whatever its [GI](#gloss-gi). So a recipe isn't marked incomplete because the salt has no [GI](#gloss-gi). This is the same rule [DCP](#gloss-dcp) uses for foods with under 1 g of protein and no amino acid data.

[GL](#gloss-gl) = ([GI](#gloss-gi) x grams of available carbohydrate) / 100 per ingredient, summed across all ingredients in the meal.

**Which carbohydrate counts.** [GI](#gloss-gi) is measured on *available* carbohydrate, the part your body digests into glucose, so fiber is left out. [USDA](#gloss-usda) and the Canadian table give total carbohydrate, fiber included, so NuMa takes the fiber off. It does the same for Open Food Facts products and foods you entered yourself, since those mostly come from US labels, which also count fiber in. The UK, Australian and French tables already leave fiber out, so their figure is used as it is. For a high-fiber food the difference is large: beans with 60 g carbohydrate and 34 g fiber per 100 g have 26 g available. (An Open Food Facts product from Europe already leaves fiber out, and the label doesn't say which kind it is, so for such a product NuMa's figure runs low by its fiber.)

Below the [GL](#gloss-gl) figure, a meal, recipe or day also gets an [estimated GI](#mixture-gi).

[GL](#gloss-gl) is shown for reference only and does not affect protein quality scores. See [glycemic load](#gl) for a full explanation of glycemic load and its limitations. See [glycemic index](#gi) for background on the glycemic index.


#### Estimated GI of a meal or recipe {: #mixture-gi}

*Search terms: meal GI, recipe GI, mixed meal GI.*

A meal, a recipe and a whole day each get an estimated [GI](#gloss-gi), shown under the [GL](#gloss-gl) figure. It is each food's own [GI](#gloss-gi), averaged according to how much carbohydrate each food brings:

    GI = sum of (food's GI x its carbohydrate) / total carbohydrate

So a meal of 40 g carbohydrate from sugar (GI 65) and 15 g from milk (GI 39) comes out at about 58. It is the same arithmetic as [GL](#gloss-gl) run the other way: 100 x [GL](#gloss-gl) / carbohydrate. A single food's page shows that food's own [GI](#gloss-gi) instead.

It is read on the usual [GI](#gloss-gi) scale: Low 55 or under, Medium 56–69, High 70 or more. A figure within 5 of a boundary is shown as close to the next band ("Medium, close to Low"). The estimate isn't precise enough to treat 54 and 57 as different.

**It's an estimate of what's in the food, not a measured blood-sugar response.** It's the standard way of working out a meal's [GI](#gloss-gi), and studies disagree on how well it works. One found that table [GI](#gloss-gi) values did predict the response to mixed breakfasts[^91]. Another found no connection at all for meals that differed a lot in fat and energy[^92]. A third measured three meals and found the calculation came out 22–50% higher than the [GI](#gloss-gi) actually measured[^94]. Fat, protein and fiber eaten with the carbohydrate slow its absorption, and the calculation can't see that (see [glycemic load](#gl) for why).

The estimate comes with these conditions:

- **Only foods with a GI count.** If some foods have carbohydrate but no [GI](#gloss-gi), the estimate describes the rest and says so: "GI of the 72% of carbohydrate with a GI value". Unlike [GL](#gloss-gl), it isn't a lower limit. The missing foods could push it either way.
- **Not given under 10 g of carbohydrate.** [GI](#gloss-gi) is measured with 25 or 50 g of carbohydrate. With much less, the same person's response to the same food varies a lot from one test to the next: in one study the variation was about twice as large with 5 g of carbohydrate as with 20 g[^95]. So for a cup of coffee with a teaspoon of sugar and a splash of milk (about 5.5 g), NuMa gives the [GL](#gloss-gl) (about 3) but no [GI](#gloss-gi), and says why.
- **Ingredients that may not be eaten as listed.** In a recipe, an ingredient whose name says it is raw, dry, uncooked or a flour is flagged if its [GI](#gloss-gi) counts. Cooking, baking and grinding change how fast starch is digested: flour, water and yeast don't have the [GI](#gloss-gi) of bread. If the [GI](#gloss-gi) you gave such an ingredient was for the form you eat, or the ingredient really is eaten as listed (raw fruit in a smoothie), click **These ingredients are eaten as listed — stop flagging them** on the recipe's page. **Flag uncooked ingredients again** turns the flag back on. The switch covers that recipe's own ingredients, not those of recipes used inside it, which have their own. A meal or day containing the recipe names the flagged ingredient and the recipe it's in, linked so you can get to the switch. Matching on names is rough. Dried fruit ("Apricots, dried, uncooked") is left out, since it's eaten as it is, but a branded food whose name doesn't say it is dry (a bag of small red beans, named just that) isn't caught.
- **Values measured in people with diabetes.** The same note as for [GL](#gloss-gl) names any food whose [GI](#gloss-gi) was measured in people with impaired glucose tolerance or diabetes. See [GI populations](#gi-populations).

A day's estimated [GI](#gloss-gi) is what research calls a *dietary GI*: the [GI](#gloss-gi) of everything you ate that day, weighted the same way.


#### Meal History Tables {: #meal-history}

*Search terms: past meals, search history, exclude, absent, never eaten.*

These tables appear when you type a name or [ID](#gloss-id) in the **Search meal history** box on the Meals & Log list and press Enter or the button. The ID can be a [code](#search-by-code) such as **U171477** or **[R21](#gloss-code)**, or a cached food's [FDC ID](#gloss-fdc-id) number on its own. With **Meals that contain** picked (the usual), you get the two tables below. With **Meals that don't contain** picked, you get one table instead, *Meals without ...*: every logged meal that food or recipe isn't in, with the meal's number, date, name and number of items.

#### MEAL HISTORY -- OCCURRENCES
Every time a food or recipe appeared in any logged meal.

    ID          The meal's number.
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

Note: only foods and recipes logged directly as meal items appear here. Ingredients inside a logged recipe are not individually searchable, so a meal that holds a recipe made with the food still counts as a meal that doesn't contain it.


#### Missing Amino Acid Profiles {: #missing-aa}

*Search terms: missing amino acids, no AA data, excluded ingredients.*

*One of NuMa's data checks — see [Checking your data](#checking-your-data) for the rest.*

When a meal contains ingredients without amino acid data, NuMa cannot include them in the [pooled DIAAS](#gloss-pooled-diaas) calculation. This section lists the affected ingredients and describes your options.

NuMa distinguishes two cases:

Standalone meal ingredients: foods logged directly in the meal.

    The meal's Refresh from USDA button fetches amino acid data for
    these where USDA has it. Otherwise, replace the food with a USDA
    Foundation or SR Legacy equivalent that has amino acid data.

Inside a recipe: ingredients that are part of a recipe you logged.

    These must be fixed by editing that recipe (Recipes → the recipe →
    Edit) and replacing the problematic ingredient there.

It's safe to ignore when the affected food contributes negligible protein (garnish, spice, a small amount of fruit). It matters more when the food is a significant protein source in your meal. Foods contributing less than 1 g of protein are treated as negligible and left off this list entirely (a footnote tells you when items were omitted this way).

**Turning this check off for a food.**{: #missing-aa-off} Some foods carry a little protein that doesn't matter for protein quality — a supplement, a seasoning blend, a food you eat for something else entirely. To stop NuMa listing one here, click **Amino acids not needed for this food — stop listing it** beside its name. NuMa marks the food's amino acids "not needed", the same mark as the **not needed** box on Foods → 9, so it also drops off that page's list of foods with no amino acid data and out of Claude AI prompts. It applies everywhere the food is used, not just this meal or recipe; a short line under the list counts the foods hidden this way. The food is still left out of the [DIAAS](#gloss-diaas) calculation — the mark stops the warning, it doesn't supply data. To undo it, open the food's own page and click **(undo)** beside *Amino Acids* under "Marked not needed for this food". The button works for a food inside a recipe too, since the mark belongs to the food.

The [DIAAS](#gloss-diaas) calculation runs on whichever ingredients do have [AA](#gloss-aa) data. The result is flagged as an estimate, and the [DCP](#gloss-dcp) figure reflects only the protein from data-complete ingredients.

See [meal protein digestibility](#meal-diaas) to see the digestibility table. See [DIAAS](#diaas) for [DIAAS](#gloss-diaas) background.


#### Recipes List Table {: #recipes}

*Search terms: recipe list, recipes table, recipe columns.*

Shows all your saved recipes. Sorted by Last accessed by default; use the sort dropdown (not available while a search filter is active) to switch to Name or [DCP](#gloss-dcp)/serving instead. Your choice is remembered as the default the next time you browse recipes.

Columns:

    Compare     Tick to compare recipes side by side (see Compare selected).
    Code        The recipe's code (R21).
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
Shows the current ingredients in a recipe, on its page and on Edit Recipe. Refreshes after each change so you can see the current state.

Columns:

    #       Row number. On Edit Recipe, each row also has up/down, Edit
            and Remove controls.
    Amount  Portion entered: e.g. "175 g", "14.7 g (2 T)", "2 servings".
    Food    Ingredient name, followed by its code (U171477, UD4, R21 for
            an ingredient that is itself a saved recipe, and so on —
            see code in the Glossary).
    Notes   Your note for that ingredient, if any.

Nested recipes (a code starting with R) have their nutrients scaled automatically from their recorded serving count and total weight. Note that a nested recipe's Amount here is always a plain serving count, never a `pN` shortcut — see [Recipes: servings instead of `pN`](#portions-vs-servings) for why recipes and foods work differently here.

**Unsaved recipe-details edits and adding an ingredient.** The Recipe details fields (name, servings, instructions, etc.) at the top of the Edit Recipe page save separately from the ingredient list — clicking "Add to recipe" doesn't normally touch them. If you've changed one of those fields without clicking "Save recipe details" yet and then add an ingredient, a warning appears: adding the ingredient will save those pending changes for you rather than silently discard them. Choose Cancel to go back and finish editing those fields first, or Continue to save them and add the ingredient in one step.

**Adding a recipe as an ingredient, by servings or grams.**{: #subrecipe-amount} A recipe that turns up in the ingredient search can be added to the one you're editing like any food. Type how much in servings, or switch the box beside the amount to **grams**; NuMa turns grams into servings using that recipe's serving weight, shown in the row ("1 serving = 1 cup, 240 g"). The grams choice appears only for a recipe whose serving weight NuMa knows: it has a total weight entered, or every one of its ingredients has a weight. The ingredient is always saved as a number of servings, so that's what the ingredient list shows afterward.


#### USDA Food Search Results {: #food-search}

*Search terms: results columns, AA checkmark.*

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
    Recipes, Pantry, Cache,         Same match-quality ranking, but when two
      then Other                    or more results are tied on how well they
                                    matched your search, your own Recipe,
                                    then Pantry, then Cache entries sort
                                    ahead of USDA/OFF/other external results
                                    within that tie. It never lets a weaker
                                    match from your own data outrank a
                                    stronger external match.
</pre>

Both modes group your own matches under their own heading above a divider, with external results below. Within your own matches, **recipes always come first**, then Pantry and Food Cache foods, each in best-match order. Your own matches are always listed before online ones, so a food or recipe you already have is never buried under a wall of online results.

See [Ordering food search results](#search-ranking) in Part 6 for the full explanation.

**Source filter.** A row of checkboxes next to the search box itself — visible before you've even typed a query, not just after results come back — narrows the list to any combination of sources you check: Pantry, Food Cache, Recipes, [USDA](#gloss-usda) FoodData Central, Open Food Facts, Canadian Nutrient File, CoFID, AFCD, CIQUAL (USDA and Open Food Facts, the two most-used external sources, lead the external group). Check as many as you like; unchecking every box is treated the same as checking them all, since a filter that hides everything isn't useful. Each checkbox is labeled with the short badge used elsewhere plus its full name (e.g. "USDA — USDA FoodData Central") and re-runs the search the moment you check or uncheck it. A **Select all sources** button re-checks every box in one click. A **What are these sources? →** link next to the "Source" label jumps to [Food data — where it comes from and how it is stored](#food-data). Your choice is sticky across every search box that has this filter, the same way the sort-order choice is. It appears next to every food search in the app: the standalone Foods → Search page, Analyze a Food Portion, Convert a Portion, Comparison, My Pantry's "Add a food" search, the Meals & Log "Add Food or Recipe" panel, a recipe's ingredient search, and the two "copy from another food" searches on the Edit Custom Profile page.

**"Did you mean" suggestions on a search with no results.**{: #search-suggestions} Every one of those same search boxes offers likely corrections right next to a "No results" message — e.g. searching "brocoli" suggests **broccoli**. Click a suggestion to re-run the search with it, or press Esc to dismiss the suggestions and keep what you typed. This works fully offline: it checks your own previously searched/cached foods, pantry items, and recipes first, then the food names bundled with the CoFID/[AFCD](#gloss-afcd)/CIQUAL [databases](#gloss-database) — it can't invent a suggestion for a brand name it's never encountered anywhere. It also appears on searches that don't have a Source filter, since they only ever look at your own cached data: [Food Cache](#food-cache-web), [Annotate](#annotate), [Recipes](#recipes-menu-web), [Search meal history](#meal-history), and Custom food profiles' "copy a cached food as a draft" search.

**Omitted-source warning.** Because the Source filter is sticky, a box unchecked once (even by accident, or while narrowing down a different search) stays unchecked everywhere until you re-check it — silently, with no visual difference from a normal search. If that hides a food you expected to see, it can look exactly like a search or ranking bug rather than a filter setting. On the Foods search page and the Meals & Log "Add Food or Recipe" panel, whenever one or more sources are unchecked, a small red note appears next to the Sort by control — **Omitted from search: RECIPE**, for example — naming exactly which ones. Check the Source filter row below to bring them back.

While a live [database](#gloss-database) (USDA, Open Food Facts, or Canadian Nutrient File) is being searched, a red **Online search in progress…** note shows, so a few seconds' wait doesn't look like NuMa has stalled. It appears on every page that searches online: near the result count where your own matches show first, or beside the Search button on pages that show nothing until the online results are in. Hover over it to see which sources it's contacting. If you've unchecked all three, the note (and the network requests behind it) doesn't appear at all. CoFID, AFCD, and [CIQUAL](#gloss-ciqual) are different: each is a bundled dataset, not a live lookup, so their results appear instantly alongside your own Pantry/Cache/Recipe matches — checking or unchecking any of them never triggers a network wait.

**Result limit.** A "Show up to ___ search results" box next to the Source filter controls how many results are fetched and shown, per source (default 25, up to 500). Type a number and press Enter or click Search to apply it — like the Source filter, your choice is remembered as the default for next time.

See [Food Cache](#cached) for the [Food Cache](#gloss-food-cache) column guide. See [Food Cache](#food-cache-web) to learn how to get missing amino acid data via Claude [AI](#gloss-ai).


#### Comparison Tables {: #comparison}

*Search terms: versus, vs, difference between foods.*

Shows up to eight foods and/or recipes side-by-side, mixed in any combination, in up to four tables: an ingredient table, a protein-quality table, a glycemic table, and a nutrient table. By default every comparison is per 100 g of each item — a food's natural unit (grams) and a recipe's (servings) aren't otherwise a comparable amount to judge side by side, so the page starts every item on the same 100 g footing. You can also set your own amount for each item (see below). To start a new list, click **Clear the list and start over**, beside the Search button (your saved lists are not affected). Once there is something to compare, a **Contents** list down the side of the page jumps to each part: the search, the items being compared, Compare amounts, each comparison table, and Save this list.

**Gathering items from several searches.**{: #comparison-gather} Search for one food, tick it, then simply search for the next one: whatever you ticked is added to the comparison before the new search runs, so nothing you picked is lost. (**Add selected to comparison** does the same without searching again.) Everything added so far is listed under the search, each with a **Remove** button.

**Setting an amount for each item.**{: #comparison-amounts} Each item in that list has an **Amount** box: grams for a food, servings for a recipe. A recipe that has a weight per serving (its own total weight, or one NuMa can add up from its ingredients) also has a **servings / g** choice beside the box, and shows "1 serving = … g" underneath (with the recipe's serving description, such as "1 serving = 1 muffin (85 g)", when it has one — that description also appears under the recipe's name in the nutrient table whenever servings are being compared), so you can give it in grams instead; its column then reads, for example, "100 g (0.97 servings)". A recipe with no weight per serving takes servings only. A food that has portions ("1 slice (28 g)") has a **g / portion** choice beside its box too, so you can set it as a number of one of its portions — 2 × 1 slice — and its column reads "2 × 1 slice (56 g)". Fill in the amounts you want, then click **Show comparison at the amounts set above** (or press Enter in an Amount box). Of the two Show comparison buttons, the blue one is the one that matches what you've asked for: **Show comparison for 100 g of each item** until you type an amount, then the amounts one. Every table then shows each item at its own amount — 30 g of almonds beside 150 g of yogurt and 2 servings of your granola, say — and the **Compare amounts** choice switches to **The amount I set for each item**. A box left blank means 100 g of a food or 1 serving of a recipe. Your amounts stay with the comparison as you add or remove items, and are kept when you save it as a list. Switch **Compare amounts** back to per 100 g at any time to see how concentrated each item is instead; your amounts are kept for when you switch back.

**Comparing recipes as written.**{: #comparison-basis} Per 100 g is the default because it puts a food's grams and a recipe's servings on the same footing, and shows how concentrated each item is. But it isn't always what you want: two versions of a recipe, one with a little salsa added, look as if the other ingredients shrank, because each is now a smaller share of 100 g. When a comparison includes a recipe, a **Compare amounts** choice above the tables offers two more ways to see it (as well as [the amount you set for each item](#comparison-amounts)):

- **Per serving of each recipe, as written** — one serving of each recipe: its own ingredient amounts divided by its servings, and the nutrients of that serving.
- **Each whole recipe, as written** — every ingredient exactly as entered in the recipe, with the measure you typed (⅓ c, 2 T) beside its grams, and the whole recipe's nutrients.

Each recipe's column heading says which amount it shows ("1 serving (140 g)", "whole recipe, 1 serving, 177 g"). A plain food has no recipe amounts, so it stays per 100 g in every view. NuMa remembers your choice. Neither view is scaled by the recipe's weight, so the "(estimate)" mark below doesn't apply to them.

**How a recipe's 100 g figure is worked out.**{: #comparison-estimate} A food's per-100g nutrients come straight from its cached data — no estimation involved. A recipe has no single "100 g" anything, so NuMa derives one from the recipe's weight, then scales the recipe's total nutrients — and, for the ingredient table, each ingredient's own amount — by 100 divided by that weight. The weight is the same one a meal uses when you log the recipe by weight:

- **The recipe's own total weight**, when you've entered one on its edit page. This is the weight of the finished dish, so it can allow for cooking loss, water evaporating, and so on. A stew that cooks down from 1,300 g of raw ingredients to 1,000 g is compared per 100 g of the 1,000 g, and its raw ingredients then add up to more than 100 g in the ingredient table.
- **Otherwise, its ingredients added up**: each direct food ingredient contributes its own entered gram amount; a sub-recipe ingredient contributes its weight per serving × how many of those servings this recipe uses — its weight per serving being its *own* recorded total weight ÷ its own servings, or, if it has no recorded total weight, the sum of its own ingredients worked out the same way, however deep the sub-recipes go.

(Until October 18, 2026, Compare always added up the ingredients and ignored a recipe's own total weight, so a recipe with a stated weight could show slightly different figures here than on a meal.)

If a recipe has no total weight and any ingredient's weight can't be determined — a direct ingredient with a blank or zero amount, a sub-recipe that has since been deleted, or a sub-recipe whose servings aren't set or whose own ingredients can't be weighed — that one ingredient is left out of the sum entirely rather than guessed at. The summed weight is then a lower bound, not the true dish weight, so the recipe's 100 g figures run *higher* than they should (the same nutrient total divided by a too-small weight). NuMa marks this by appending "(estimate)" next to that recipe's name everywhere it appears in these tables, so a higher-than-expected number has a visible reason rather than looking like a data error.

The **ingredient table** has one row per distinct ingredient (food or recipe, each with its code) across the items you're comparing, one column per item, showing how much of that ingredient goes into 100 g of the finished item (or "--" if it isn't used, or if a recipe has no total weight and its ingredient weights are incomplete). A food entry shows itself as its own single "ingredient" — always "100 g," by definition. Ingredients shared by two or more items are listed first (highlighted) — that's usually the interesting question when comparing recipes: which ingredients differ, and by how much, per 100 g of the finished dish. A sub-recipe used as an ingredient shows its (rescaled) serving count rather than being expanded into its own raw ingredients.

The **protein-quality table** ([DIAAS](#diaas)-based) appears when at least one item has enough amino acid data to score: composite [DIAAS](#gloss-diaas) score, raw protein, digestible complete protein (DCP), DCP as % of raw protein, and the limiting amino acid — all per 100 g of the item, highest value per row highlighted, "--" for an item without enough data.

The **glycemic table**{: #compare-gl} appears when at least one item has a [GI](#gloss-gi) or a [GL](#gloss-gl) to show: each food's [GI](#gloss-gi) (a recipe has no single [GI](#gloss-gi), so it shows —) and each item's [glycemic load](#gl) per 100 g — [GI](#gloss-gi) × carbohydrate ÷ 100, counting only foods with a [GI](#gloss-gi). Here **lowest** is highlighted, since less is better. A figure missing some foods' [GI](#gloss-gi) reads "≥" with how much of the carbohydrate it covers, and is never highlighted, since its true value is higher. A **†** marks a [GI](#gloss-gi) [measured in people with diabetes](#gi-impaired). Per 100 g suits comparing kinds of food; for what a real portion does, see the meal or recipe page.

The **nutrient table**{: #compare-nutrients} covers every nutrient a food's own nutritional analysis shows — Macronutrients, Water, Omega Fatty Acids, Minerals, Vitamins, [Phytonutrients](#gloss-phytonutrients) — plus Amino Acids, every value per 100 g, highest value per row highlighted in green, sortable by checked nutrients. A nutrient that none of the items has data for gets no row (and a group left with no rows is dropped), and a yellow box above the table names every nutrient left out that way, so a missing row always means "no data", never an oversight. The items you chose are listed above the table — each also shows an **[AA](#gloss-aa)** column indicating at a glance whether it has amino acid data (✓) or not (✗).

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
    GI source        Where the GI value came from. Filled in for you when
                     you pick a value from the lookup; type your own for a
                     value from anywhere else.
    DIAAS estimate   Your protein quality estimate (0.00-2.00). Useful for
                     packaged foods that lack amino acid data in USDA. See
                     <a href="#diaas">DIAAS</a>.
    DIAAS source     Where the DIAAS value came from.
    Prep context     A short preparation note (e.g. "boiled 20 min", "raw").
</pre>

**Note where each value came from.** A source is kept only alongside its value: clear the value and its source goes too. Both appear on the food's page after "Value taken from". If you pick a value from the GI lookup and then type a different number over it, the lookup's citation is cleared, since it no longer describes your number. A source you typed yourself stays.

**Raw or cooked: pick the GI for the form you eat.** A yellow warning under the GI box is there because this mistake is easy to make. Cooking, baking and grinding change GI a great deal: raw wheat flour stirred into water tests around 20, while bread baked from it is 70–90, and the lookup lists both kinds side by side. If the food's name says it is raw, dry, uncooked or a flour, the warning adds that a raw-form GI will make the meals you cook from it look better than they are, so use the GI of what you make from it, or leave the box blank. Recipes flag such ingredients too: see *Ingredients that may not be eaten as listed* under [Glycemic Index](#gi).

**Looking up a GI value instead of typing one.** Open **Look up a GI value from the published reference table** and search it by name. Click anywhere on a result to take its value: the list closes, the GI box fills in, and the **Save annotation** button highlights — the value is not stored until you press it. See [Where GI values come from](#gi) for the table and how to pick a population. If a search finds nothing, the page lists what to try next: plainer words, another name for the food, a similar food's value, or glycemicindex.com.

**There's no lookup for DIAAS**, since published values exist for only a few foods. A note under the box says how to estimate one from the food's main protein source, using [the table in the DIAAS section](#diaas-estimate-table).

**The two "don't prompt me again" checkboxes** are only for deliberately leaving a value blank. Saving a GI or DIAAS estimate already stops NuMa asking about that one, so you do not need to tick anything to make the prompt stop.

**If you don't record GI values at all**, say so once instead of per food: tick **I do not record glycemic index data** at the foot of **Settings** then **Glycemic Index Reference Table**. NuMa then never asks you for a GI value when you add a food, the per-food GI checkbox disappears as redundant, the GI field itself folds away on this page (still there if you want it), and the notices about which GI reference table is in use stop. Nothing already recorded is deleted or hidden — a GI value you have saved is still shown and still used to work out [glycemic load](#gl) — and un-ticking it puts everything back, including any per-food choices you had made. A food still missing a DIAAS estimate goes on prompting for that, since it is a separate question.

**Saving settles the food.** Whatever you fill in, clicking **Save annotation** means you have dealt with this food: it stops interrupting you when you add it to a meal or the pantry, even if you deliberately left one of the two estimates blank. Come back any time through Annotate a Food to fill in the rest. **Skip for now** is the opposite — it saves nothing, so NuMa asks again the next time you add that food.

**When only one estimate is outstanding**, the prompt says so, and says which. The form always shows both the GI and the DIAAS field, so a prompt that is really about DIAAS would otherwise look identical to the GI prompt you just dealt with. A line above the form names whichever one is already settled, and the two fields are badged **Asking for this one** and **Settled — not being asked about** so there is no guessing. The page always opens at its top, with the cursor in the GI box when the food has no GI yet; when it has a GI but no DIAAS, a **DIAAS needed, click to go there** button near the top takes you straight to the DIAAS box.

Annotations appear wherever that food is used: [Food Cache](#gloss-food-cache) list, food and recipe analysis, and meal analysis.


#### Foods to Import Review Table {: #food-import}

*Search terms: Claude import, import preview.*

Appears when you click Review on the Import Claude response page, to import the data Claude gave you. Shows a preview so you can review before confirming the write.

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

Review each row for plausibility. If a value looks wrong, don't import — go back to the Import Claude response page, edit the pasted text in the textarea (or paste in a corrected reply from Claude), and click **Review** again. Otherwise click **Import … into cache**.

After importing, each food is written to your cache. Foods that gain amino acid data change from — to ✓ in the [AA](#gloss-aa) column of the [Food Cache](#gloss-food-cache). Any notes Claude added are saved as curator notes — view them by clicking that food's "Notes ▸" link in the [Food Cache](#gloss-food-cache) list.

For the full import workflow, see [Food Cache](#food-cache-web).


#### Custom Food Profiles List {: #drafted-foods}

*Search terms: custom foods list, my custom foods.*

Shows the custom food profiles you have created by hand -- products from a label, research table entries, or supplements not in [USDA](#gloss-usda) or Open Food Facts[^3].

Columns:

    Name    Food name as you entered it.
    Code    The food's code — UD followed by a number (UD4).
    Type    Where it came from ("User Drafted", or the source of a
            food you copied and edited).

Custom food profiles are stored in your [Food Cache](#gloss-food-cache) and appear in all food searches alongside [USDA](#gloss-usda) and Open Food Facts[^3] entries. Internally these are called "user-drafted" foods, and their [codes](#gloss-code) start with UD (older versions of NuMa showed "usr" — see the [usr](#gloss-usr) glossary entry).

To edit nutrient data: open the food from [Food Cache](#gloss-food-cache) or this list and click **Edit nutrients**. Editing is done in the [Food Cache](#gloss-food-cache) record itself, not in a separate copy.

**Comparing search results before you copy.** On the edit page, both searches ("Copy nutrient values from another food" and "Estimate amino acids from another food") give each result a **Compare** checkbox. Check the ones you want to weigh up and click **Compare checked foods with this one**: the [Compare](#comparison) page opens with the profile you're editing first and the checked foods beside it, every nutrient side by side per 100 g. Its **← Back to editing …** button at the top brings you back to the section you came from. Any unsaved edits are saved first, as with a search, so the comparison shows the profile as you have it now, and the Undo offer is waiting when you return.

To create a new custom profile: Foods -> Custom Food Profiles -> Create. See [Food Cache](#food-cache-web) for an alternative way to get missing data (e.g. amino acid data from Claude [AI](#gloss-ai) for foods not in [USDA](#gloss-usda)).

**Estimating amino acids by copying from another food.** Whenever you're prompted for a food's amino acid profile (creating a custom food profile, copying a cached food, or editing any food's data), a third option lets you search for and pick a similar food that already has amino acid data, instead of typing values in or pasting from literature. The picked food's amino acids are **scaled to match this food's own protein content** (not copied raw) — a food with less protein than the source gets proportionally less amino acid content, and vice versa — the same scaling already used by hand in this app's built-in curated foods (e.g. amino acids scaled between fresh and dried okara). A note documenting the source food and scale factor is suggested automatically for the Note field. On the web app, the same picker appears as an "Estimate amino acids from another food" panel on the custom-profile edit page ([Custom Food Profiles](#custom-foods)); editing any food's data this way marks it user-drafted, same as any other edit.

On the web app, [Food Search](#food-search) (and Food Cache and Pantry's own ingredient search) has a shortcut into this workflow: every food row shows a **Copy as custom-food draft** link/button. Clicking it duplicates that food as an editable draft and takes you straight to its edit page, [AA](#gloss-aa)-source search box ready — skipping the separate trip through Custom Food Profiles' own "Copy a cached food as a draft" search.


#### My Pantry Table {: #pantry}
Shows the protein sources you have flagged as currently on hand. The Pantry drives the complement advisor -- when NuMa suggests foods to fill an amino acid gap, it checks your pantry first and shows matching foods in a "From your pantry" tier.

Columns:

<pre>
    Compare Tick to compare pantry foods side by side.
    Food    Food name.
    Code    The food's code (U171477, UD4, OFF3 ...); -- for name-only entries.
    AA      Amino acid data status.
              checkmark  AA data in your cache. This food can be used in
                         complement suggestions.
              X          No AA data. Click Edit to add it.
              --         Name-only entry: no USDA link, no nutrient data.
                         Use Link a food to attach real data.
    Notes   Your optional note for this pantry entry.
    Added   When you added it.
    Type, GI est., DIAAS   Same as the matching columns in the
            <a href="#cached">Food Cache</a> list — see the DIAAS entry there for
            how the saved-estimate-vs-reference-table value is chosen.
    ARCH    Shown only when archived entries are visible (the show-archived
            toggle) — a dot marks an entry as archived. See <a href="#archive">archiving</a>.
</pre>

Only pantry foods with [AA](#gloss-aa) data (checkmark) appear in complement suggestions. Name-only entries (--) and those without [AA](#gloss-aa) data (X) may still appear if their name matches a built-in complement table entry. Archived pantry entries never appear in complement suggestions.

Actions: **Add a food** ([USDA](#gloss-usda) search or name-only — the search results table is the same one described in [USDA Food Search Results](#food-search), including the Source filter and sort-order dropdowns), **Remove**, **Archive/Restore** (see [archiving](#archive)), and an **Edit** button on each row that jumps straight to that food's Food Cache entry for editing. A name-only entry (no USDA link) shows a **Link a food** button instead — search and pick a match to attach real nutrient data to that same pantry row, rather than adding a duplicate.

**Why save just a name?**{: #pantry-name-only} It's a placeholder: it records that you have a food on hand when a search doesn't turn up a good match, you're offline, or you'd rather pick the right match later. To add one, click **Can't find it? Save just the name for now** just under the Pantry search box. A name-only entry has no nutrient data at all, so it can't be analyzed or compared until you link it — but it keeps your pantry list complete in the meantime, and **Link a food** turns it into a full entry without retyping anything.

**Only a search-and-select adds a food to your [Food Cache](#gloss-food-cache).** Picking a real match from **Add a food** caches it, the same as any other food search in NuMa — see [how foods enter your Food Cache](#food-data) in Part 7. Typing a **name-only** entry does not: nothing is written to the cache until you use **Link a food** to attach a real match, which is why a name-only row shows "--" in the [AA](#gloss-aa) column above instead of a checkmark or X.

See [complement suggestions](#comp) for how complement suggestions use your pantry.


#### Protein Digestibility Overrides {: #dcp-overrides}

*Search terms: digestibility override, custom digestibility.*

Shows your custom true [ileal digestibility](#gloss-ileal-digestibility) coefficients. These values override the defaults NuMa uses in meal-level [DIAAS](#gloss-diaas) calculations.

Columns:

    Food name       Name of the food this override applies to (matched
                    case-insensitively against meal ingredients).
    Digestibility   Your custom coefficient (0.00-1.00). The fraction of
                    protein absorbed by the small intestine.
    Notes           Your source note (e.g. "Smith 2020 Table 3").

When an override is active for a meal ingredient, the Digestibility column in the Meal Protein Digestibility table shows the value with a "↑ user" marker next to it, distinguishing it from estimated or literature defaults.

Use overrides when you have found a published measured value for a food you eat regularly and it differs meaningfully from NuMa's default. Values should come from primary literature ([ileal digestibility](#gloss-ileal-digestibility) studies), not from product labels or general nutrition sources.

Set in **Settings → 4. Protein Digestibility Overrides**: enter a food name (matched exactly), a coefficient (0.00-1.00), and an optional source note, then Save. Entering the same food name again replaces its existing override. Each row in the table has a delete (✕) button.

See [meal protein digestibility](#meal-diaas) to see where this value appears in the analysis output. See [DIAAS](#diaas) for background on true [ileal digestibility](#gloss-ileal-digestibility).

---

## Part 6 — Shared Operations

*(Reading time: 47 minutes)*

Several operations show up in more than one place in the app — the same mechanism behind a search box on three different pages, say. This Part collects those, so they're documented once instead of several times, with a link back here from every place they apply.

### A. Setting up your computed daily nutrient targets {: #daily-nutrient-targets}

*Search terms: daily targets, goals table.*

This is a table of your personalized nutrient targets, computed from your profile: calories, protein, carbohydrates, fiber, every tracked mineral, and every tracked vitamin — each labeled with its goal type (minimum, target, or upper limit). See [daily nutrient goals](#goals) for the formulas behind these numbers, and [RDA](#rda) for where the underlying reference values come from.

This appears as its own read-only Settings panel and updates automatically whenever **Your Profile**, just above it, changes. It requires an active profile — if the table looks empty or the numbers seem off, check that your profile (age, sex, weight, height, activity level) is filled in first.

**Archiving vs. deleting** is documented once, in Part 5's [Archiving](#archive) reference, so it isn't repeated here.

**Every percentage shown elsewhere carries its goal type too, not just this table.** A percent-of-target is meaningless on its own — 120% is good news for a minimum (protein: you've cleared the bar) and bad news for a limit (sodium: you're over the cap). Wherever a nutrient's percentage appears — on a food, meal, recipe, daily summary, or trend page — it's followed by a small `min`, `max`, or `target` tag (hover it for the full explanation), so you never have to come back to this table to know which direction is good.

### B. Dietary Preferences (Settings → 3) {: #diet}

*Search terms: diet preference, vegan, filter foods.*

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

*Search terms: search order, search ranking, search by code, result order.*

**Searching by code.**{: #search-by-code} Every food and recipe search box — Foods → Search, a meal's add-food panel, Edit Recipe's ingredient search, Compare, Convert, My Pantry, and the "search for a food to copy from" boxes — also takes a [code](#gloss-code) on its own: **[R21](#gloss-code)** for a recipe, **U171477**, **[UD4](#gloss-code)** or **[OFF3](#gloss-code)** for a food, **U171477.1** for an older version of one. Upper or lower case both work. The search then shows just that one food or recipe, straight away and without going online, whatever the Source boxes are set to, and even if it's archived. A plain number works too when it is the [FDC ID](#gloss-fdc-id) of a food already in your Food Cache (171477 for U171477). A code NuMa has nothing for, or a number that isn't a cached food's FDC ID, is searched as ordinary text instead, so a USDA FDC ID you haven't used yet still finds the food online. A box that can't offer the item (a recipe in a search for foods only, a recipe inside itself) ignores the code. Hover over a search box for a reminder.

The boxes that *filter a list* take a code too: the Recipes list (**R21**), the Food Cache and Annotate lists, My Pantry's **Filter my pantry list** (**U171477**, **UD4** …), Food Use in Recipes' name filter, the Food Use in Meals "Replace it with" box, and [Search meal history](#meal-history), where **U171477** or **R21** lists every meal that food or recipe was logged in. A code there narrows the list to just that one item, archived or not; anything else filters by name as before.
When you search for a food — whether from the Food Search page, the Meals & Log "Add Food or Recipe" panel, or a recipe's ingredient search — NuMa has to decide what order to show the matches in. That's a harder problem than it sounds, because "best match" usually means several different things at once: does the name contain your search words? All of them, or just some? And does it matter which words a near-miss is missing?

**The short version:** results are ranked first by how many of your search words appear in the name — an item matching every word you typed always outranks one matching only some of them, which always outranks one matching none. Your own matches are then listed before the online ones ([USDA](#gloss-usda), Open Food Facts, Canadian Nutrient File and the rest), under a "From your recipes, pantry, and food cache" heading with a divider below it, so something you already have is never buried under a wall of online results. Within your own matches, **recipes come first**, then Pantry and Food Cache foods, each group in best-match order. (An earlier version of NuMa let pantry/cache items always outrank everything else in the "Pantry, Cache, then Other" sort mode regardless of match quality, so an unrelated pantry item with only a coincidental word match could show up ahead of the food you actually typed. That mode now only breaks ties this way among equally-good matches — see below.)

**Word order matters, too.** If you type more than one search word, NuMa treats the order you typed them in as a signal of what matters most to you. Suppose you search `milk dry instant` because there are two kinds of dry milk — instant and non-instant — and you specifically want the instant kind, but you've put "dry" before "instant" because that's the more important distinguishing word to you. If nothing in your data matches all three words, NuMa prefers a match on `milk` + `dry` over a match on `milk` + `instant`, precisely because you typed "dry" first. In effect, the words you type earlier act as your stated priorities — a partial match that preserves your earlier words beats one that preserves only a later one, even when both partial matches contain the same number of words.

This means you can deliberately front-load your most important search word when you know a food name might be ambiguous or your data might be incomplete — put the word you care most about disambiguating on first, and let NuMa's ranking favor it if a perfect match isn't available.

*(For technically skilled users: the exact algorithm — including how word order is encoded as a simple bitmask comparison — is documented in `README-numa-documentation.md`, under "Searching for a food.")*

**When several results tie on text relevance, USDA data quality breaks the tie before name length does.** A dozen near-identical branded listings (say, a dozen "INSTANT NONFAT DRY MILK" products) can match your search words exactly as well as the one or two Foundation/[SR](#gloss-sr) Legacy foods actually named that — and branded names are often shorter, which used to let them win the final tiebreak even though they're the ones least likely to carry real amino acid data. Ties are now broken by data quality first (Foundation/SR Legacy, then Survey/Experimental, then Branded/Open Food Facts) and only fall back to shorter-name-wins after that, so the reference food most likely to actually answer your question surfaces before its branded look-alikes.

**Your own data is always checked first.** Before NuMa ever reaches out to USDA or Open Food Facts, it checks your local Food Cache and Pantry — a match there appears instantly, with no network round-trip. USDA and Open Food Facts results are still fetched right behind it (not only when the local check comes up empty), so a food newer than your cache, or one you've never looked up before, still turns up — it just takes a moment longer to appear. Once those external results arrive, the whole list (local and external together) is re-ranked by match quality as described above, so a stronger external match can end up ahead of a weaker local one rather than being stuck below it. A 12- or 13-digit barcode ([UPC](#gloss-upc)-A or [EAN](#gloss-ean)-13) skips general search entirely and goes straight to a direct Open Food Facts lookup by that exact code.

**Search result depth.** Plain, unprocessed foods (the ones most likely to carry full amino acid data) can get buried under branded or prepared-dish matches for the same word — USDA's own relevance ranking can push something like "Potatoes, flesh and skin, raw" 15–20 results deep for a plain "potato" search, or return two dozen canned/branded products before a plain cooked bean shows up for "pinto beans." To counter this, NuMa runs a second search pass restricted to Foundation Foods and SR Legacy (USDA's most complete, least processed data), so those results aren't lost in the noise. How many results that second pass fetches is configurable (Settings → 6. USDA [API](#gloss-api) Key → Search result depth) — the default of 25 is enough for the vast majority of searches; set it higher if you still don't see the food you expect, or to 0 to remove the cap entirely (every matching result USDA returns, in one page — a higher number means a slightly slower search).

### D. Data editing: what changes when editing recipes, meals, or the food cache {: #editing-consequences}

*Search terms: editing consequences, recalculation.*

*How NuMa shows you the effect of a change, including on past days: [Seeing what a fix changed](#data-effects). Every data check: [Checking your data](#checking-your-data).*

**The short answer: changes to nutrient data cascade, all the way down; amounts you've already typed do not change.** Edit a food's nutrients, or a recipe's ingredients or servings, and every total built on it — other recipes, logged meals, past days, the Meals & Log list, the Daily Summary, averages and plots — is brought up to date automatically. You never need to recompute anything by hand. What does *not* change by itself is an amount already entered in a recipe or meal: it was saved as grams when you typed it, so a later portion edit leaves it alone, and Foods → 9 lists the ones worth a second look.

| You change… | Recipes that use it | Meals that log it, past days included | More |
|---|---|---|---|
| **A food's nutrients** — editing them, copying from another food, estimating amino acids, refreshing from [USDA](#gloss-usda), importing Claude's answer, merging duplicates | Recalculated at once, and every recipe built on those too | Recalculated by the next page you open | [Editing or changing a food](#food-edit-consequences) |
| **A food's portions** (`p1`, a cup weight) | No change — amounts keep the grams they were entered with | No change, for the same reason | [Amounts that no longer match](#stale-amounts) |
| **A food's [GI](#gloss-gi)** (Foods → Annotate) | Recipe glycemic load follows at once — it's worked out fresh each time it's shown | Same, for meals and days | [Glycemic Load Output](#glycemic) |
| **A food's name** | The new name replaces the old one on every ingredient line that uses the food; nutrients unaffected | Same, and in your pantry | [Editing or changing a food](#food-edit-consequences) |
| **Deleting a food** | Refused while any recipe, meal or pantry entry uses it | Refused | [Editing or changing a food](#food-edit-consequences) |
| **A recipe's ingredients or amounts** | That recipe recalculated, and every recipe built on it | Recalculated by the next page you open | [Changing a recipe…](#recipe-dcp-cascade) |
| **A recipe's servings count or Total weight** | Per-serving figures change, and cascade as above | A meal logs servings, so "1 serving" now means the new serving; the meal page flags the item and asks whether to keep the grams you ate | [How a meal records a recipe](#recipe-servings-grams) |
| **A recipe's name** | The new name replaces the old one everywhere | Same | [Editing or changing a food](#food-edit-consequences) |
| **Deleting a recipe** | Its sub-recipe lines stay, flagged "recipe (deleted)" | Its meal items stay, flagged the same way | [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) |
| **Substituting** one food or recipe for another everywhere | Ingredients switched and recalculated, cascading up; amounts kept as typed | Items switched; amounts kept as typed | [Replace a Food or Recipe Everywhere](#fooduse-substitute) |
| **A what-if** | Nothing, unless you click Apply | Nothing, unless you click Apply | [Saving, downloading and applying a what-if](#whatif-apply) |
| **Your profile** (weight, targets) | — | Past days keep the profile they were pinned to | [Per-Day Profile Tracking](#day-profile) |
| **The manual's source file** | — | — | [Editing the manual's source file](#manual-source-edits) |

A meal's or recipe's own page always works its figures out fresh from your data as it is now, so it is never behind. The cascade exists for the figures NuMa *saves* for its lists, and is described below.

NuMa saves some of its results so it doesn't have to work them out again on every page: each recipe's [DCP](#gloss-dcp) per serving, and each meal's DCP, calories and nutrient totals — the figures the Meals & Log list, the Daily Summary's Recent Days table, Nutrient averages across days and Nutrient Plot all read from. Whenever you change something those results were worked out from, NuMa works them out again for you. This section is the list of what follows from what, so an edit never has a consequence you didn't expect. For the other side of the same question — where NuMa fills in data that's missing, rather than recalculating data you've changed — see [Where NuMa fills gaps: estimates and estimation](#filling-gaps).

#### Changing a recipe DCP by changing the recipe changes the DCP in everything that uses it {: #recipe-dcp-cascade}
A recipe can be used as an ingredient inside another recipe — a lentil sauce that shows up in three different dinners, say. Editing and saving that base recipe recalculates its own digestible complete protein ([DCP](#gloss-dcp)) automatically. If it's also used as a sub-recipe ingredient elsewhere, saving it recalculates DCP for every recipe that depends on it too — directly, or through another sub-recipe in between — so a foundational recipe's protein score is never left stale in anything built on top of it. You never need to manually recompute a dependent recipe just because you changed the recipe it's built from.

**Meals that log the recipe follow along too.** Every meal that logs the recipe you changed — or any recipe built on it — has its saved DCP, calories and nutrient totals recalculated as soon as you open your next page in NuMa, so the Meals & Log list and the Daily Summary show the new figures straight away.

A bulk "recompute DCP for all recipes" option still exists on the Recipes list — worth running after a bulk import, or if you suspect stale numbers predating this cascading recalculation.

#### How a meal records a recipe: servings, with grams when they're known {: #recipe-servings-grams}

*Search terms: recipe servings, grams per serving, serving weight.*

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

*Search terms: edit food, rename food, change nutrients, food changes.*

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

**Renaming a food renames it everywhere you've used it.**{: #food-rename} When you save a new name on a food's Edit page, the new name replaces the old one on every recipe ingredient line, every logged meal item (past days included) and every pantry entry that uses that food, the same way renaming a recipe always has; the page tells you how many places it changed. Nutrients don't change, because they always come from the food a line is *linked* to, whatever name it shows. One thing can change: NuMa estimates protein digestibility from a food's name (see [Protein digestibility](#digestibility-by-name)), so a name that drops a telling word ("tofu", "lentil") can change the food's DCP figures, and a digestibility you set yourself moves to the new name with it. A name you typed into an ingredient line's own **Edit** popup on the Edit Recipe page is replaced too. That popup changes only the name the line shows, never which food it's linked to. So if a recipe's nutrients look wrong, check that each ingredient is linked to the food its name says; to link one to a different food, remove the line and add the right food.

**A food still used somewhere can't be deleted.** NuMa refuses to delete a food that a recipe, a logged meal or your pantry still uses, so nothing is ever left pointing at a food that no longer exists. Recipes are different — see [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere).

#### Meals and days {: #meal-edit-consequences}

*Search terms: meal totals, day totals, recalculate meals.*

A meal's or a day's own page always works everything out fresh, from whatever your foods and recipes contain right now. The figures saved for the list views (Meal [DCP](#gloss-dcp), Day DCP, % of goal, calories and the nutrient columns) are brought up to date automatically after any food or recipe edit, as described above. The batch button on [Meals & Log](#meal-columns) that calculates DCP and calories for all meals, or just the last 10 or 30 days, is still there for after a bulk import, or for meals whose figures were saved before this automatic refresh existed (October 2026).

If one of these automatic recalculations ever fails outright, it's reported under [System Issues](#system-issues-howto) in Settings rather than silently leaving old numbers in place.

#### Editing the manual's source file (user-manual.md) {: #manual-source-edits}

*Search terms: edit manual, manual source, markdown, build manual.*

*For anyone running NuMa from its source folder (`python web/launcher.py`). An installed copy of NuMa carries its own manual; editing files there does nothing useful.*

This manual is written in `user-manual.md` and shown in your browser as `user-manual.html`, which NuMa builds from it. **To see an edit, save `user-manual.md` and reload the manual's browser tab.** Opening the manual, or the Home page, checks whether the `.md` file is newer than the `.html` and rebuilds it if so. There's no need to restart NuMa or run anything. A manual tab that is already open won't change until you reload it.

The rebuild also rewrites the reading-time figures in `user-manual.md` itself, so your editor may report that the file changed on disk. Accept the new version.

If a reloaded tab still shows the old text:

- **Check the "Updated" date on the manual's second line.** If you've ever clicked **Update manual now** on the Home page, NuMa keeps that downloaded manual and shows it instead of your own build whenever its date is the newer one. Set the date to the current date and time to make your copy the newer one.
- **Run `python3 scripts/build_manual.py` from the NuMa folder.** It does the same rebuild, but prints any error that stopped it (two footnote markers side by side, for instance).

### E. Entering custom foods and dietary supplements {: #custom-foods}
#### Custom food profiles

*Search terms: create food, homemade, nutrition label.*

When a food isn't in [USDA](#gloss-usda) or Open Food Facts[^3] — or the entry you found is incomplete — create a custom profile from an existing food as a starting point, or from scratch, via Foods → Custom food profiles → Create.

Whichever interface you use, the same fields apply:

- **Name** — what to call this food in searches and meal logs.
- **Supplement mode** (see below) or a normal serving size and unit.
- **Basic macros** — calories, protein, total fat, carbohydrates, fiber, sugars, saturated fat, mono/poly fats, sodium. Fill these in first: calorie totals and protein quality depend on them.
- **Minerals, vitamins, amino acids, and [phytonutrients](#gloss-phytonutrients)** — all optional. Each box takes a plain number in the unit shown beside it, or a number with a unit that NuMa converts: `400 IU` ([IU](#gloss-iu)) for vitamins A, D and E, `12 mg`, `2.4 µg`, `1046 kJ` for calories. Amino acids can be typed one by one, or pasted as a table into **Paste an amino acid table** (g or mg per 100 g of food, g per 100 g of protein, or mg per g of protein — choose which, and NuMa converts). See [Data entry](#data-entry) for every form NuMa accepts.
- **Note** — document your source or any caveats about the data.

Once saved, the food appears in every search and can be used in meals and recipes exactly like any other food. Edit or delete it from the same place you created it, at any time.

**Editing the `p1`, `p2`, … portion shortcuts.** A food created by copying an existing one carries over that food's saved portions ("1 cup," "1 slice," and so on) exactly as-is — the custom-profile form itself doesn't have a portions editor. To add, remove, or change one, go to that food's [Food Cache](#food-cache-web) entry and use its **Portions** action, the same tool used for any cached food — see [A food's portion or serving-size data looks wrong](#ts-no-piece-portion) for how. This works whether the food started from scratch or as a copy, since a custom profile is still just a food in the cache underneath.

#### Dietary supplements — tablets, capsules, softgels {: #supplements}
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


### F. Deleting a recipe that's used elsewhere {: #delete-recipe-elsewhere}

*Search terms: remove recipe, recipe in use.*

If the recipe you're deleting has been logged in a meal, or another recipe uses it as a sub-recipe (an ingredient that is itself a recipe), NuMa warns you before deleting — whether you click **Delete** on the Recipes list or **Delete recipe** on the recipe's own page. The warning says how many meals it's logged in (and between which dates) and which recipes use it, and suggests **Archive** instead: an archived recipe drops out of lists and search but keeps working everywhere it's used. If you delete it anyway:

1. Every meal it's logged in keeps the line, flagged "recipe (deleted)", but no longer counts its nutrients in that meal's totals.
2. In a recipe that used it as a sub-recipe, that ingredient line is not removed. It stays in place, but is now flagged "recipe (deleted)" wherever it appears — in ingredient lists, meal history, and Food Use in Meals. This is expected, not a bug: NuMa can't know whether you meant to also cascade-delete every recipe that depended on it, so it leaves the reference intact and visible instead.
3. If you later create a new recipe whose name shares at least one word with the deleted recipe's name (for example, re-creating "Beef Stew" as "Chicken Stew," or under the exact same name as before), NuMa offers to relink those broken references to your new recipe — the offer appears as a banner on the new recipe's edit page.
4. If more than one deleted recipe matches by name, you're offered each one separately, and only the ones you confirm get relinked. Declining leaves the old references flagged as before.
5. To see every currently-broken reference in your data, regardless of what you're about to create, use the "Broken recipe references" button on the Recipes list.

### G. Ignoring a complement suggestion {: #ignore-complement}

*Search terms: ignore suggestion, hide suggestion, exclude food.*

Every [complement suggestion](#comp) — a Tier 1 gap closer, a Tier 2 [DIAAS](#gloss-diaas)-boosting option, or a food inside a Tier 3 two-food combination — carries an "Ignore this suggestion in recalculation" checkbox. Check one or more, then click **Recalculate complements** (it activates as soon as anything is checked) to reload the page with those foods excluded from every tier — pantry, general, two-food combinations, and DIAAS boosters all rebuild around the remaining candidates. Use this when a suggested food genuinely isn't an option for you (out of stock, disliked, already ruled out for some other reason) and you'd rather see the next-best alternative than one you can't act on.

Ignoring more foods on a later recalculation adds to the list rather than replacing it. A collapsible "Ignoring N suggestions — manage" panel lists every currently-ignored food alphabetically, each with its own "Remove ignore" checkbox to restore just that one; a "Clear all" link removes the whole list at once.

The ignored list is not saved anywhere — it resets the moment you navigate away, or reload the page without it. Available on the Food detail, Meal, and Recipe pages.


### H. Where NuMa fills gaps: estimates and estimation {: #filling-gaps}

*Search terms: missing values, generic values, filling in.*

*To find the gaps themselves, see [Checking your data](#checking-your-data).*

Food data is never complete — plenty of foods have no amino acid figures, and no food record carries a protein digestibility figure at all. Where a calculation needs a number that isn't there, NuMa either fills it with an estimate from a small built-in list, or leaves the food out and tells you. It never quietly saves a generic estimate into your own data. This is the full list of where estimation happens.

**Protein digestibility — an estimate for every food, every time.**{: #digestibility-by-name} [DCP](#gloss-dcp) needs to know how much of each food's protein your body actually absorbs. Food databases don't record that, so NuMa looks it up by the food's name, in this order:

1. your own figure, if you've entered one for that food ([Protein Digestibility Overrides](#dcp-overrides), Settings → 4);
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

*Search terms: data checks, data quality, problems in data, find errors.*

Every result NuMa gives you is only as good as the food data underneath it. A food with no calorie value quietly adds nothing to every calorie total it's part of; a wrong cup weight is worse still: NuMa works out the food's density from it, and uses that density for *every* volume measure of the food — tablespoons, teaspoons, fluid ounces, any fraction or multiple of a cup — so every such amount you enter for that food, in any recipe or meal, comes out wrong. (Correcting the cup weight fixes amounts entered afterwards; those already entered are listed under [Amounts that no longer match](#stale-amounts).) NuMa checks your data in three places:

- **When data comes in.** Each food is checked the moment it's saved, by whatever route — a [USDA](#gloss-usda) fetch, Open Food Facts, a [CSV](#gloss-csv) or Claude [AI](#gloss-ai) import, or your own typing. Missing calories are filled in as an estimate, and right after you add a food with a problem to a meal or recipe, a note on that page says what's wrong with it.
- **Where you use data.** Food, meal, recipe and daily-summary pages flag what affects the figures you're looking at.
- **In one place, on demand.** **Foods → 9 (Database Integrity and Data Completeness Check)** lists every problem across all your data. The Home page tells you when new problems turn up (see [the reminder](#data-check-reminder) below).

#### Every check, and what to do about it {: #data-checks-list}

*Search terms: all checks, data check list, fix data.*

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
| [Missing GI values](#missing-gi) | A food you use with carbohydrate (5 g or more per 100 g) but no [GI](#gloss-gi), so [glycemic load](#gl) is incomplete wherever it appears and it can't be suggested as a [lower-GI swap](#gl-swaps) | Foods → 9 (foods you use, most-used first); any incomplete [GL](#gloss-gl) figure; Top Contributors ranked by glycemic load | Look one up on the food's Annotate page; or tick "not needed" (the same as "don't prompt me") |
| [Missing portion weights](#ts-no-volume-portion) | A food with no cup, spoon or piece weight, so a volume or count can't become grams | Foods → 9 (foods you use, most-used first); recipe pages ("No portion/weight data exists"); when you type an amount | Add the weight once on the food's Portions page; or tick "not needed" if you always weigh it |
| [Duplicate foods](#duplicate-foods) | Two or more foods with the same name, so a fix to one doesn't reach what uses the other | Foods → 9 → **Find duplicate foods** (on request) | Compare them, keep one (the rest are replaced by it everywhere), or mark "not duplicates" |
| [Recipe weight unknown](#recipe-servings-grams) | A logged recipe whose serving weight can't be worked out; a recipe whose serving size changed after you logged it | Meal pages | Enter the recipe's total weight; review the meal as the page suggests |
| [Deleted sub-recipes](#ts-deleted-recipe) | A recipe ingredient or meal item pointing at a recipe that was deleted | Recipes → Broken recipe references; Edit Recipe (offers to relink) | Relink it or remove it |
| [Failed recalculations](#system-issues-howto) | A recipe or meal whose automatic recalculation broke after a change | Settings → 15; a red alert at the top of every page | **Retry** |
| [Import checks](#fetch) | Claude AI replies, [CSV](#gloss-csv) files and recipe imports: missing names, non-numbers, unknown nutrients; imports fill only empty values | The import page's "Notes from validation" | Fix the source and import again |
| [Estimates](#filling-gaps) | Where NuMa used an estimate (calories, amino acids, protein digestibility) instead of measured data | Labeled where the figure appears | Replace with real data where you can |

**Right after you add a food.** If a food you've just added to a meal or recipe has a problem from the table above (not merely an estimate), the page you're returned to says so straight away, with a link to the food. That is the cheapest moment to fix it: one food, while you remember what it is.

**The Home page reminder.**{: #data-check-reminder} When new problems appear since you last opened Foods → 9, the Home page says how many, with a link. Opening the check counts as reviewing them, and the note goes away; it comes back only for problems that are new after that. Problems in the starter foods and recipes NuMa comes with never set it off (they're listed on Foods → 9 all the same), so a new install doesn't open with a warning about data you haven't touched. In **Settings → 14 (Data Quality Reminder)** you can turn it off, or ask for a reminder every so many weeks even when nothing is new, as a routine. A monthly look is a sensible habit if you log most days.

#### Seeing what a fix changed {: #data-effects}

*Search terms: effect of a fix, what changed.*

Fixing data changes results, sometimes a lot. A missing calorie value on almonds took one day's total from 1,527 to 1,955 kcal. NuMa shows you the effect three ways:

- **"What this change did."** After you refresh a food from [USDA](#gloss-usda), fill it in from another food, save a custom food, import Claude [AI](#gloss-ai)'s data, merge duplicate foods, or update amounts on Foods → 9, the page lists every recipe (per serving) and logged meal whose calories, protein, carbohydrate or fat moved, with before and after figures.
- **How much of a calorie total is measured.** The **Calories** note on a meal, recipe or daily summary leads with the share of its calories that comes from measured values rather than estimates, and names any food with no calorie value at all (whose grams count as zero).
- **Past days change too, and say so.** A logged meal's totals are worked out from its foods' data, so correcting a food rewrites every past day that used it. That's usually what you want, since it makes your history more accurate, but it means a past day's numbers can differ from what you saw then. Meal and Daily Summary pages note when and why their totals were recalculated ("Totals recalculated: 2026-10-03 (Nuts, almonds: its data changed)").

**Amounts that no longer match.**{: #stale-amounts} An amount you type as a volume or portion is turned into grams once, when you enter it (see [Editing or changing a food](#food-edit-consequences)). If the food's portions change later, or NuMa's way of converting does, those grams stay as they were. Foods → 9 lists every recipe and logged meal amount that would come out differently if typed today, with the grams stored and the grams it works out to now (each food has a **portions** link beside it). Check the food's portions first: if a portion weight is itself wrong (a "tsp" that's really a half teaspoon, say), fix it on the food's Portions page, and the "Now" figure follows. Then, for the amounts you tick, choose one of two buttons:

- **Update the ticked amounts to their "Now" grams** — the amount you entered stays; its grams change. Updating a logged meal changes that past day's totals.
- **Keep the ticked amounts as entered** — the stored grams are right (you weighed it, say). NuMa rewrites the amount as your own weight, "8 c (2309 gr)" becoming "2309.2 g (8 c)", the same as if you'd typed the weight yourself, so it's never listed again. To change it later, edit the amount.

Amounts typed with their own weight ("42 g", "2 T 15 g") are never listed. A volume with a weight in brackets after it, like "1/3 c (42 gr)", is: older versions of NuMa added that weight themselves, but it may be one you weighed, so check before updating. Updating one drops the bracketed figure.

The food's own **Portions page** shows the same list for that one food, right after you add, change or remove a portion (and whenever any of its amounts still don't match). There, recipe amounts start ticked; logged meals and bracketed-weight amounts start unticked, for you to decide. If you've just reordered portions, amounts entered as `p1`, `p2`… now point at a different portion, so re-enter those rather than updating them.

**Amounts converted with a generic density.**{: #generic-density} When you enter a volume ("1/3 c", "2 T") for a food that has no cup or spoon weight of its own, NuMa converts it with a generic density for that kind of food: protein powders, flours, seeds and so on. That's a reasonable guess, but it is a guess, so recipe pages, Edit Recipe and meal pages mark every such amount **≈ generic\***, with a footnote. Click the mark to go to the food's Portions page, measure the food's actual cup or spoon weight (fill a measuring cup, level it, weigh it), and add it there. The mark then disappears, and the amounts it affects show up under [Amounts that no longer match](#stale-amounts), ready to correct. Foods → 9 lists every food with such amounts, most-used first, under **Amounts converted with a generic density**. An amount with a weight in brackets ("2 T (14.7 gr)") counts too: older versions of NuMa wrote their own conversion that way, so it's most likely the same generic figure, unless you weighed it. A weight you typed yourself ("15 g") is never marked.

**Foods you use with no amino acid data, or no portion weights.** These two lists on Foods → 9 could be long — dozens of foods for a well-used install — so each starts folded up, showing only its count, and lists only foods you actually use in a recipe, a meal or your pantry (an unused food affects no result), most-used first. Open one when you want to work through it. In the amino acid list, **find amino acid data** beside a food searches for a similar food to copy amino acids from, scaled to this food's protein. Tick **not needed** for a food that doesn't matter — a sprinkle of cheese with no amino acid data, a food you always weigh — and it stops being counted. Neither list raises the Home page reminder: they're improvements to make when you have time, not errors.

**Foods you use with no GI.**{: #missing-gi} A third folded-up list on Foods → 9, built the same way: foods you use with 5 g or more carbohydrate per 100 g and no [GI](#gloss-gi) recorded, most-used first, with each one's carbohydrate per 100 g. Each one leaves [glycemic load](#gl) incomplete wherever it appears, and can't be offered as a [lower-GI swap](#gl-swaps) — swap suggestions only come from foods with a [GI](#gloss-gi), so this list is also how to get more and better suggestions. Click **look up a GI** beside a food to open its Annotate page with the reference-table lookup ([how](#gi-source-para)); saving brings you back to the list. Tick **not needed** for a food whose [GI](#gloss-gi) doesn't matter to you: it is the same as **don't prompt me** on its Annotate page, so the food stops being listed and a glycemic load that includes it says "marked don't prompt me" instead of asking you to add one. The list is hidden if you've turned GI off in Settings. Like the other two, it never raises the Home page reminder.

**Foods: days eaten.**{: #days-eaten} Another folded-up list on Foods → 9, for finding the gaps that matter most. Choose **Days to cover** and the date to go **back from** (30 days ending today, unless you change them) and click **Show foods eaten in these days**. Three tables follow, each most-days first:

- **All foods eaten** — every food eaten in those days and on how many of them, whether you logged it on its own or it came inside a recipe (sub-recipes included). "(4 in a recipe)" means on 4 of those days it came only from a recipe.
- **Eaten with no GI** — foods with no [GI](#gloss-gi) that left a day's [glycemic load](#gl) incomplete, ranked by how many days they did. This is the list to work from if the [Nutrient Plot](#nutrient-plot) shows few [GL](#gloss-gl) points: a food at the top blocks the most days. A food you only eat a pinch of (cinnamon, say) isn't listed, since too little carbohydrate to matter is counted as zero anyway. One whose [GI](#gloss-gi) is marked "don't prompt me" stays listed, because it still leaves those days incomplete. Click **look up a GI** to add one. Hidden if you've turned GI off in Settings.
- **Eaten with no carbohydrate value** — foods with no carbohydrate figure at all, not even 0, so they add nothing to carbohydrate totals or glycemic load. A supplement belongs here only until you tick its Macronutrients "not needed" under [Missing nutrient data](#data-completeness).

**Duplicate foods.**{: #duplicate-foods} Two copies of one food split your data: correct one and the recipes and meals using the other don't see it. **Find duplicate foods** on Foods → 9 lists foods whose names match once capitals, punctuation, a "\* " starter prefix, "Copy of" and "([FDC](#gloss-fdc) …)" are ignored — names that are merely similar ("Peanut butter, creamy" and "Peanut butter powder") aren't matched. For each group it shows each copy's type, how many nutrient values it has, which values you've edited on it, and where it's used. Click **Compare nutrition** to see them side by side, then **Keep this one** on the better copy (usually the one with more values, or the one you've corrected).

If the other copies have values the one you keep lacks or has differently, or portions it doesn't have, the button reads **Keep this one, reviewing the others' values first**, and you choose before anything is deleted. Each such nutrient lists the kept copy's value and each other copy's, with yours marked "(yours)", and you pick one. NuMa preselects the sensible choice: a blank is filled, and a value you edited on a copy being merged wins over the kept copy's, unless that one is your edit too. A value you copy over counts as your own edit, so a later [Refresh from USDA](#review-incoming) won't replace it without asking. Portions the kept copy lacks are ticked to be added.

Then every recipe, logged meal and pantry entry using the others switches to it and the others are deleted. Each line keeps its own name and amount, and "what this change did" shows how totals moved. If both copies were in your pantry, you're left with one entry, not two. If two foods really are different (raw and cooked, say), click **Not duplicates** and they won't be listed together again; **Show groups marked "not duplicates"** brings them back if you change your mind. A "\* " food is part of NuMa's [starter data](#starter-data); keeping your own copy instead deletes the starter one.

**Foods in your pantry more than once** is the last list on the same page. Adding a food that's already in your pantry no longer adds a second entry: the existing one is used, and brought back if it was archived. Older pantries can still have doubles, which NuMa merges on its own when it starts. Any left over are listed here with a **Merge into one** button, which keeps the oldest entry you added and combines the notes.

**Old USDA copies.**{: #old-copies} USDA revises its records from time to time. Foods → 9 lists USDA foods you haven't fetched or refreshed in over a year. That isn't a problem in itself; **Refresh from USDA** on the food's page shows whether anything changed and lets you choose what to take.

**Vitamin K from USDA, corrected.**{: #vitamin-k-fix} Until 14 October 2026, NuMa took a USDA food's vitamin K from the wrong USDA figure: menaquinone-4, one form of vitamin K2, found mostly in meat and eggs, and in small amounts. The figure that counts is phylloquinone (vitamin K1), the form leafy greens carry and the one the daily goal for vitamin K is based on. So most USDA foods saved before then show little or no vitamin K. Raw spinach, one of the richest sources, showed none at all, and a day's vitamin K looked far short of its goal. Foods saved since then are right. For the older ones, the Home page shows a **VITAMIN K** note, and Foods → 9 has a **Correct vitamin K for N USDA foods from USDA** button. It asks USDA for each food's vitamin K alone, 20 foods at a time, and replaces the old value (or removes it, where USDA has none). Nothing else about the food changes, and a vitamin K value you entered yourself is kept. Meals and recipes using a corrected food are updated to match. A food USDA leaves out of a batch is asked for on its own. One USDA has no record of at all (a food you drafted under a USDA-style number, say) is left as it is, named in the result, and not asked about again. One that couldn't be reached (no internet, say) stays on the list, and clicking the button again tries it again. Foods from the other food tables were never affected: the UK and French tables report vitamin K1, and the Canadian table's vitamin K is the same figure.


### J. Data entry: what you can type, and data errors to catch {: #data-entry}

*Search terms: typing values, input rules, form errors.*

*Every data check NuMa runs afterwards: [Checking your data](#checking-your-data).*

**NuMa's rule for anything you type: it reads what it can, tells you when it converted something, and refuses — by name — anything it can't read.** Nothing you type is silently thrown away. If a form can't be saved, everything you typed stays in its box, with a list of exactly which values need fixing.

#### Amounts — in meals, recipes, a food's page, Convert and Compare

*Search terms: units, fractions, ounces, how to type an amount.*

| You type | NuMa reads it as |
|---|---|
| `150` or `150 g` | 150 g (a number on its own is grams) |
| `150g`, `3oz`, `2T` | the same as with a space |
| `3 oz`, `0.5 lb`, `1 kg` | converted to grams |
| `1/4 cup`, `1 1/2 c`, `2 T`, `1 tsp`, `100 ml`, `1 fl oz` | converted to grams with the food's own cup or spoon weight (or a [generic density](#gloss-generic-density), marked **≈ generic**) |
| `½ cup`, `1½ c`, `¾ tsp` | the same as `1/2 cup`, `1 1/2 c`, `3/4 tsp` |
| `1,000 g` | 1000 g; `12,5 g` (a decimal comma) is 12.5 g |
| `2 tbsp.`, `3 oz.`, `2 tbs`, `1 fl. oz` | trailing periods and common spellings are understood |
| `2 T 15 g`, `1/4 c 60` | your weight wins: 15 g, shown as "15 g (2 T)" — use this when you've weighed it |
| `p1`, `2 p1`, `1.5 p2` | the food's 1st portion, twice its 1st, one and a half times its 2nd (see [Portion Input Formats](#portion-formats)) |
| `1 large egg`, `2 eggs`, `3 slices`, `2 tablets` | a count of one of the food's own portions, matched by name |
| `1 serving`, `2` (for a recipe) | servings; or switch the box to grams |

**Writing the weight in the amount and the volume in the note** (amount `16 g`, note `2 T`) is safe: the grams you typed are what's used. It's no longer necessary — `2 T 16 g` records both in one box — and better still is to give the food its real cup or spoon weight once (Food Cache → **Portions**), so `2 T` comes out right by itself.

**Refused, with the reason:**

- `2 bananas` for a food with no portion called banana — the message lists the food's portions (`p1 = 1 medium banana`…) so you can pick one.
- `2 eggs` when the food has both "1 large egg" and "1 small egg" — NuMa won't guess; type `2 large eggs` or `2 p1`.
- `2 cups` for a food with no cup weight and no generic density — weigh it, or give the food a cup portion.
- `2 T 15 bananas` — whatever follows a volume must be a weight.

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

**A pasted amino acid table** (Edit Custom Profile → **Paste an amino acid table**) takes one amino acid per line, name then figure, in whatever form the table used: `Lysine 5.2`, `Leucine: 7.9`, two columns copied from a spreadsheet. Choose what the figures are measured in. Per-protein figures are converted with the Protein box, so fill that in first. Amino acids NuMa doesn't track (arginine, alanine…) are left out and named; an unknown name, a line with no number, or the same amino acid twice is refused.

#### Data errors NuMa can't catch for you

*Search terms: common errors, per serving vs per 100 g.*

Some mistakes produce a perfectly readable number, so no form can refuse them. These are the ones worth watching for:

- **Per-serving figures typed into per-100 g boxes.** A label saying "protein 6 g per 30 g serving" means 20 g per 100 g. Typing 6 makes the food a third as nutritious as it is. (Supplements are the exception: in [supplement mode](#custom-foods) you type per-tablet amounts.)
- **The wrong unit's number.** Sodium "0.4" typed as mg when the label says 0.4 g is a thousandfold error. Type the unit with it — `0.4 g` — and NuMa does the conversion.
- **A slip of the decimal point.** `100` for `10.0`. Foods → 9 catches the impossible cases (more than 100 g of protein in 100 g of food, sugars more than carbohydrate, calories that don't fit the protein, carbs and fat) but not a merely unlikely one.
- **A wrong portion weight.** A "cup" portion that's really a half cup makes every `1 c` of that food wrong. Foods → 9 lists amounts that change when you correct a portion, under [Amounts that no longer match](#stale-amounts).
- **The wrong food.** An ingredient line keeps the name you gave it even when it's linked to a different food — see [Editing or changing a food](#food-edit-consequences).

After saving a food, its page shows any problem NuMa can see straight away; [Checking your data](#checking-your-data) lists every check.

---

## Part 7 — Essential resources

*(Reading time: 33 minutes)*

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
3. Enter it in NuMa under **Settings → 6. [USDA](#gloss-usda) API Key**, and click **Save key**. The field shows your current key in plain text whenever one is already saved, so you can retrieve it there any time.

Your key is stored on your computer only. Once set, all food searches use your personal key with a much higher rate limit.

**Search result depth** (Settings → 6. USDA API Key) — see [Search result depth](#search-ranking) in Part 6 for what this controls and why.

Every food in these online tables has a unique [ID](#gloss-id) number — think of it as a product code that identifies that one food and nothing else.

**Your [Food Cache](#gloss-food-cache)**{: #FoodCache} is a table stored on your own computer. When you search for a food, NuMa checks your [Food Cache](#gloss-food-cache) first and shows any matches in a fast **[Food cache](#gloss-food-cache)** table before going online. Any food you have looked up before will be there and can be selected instantly, without a network call. If the food is not yet in your cache, the program searches the other sources you've ticked and shows you a combined list of matches. When you select a food from that list, NuMa saves a copy of its nutrient data in your [Food Cache](#gloss-food-cache) automatically. Over time, most of the foods you normally eat will be in your [Food Cache](#gloss-food-cache) for quick retrieval.

**Edit protection.** Any food you edit manually — through Foods → 5. [Food Cache](#gloss-food-cache) — is marked as user-modified, and its type then reads, for example, "[SR](#gloss-sr) Legacy · user-edited": where it came from, and that you've changed it. NuMa will never silently overwrite a user-modified food with a fresh copy from [USDA](#gloss-usda), even if you search for that food again later. Your edits, custom amino acid values, and notes are permanent unless you change or delete them yourself. When you do ask for fresh data, with **Refresh**, you see it side by side with yours first and choose value by value — see [Refreshing a food, or filling it in from another food](#review-incoming).

NuMa keeps track of *which* values you changed, by remembering what the food's source last supplied. The food's page lists them under **Your changes to this food's original values**, each beside the original. A food is user-edited only while at least one of your changes remains, or while it has a GI, DIAAS or preparation note of yours: change a value back, or take USDA's on a Refresh, and once nothing of yours is left the "user-edited" mark goes away by itself. (A food you edited before NuMa tracked values one by one says so on its page; one Refresh from USDA lets NuMa work out which values are yours.)

**Refreshing a food, or filling it in from another food.**{: #review-incoming} Both open the same review screen: each value that differs is listed with what the food has now beside what's incoming, and only the values you tick are written.

- **Refresh** (Food Cache list, or **Refresh from USDA** on a USDA food's page) fetches USDA's current copy of the food.
- **Fill in nutrients from another food** (on the food's page, for any food that isn't one of your custom profiles) lets you search for a similar food and pick from its values. Tick the **Compare** box on a few results to weigh them up side by side first; Compare then has a **Fill in ... from ...** button for each of them, which opens this review screen with that food's values. Your custom profiles have the same search on their Edit page.

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

**Where it all lives on your computer.**{: #data-location} Your Food Cache, Food Annotations, Pantry, recipes and logged meals are all tables in one database file. That file, your page preferences (sorts, columns, dismissed notices), and any large files you've built (such as your 2021 glycemic index table) sit in NuMa's data folder. Your profiles and USDA key sit in a separate config folder:

- **Windows:** data in `%LOCALAPPDATA%\numa`, config in `%APPDATA%\numa`.
- **Linux:** data in `~/.local/share/numa`, config in `~/.config/numa` (hidden folders; press Ctrl+H in your file manager to see them).

Both folders are kept apart from the program itself, so updating NuMa never touches them. To back them up, restore them, or move your data to another computer, see [Backing up your data](#backup).

### B. Glossary {: #glossary}

*Search terms: definitions, acronyms, jargon, what does it mean.*

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

**EAN**{: #gloss-ean}  —  European Article Number, the 13-digit barcode standard used outside North America. Typing one into food search goes straight to an Open Food Facts lookup. See [Ordering food search results](#search-ranking).

**EAR**{: #gloss-ear}  —  Estimated Average Requirement. The intake that meets the needs of the *average* person in a group, with no safety margin — a population-statistics figure, not a personal target. The [RDA](#gloss-rda) is set above it. NuMa does not use the EAR for anything. See [Recommended Dietary Allowances](#rda).

**EFSA**{: #gloss-efsa}  —  European Food Safety Authority. The European Union's food-science agency, whose dietary reference values are the European counterpart of the IOM's; NuMa offers its water goals (2.5 liters a day for men, 2.0 for women) as an alternative to the IOM's, under **Water goals from** in Settings → 1, Your Profile. See [The daily goal](#water-reference).

**EPA**{: #gloss-epa}  —  Eicosapentaenoic Acid. A marine omega-3 fatty acid — found in fish and seafood — that NuMa tracks alongside ALA and DHA. See [Omega-3 Fatty Acids](#omega3).

**FAO**{: #gloss-fao}  —  Food and Agriculture Organization of the United Nations. The body that published the 2013 amino acid reference standard used for all protein quality scoring in NuMa. See [FAO reference values](#fao).

**FDC**{: #gloss-fdc}  —  FoodData Central. The USDA's online nutrition [database](#gloss-database) and NuMa's primary food data source. Each food has a unique numeric FDC ID. Website: https://fdc.nal.usda.gov/

**FDC ID**{: #gloss-fdc-id}  —  The unique numeric identifier assigned to each food entry in USDA FoodData Central. You can enter an FDC ID directly at any "Search food or recipe" prompt instead of typing a name.

**Food Cache**{: #gloss-food-cache}  —  Your local [database](#gloss-database) of previously retrieved foods. Searching the cache is instant (no network required); foods are added automatically when you select them from USDA or Open Food Facts[^3] results.

**Food Annotation**{: #gloss-food-annotation}  —  Extra information you attach to a cached food: glycemic index, a DIAAS estimate, or a preparation note. Stored locally; not part of any online [database](#gloss-database).

**FSANZ**{: #gloss-fsanz}  —  Food Standards Australia New Zealand, the agency publishing the [AFCD](#gloss-afcd) food composition [database](#gloss-database) bundled with NuMa.

**Generic density**{: #gloss-generic-density}  —  A typical weight-per-volume figure for a kind of food (flours, protein powders, seeds and so on) that NuMa uses to turn a cup or spoon amount into grams when the food has no cup or spoon portion of its own. A reasonable guess, but a guess: such amounts are marked **≈ generic**. See [Amounts converted with a generic density](#generic-density).

**GI**{: #gloss-gi}  —  Glycemic Index. A scale from 0 to 100 measuring how quickly a food raises blood glucose relative to pure glucose (100). See [glycemic index](#gi).

**GL**{: #gloss-gl}  —  Glycemic Load. A measure of glycemic impact that combines GI with the actual amount of carbohydrate in a serving. More useful than GI alone for real-world meal comparisons. See [glycemic load](#gl).

**GUI**{: #gloss-gui}  —  Graphical User Interface. A visual, point-and-click interface — this is what NuMa's web app provides (see [Part 3, "Using the Web App"](#part-3-using-the-web-app)).

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

**SPI**{: #gloss-spi}  —  Soy Protein Isolate. A concentrated plant protein (95%+ protein by weight) with high digestibility (0.95); frequently cited in complement suggestions. See [Appendix D](#comp-appendix).

**SVG**{: #gloss-svg}  —  Scalable Vector Graphics. An image file stored as shapes rather than dots, so it stays perfectly sharp at any size. The better choice for printing a plot large. See [Plot File Formats](#plot-file-formats).

**TID**{: #gloss-tid}  —  True Ileal Digestibility. NuMa's abbreviation for [ileal digestibility](#gloss-ileal-digestibility), used as a column heading in per-ingredient digestibility breakdowns.

**UL**{: #gloss-ul}  —  Tolerable Upper Intake Level. The highest daily intake of a nutrient unlikely to cause harm — NuMa applies built-in ULs for twelve nutrients with a real risk of excess, shown as a column on every nutrient analysis table. See [Maximum Nutrient Limits](#maxlimits).

**UPC**{: #gloss-upc}  —  Universal Product Code, the 12-digit barcode standard used in North America. Typing one into food search goes straight to an Open Food Facts lookup. See [Ordering food search results](#search-ranking).

**USDA**{: #gloss-usda}  —  United States Department of Agriculture. The U.S. government body that publishes FoodData Central, NuMa's primary food data source.

**User-edited**{: #gloss-user-edited}  —  A food whose data you've changed since it came from its source — shown as an **edited** tag after its [code](#gloss-code), and in its type ("SR Legacy · user-edited"). NuMa remembers which values you changed, and a Refresh keeps them unless you choose otherwise. See [Food data](#food-data).

**usr**{: #gloss-usr}  —  User-drafted. Older name for what is now the **UD** prefix of a [code](#gloss-code) (UD4): a food whose nutrient profile you created or edited by hand, rather than one retrieved from USDA or Open Food Facts[^3] — this is what the [Custom Food Profiles](#drafted-foods) list shows.

**What-if**{: #gloss-what-if}  —  NuMa's Analysis pages for trying a change before making it: remove, add, replace or scale a food across a set of meals or recipes and see the nutrition before and after, with nothing saved unless you apply it. See [What-if: Meals](#whatif) and [What-if: Recipes](#whatif-recipes).

**WHO**{: #gloss-who}  —  World Health Organization. The United Nations health agency; co-publisher, with the [FAO](#gloss-fao), of the protein and amino acid requirement guidance NuMa's protein quality scoring follows.

### C. Internet resources {: #internet-resources}

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

### D. Using this manual's search {: #search-howto}

*Search terms: manual search, how to search, find in manual.*

Use the sidebar search box near the top of the table of contents.

**By default it searches whole words, not phrases, and requires all of them for something to be considered a "hit".** Type `portion size` and NuMa looks for sections that contain *both* words somewhere — not necessarily next to each other, not in the order you typed them. This is different from typing a whole phrase and expecting an exact match: `edit portion` (as a phrase) will find nothing, because that exact wording never appears anywhere in the manual, even though the idea is covered extensively. If a search comes up empty, the fix is usually to drop a word, not add one — start with just the noun you care about (`portion`), see what comes back, then add a second word only if the list is too long to skim.

**The best match is listed first.** A section ranks higher when your words appear in its heading, when they make up more of a short section than of a long one, and when the word is a rarer one — so in `replace food`, "replace" counts for more than "food", which appears almost everywhere.

**Wrap your search in double quotes for an exact phrase instead.** Typing `"iron and zinc targets"` (quotes included) looks for that literal run of text instead of AND-ing separate words — useful when you're trying to relocate a specific sentence you remember reading, rather than explore a topic. Since it has to match verbatim, an exact-phrase search is more likely to come up empty than the default word search; if it does, drop the quotes and search the same words the normal way.

**Results are sections, not raw text.** Instead of jumping straight to every individual occurrence of your words scattered across the whole manual, search shows you a short list of section headings that contain all of them — click one (or press **Enter** to jump straight to the top match) to open it, and NuMa highlights every matching word within that section so you can see at a glance where they landed. **Enter**/**Shift+Enter** (or the &#x25B2;/&#x25BC; buttons) then step between highlighted words inside that one section, not across the whole document.

**Sections also answer to everyday words they don't use.**{: #search-terms} Some sections carry a hidden list of other words people search with — *seniors* or *elderly* for a section that says "65 and over". Search finds the section by those words too, though there is nothing on the page to highlight: the count under the box then says **this section is listed under that search**.

**The "Only show things you can do" checkbox** narrows the results further, to sections that contain some instruction — add, edit, change, remove, and similar words — rather than sections that merely *discuss* a topic. Turn it on when you're trying to do something rather than understand something: `portion size` with the box checked skips past conceptual explanations of what a portion is and goes straight to the section that tells you how to add or correct one. It's a heuristic, not a guarantee — a section phrased with an instruction word this checkbox doesn't happen to recognize can still be missed, and unchecking the box always shows you the same results or more, never fewer, so it's worth trying both if the checked list comes up empty.

**The "Match case" and "Whole words only" checkboxes** are for short terms that are also pieces of everyday words. Searching for "AI" (artificial intelligence) normally matches every "ai" in the manual — *main*, *detail*, *said* — which buries the few places that mean what you were looking for. Check **Match case** and it matches only capital "AI"; check **Whole words only** as well, and it no longer matches inside words written in all capitals, such as the titles in the [Recent program updates log](#updates-log), either. **Whole words only** on its own is handy for short abbreviations like [GI](#gloss-gi) and [AA](#gloss-aa), too. Both boxes also apply to "exact phrase" searches and to the highlights inside a section you open.

**No matches at all** shows as a yellow box under the checkboxes, naming what you searched for (for example, "No matches for "xyzzy" anywhere in this manual.") and, if a checkbox is ticked, suggesting you untick it.

### E. Finding your way around the table of contents {: #toc-howto}

*Search terms: outline, navigation, open all, close all.*

The table of contents in the sidebar opens one level at a time, so even the biggest Parts stay easy to get into.

- **Click the small ▸ arrow** beside a title to show the next level down. The entries that appear are still closed, each with its own ▸, so you can keep stepping down until you reach the section you want.
- **Double-click the ▸ arrow** to open everything below that title at once, at every depth.
- **Click the ▾ arrow** of an open title to close it again; double-clicking ▾ closes it along with everything below it.
- **Click a title itself** (not the arrow) to jump to that part of the manual.
- **Expand all** and **Collapse all**, the two small buttons to the right of the "Contents" heading, open or close every level in one go. **Collapse all** takes the list back to just its main titles (Preface, Part 1, Part 2 and so on), a short list to browse.

The list starts closed. As you read, it opens just far enough to show where you are, with the current section highlighted.

A short "How to use this list" box sits under the last entry of the table of contents. Its **Got it — hide this** button puts it away for good; the **How to use this list** link beside the "Contents" heading brings it back.

### F. Bookmarking sections of this manual {: #bookmarks-howto}

*Search terms: save place, favorites.*

You can bookmark any section of this manual to come back to it later. The bookmark buttons sit in one row in the sidebar, between the search box and the "Contents" heading.

- **Bookmark this section** bookmarks the section you're reading now — the one named last in the bar across the top of the page. While you're in a section that's already bookmarked, the same button reads **Remove this bookmark**.
- **Bookmarks (N) ▾** opens a short drop-down list of your bookmarks, in the order they come in the manual, each with the Part and section it sits under. Click one to jump there.
- **×** beside a bookmark in that list removes just that one; **Clear all bookmarks**, at the bottom of the list, removes them all (it asks first).
- In the table of contents, a **★** marks a bookmarked section and a **☆** marks a title with a bookmark somewhere inside it, so you can find bookmarks in closed parts of the list.

Bookmarks are kept by your web browser, on this computer — a different browser won't see them. They survive a manual update, since they point at sections, not at a spot on the page; if an update removes a bookmarked section, the list still shows it, marked as no longer in the manual, so you can clear it.

## Part 8 — Troubleshooting and feedback — reporting problems and offering ideas {: #feedback}

*(Reading time: 20 minutes)*

If something seems broken or confusing, there's a good chance the answer is already below. The topics are grouped by how the problem *feels* rather than which menu it's in, since that's usually how you'll remember it later — and a few topics are listed in more than one group, since the same problem can feel different ways depending on what you were expecting. There aren't so many that you can't just skim the headings if nothing matches at first.

### A. Operating the program

#### The program crashes unexpectedly {: #ts-crash}

*Search terms: freeze, hang, not responding.*

If NuMa crashes or freezes, nothing you'd already saved is lost — every action (adding a food, saving a recipe, logging a meal) is written to your data immediately, not held until some later "save" step. It's safe to just restart the program and pick up where you left off.

**If a yellow "NuMa has been updated — please restart it" bar appears,** the program was updated while it was running, and some pages won't work until it restarts. Click **Restart NuMa now**: NuMa restarts behind the page, which reloads by itself a few seconds later, right where you were. (The button appears when you start NuMa from its source folder with `python web/launcher.py`; otherwise, quit NuMa and start it again.) A page that fails for this reason shows the same message and button instead of an error.

If a page seems frozen or won't load, try refreshing it first. If that doesn't help, the program running in the background may need restarting — close and relaunch it the way you normally start NuMa.

Either way, [let us know](#feedback) — see ["How to contact help"](#quickhelp) below. This is beta software; a crash almost always means we found a real bug worth fixing, not something you did wrong.

#### You know what you want to do but can't see how to do it {: #ts-findit}

*Search terms: how do I, can't find feature, where is.*

Click any **Learn more** link near a section heading or analysis output — see [Getting help](#help) for the full list of what each one covers.
Or use this manual's own search box, in the sidebar (see [Using this manual's search](#search-howto) for how to get good results from it, especially the "Only show things you can do" checkbox) — search for a word describing what you're trying to do rather than a menu name.

If you still can't find it, [tell us what you were trying to do](#feedback) in plain language, not what menu item you were looking for. That phrasing is exactly what we need to know whether the feature exists, is named confusingly, or genuinely isn't built yet.

### B. I don't understand...

#### A recipe's "Complete" checkbox doesn't match its protein-completeness score {: #ts-complete-confusion}

*Search terms: Complete checkbox, done editing.*

A recipe's **Complete** checkbox and its amino-acid completeness score are two unrelated ideas that happen to share the word "complete." **Complete** (the checkbox, see the [Recipes list](#recipes) column guide) is a personal flag you toggle yourself — "I'm done editing this recipe" — it has nothing to do with protein quality. Whether a food or recipe's amino acid profile is **complete** (clears every essential amino acid floor) is a separate calculation shown in its [DCP](#gloss-dcp) and [DIAAS](#gloss-diaas) analysis. A recipe can be marked Complete and still have an incomplete amino acid profile, or the reverse.

#### I set a recipe's servings to 0 and now everything looks different {: #ts-servings-zero}

*Search terms: zero servings, servings 0, per 100 g recipe.*

Setting a recipe's **Servings** field to 0 is a deliberate mode switch, not an error: it tells NuMa you want to analyze the recipe by total weight or volume instead of by serving count — useful for something you haven't decided how to portion yet (a big batch of granola, say). Every "per serving" figure becomes "per 100 g" or "per 100 ml" instead, and [DCP](#gloss-dcp) shows as **NC** (not computed) since there's no serving size to divide by. Set Servings back to any number greater than 0 to return to normal per-serving analysis.

*See also:* [DCP is capped or jumped in a way that doesn't add up](#ts-dcp-cap), [A food or recipe shows an "insufficient amino acid data" warning](#ts-missing-aa), [Oxalate or glycemic index data isn't showing](#ts-oxalate-gi).

### C. I'm confused — something unexpected happened

#### USDA searches got slow, or started failing {: #ts-usda-slow}

*Search terms: slow search, USDA failing.*

Without a personal [USDA API key](#food-data), NuMa shares a demonstration key (`DEMO_KEY`) with every other NuMa user, and its rate limit is tight enough that heavy use by anyone can exhaust it, causing searches to fail temporarily for everyone. A free personal key removes this ceiling and takes about a minute to get — see [Food data — where it comes from and how it is stored](#food-data) for the sign-up steps and where to enter it (Settings → 6. USDA API Key).

#### A deleted recipe shows up as "(deleted)" somewhere {: #ts-deleted-recipe}
This is expected, not a bug: deleting a recipe that's used as an ingredient in another recipe doesn't remove that ingredient line — it stays in place, flagged "recipe (deleted)" wherever it appears (ingredient lists, meal history, Food Use in Meals). If you later create a new recipe with a similar or identical name, NuMa offers to relink the old references to it automatically. See [Deleting a recipe that's used elsewhere](#delete-recipe-elsewhere) for the full behavior and how to browse every currently-broken reference.

*See also:* [I searched for a food I know exists and got nothing](#ts-search-empty), [The food I wanted wasn't at the top of the search results](#ts-search-order), [A meal's DCP isn't showing](#ts-meal-dcp), [A past day's numbers changed after I updated my profile](#ts-day-profile).

### D. I expected to see something, and it's not there

#### A food or recipe shows an "insufficient amino acid data" warning {: #ts-missing-aa}
Some foods — especially branded or prepared products — simply don't have amino acid data published anywhere NuMa can look it up automatically. This isn't a bug; it's a genuine data gap. Two ways to close it: search for a [USDA](#gloss-usda) Foundation or [SR](#gloss-sr) Legacy equivalent (plain/raw foods are far more likely to have full amino acid data than branded ones), or fetch the missing values yourself via Claude [AI](#gloss-ai) — see [Missing amino acid profiles](#missing-aa) and [Food Cache](#food-cache-web).

*See also:* [No brand or equivalent of a food has amino acid data anywhere in USDA](#ts-no-aa-anywhere), for the harder case where neither fix above applies.

#### No brand or equivalent of a food has amino acid data anywhere in USDA {: #ts-no-aa-anywhere}

*Search terms: no amino acid data anywhere, Claude AI, research amino acids.*

This is a step beyond [an "insufficient amino acid data" warning](#ts-missing-aa): you've checked, and no brand, no store variant, and no generic [USDA](#gloss-usda) entry for this food carries amino acid data — the whole category is a gap, not just the specific product. "Search for a Foundation/SR Legacy equivalent" doesn't help here because there's no equivalent food with the data you need.

The fix is to stop looking for an equivalent *food* and look instead for an equivalent *ingredient* — something with measured amino acid data whose composition dominates the protein in the food you're trying to estimate. Flour-based baked goods, for instance, get essentially all their protein from the flour; a legume-based product gets essentially all of its protein from that legume. [Estimating amino acids by copying from another food](#drafted-foods) is the tool that turns an ingredient like this into an estimate for your actual food — it scales the ingredient's amino acid values to match your food's own measured protein content automatically, rather than you doing that arithmetic by hand.

If more than one ingredient contributes meaningfully to the protein (a flour blend, for example), blend their profiles first, by mass fraction, before treating the result as a single stand-in. The copy-from-another-food picker copies from one source food at a time, so build the blend as its own custom food profile first — call it a **proxy food**: a temporary, scratch entry that exists only to hold the numbers you'll scale from, not something you'd search for or log a meal against. (If only one ingredient dominates, it's still worth entering as its own proxy food rather than typing numbers straight into the real food — see why below.)

Once you have a proxy food — blended or not — holding the numbers you need, there are two different ways to turn it into a usable estimate for your actual food. Pick whichever fits how you'll use that food going forward:

**Option 1 — create a new, clearly-labeled draft (the general-purpose default).** Foods → Custom Food Profiles → **Copy a cached food as a draft**, pick the real food you're missing [AA](#gloss-aa) data for (it copies that food's full nutrient snapshot — protein included — into a brand-new, independent entry), rename the copy something unambiguous like "Graham Cracker, generic (estimated AA)," then run the AA-copying picker on *that* draft, scaling from your proxy food. Web app: [Food Search](#food-search)'s **Copy as custom-food draft** link does the "copy as draft" half of this step in one click, right from the search results row (also available from Food Cache and Pantry's own ingredient search). Because the original cached food is never touched, USDA can still refresh its full nutrient profile and portions automatically if that entry ever changes. The tradeoff: this new draft doesn't retroactively reach meals or recipes that already reference the *original* food — those keep pointing at the un-estimated entry until you go swap the reference over by hand.

**Option 2 — edit the original food's AA fields directly (a deliberate exception).** If you know you'll always be logging this exact product, editing its AA data in place is often more practical: every past and future meal or recipe that already references it picks up the estimate immediately, with nothing to swap. The cost is small: NuMa marks the food *user-edited* and remembers exactly which values you changed, and a later **Refresh from USDA** keeps those values unless you choose otherwise ([Reviewing incoming data](#review-incoming)). Amino acids estimated this way are also remembered as estimates, so measured values from USDA can replace them later. It's an easy choice when the food is unlikely to gain real measured data any other way — a specific branded product like Nabisco Honey Maid Grahams already has its macronutrients measured and isn't about to grow USDA amino acid data on its own, so there's little future refresh being given up.

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

*Search terms: nothing found, no results, search fails, can't find food.*

Try different search terms. "beans cooked" and "beans canned" may seem to be the same thing but they are not. The latter is a subgroup of the former. Playing with search terms can yield seriously variable results.

Check your **Dietary Preference** setting (Settings). If it's set to "Plant-based only" or "Vegetarian," foods outside that category are filtered out of *every* search, comparison, and lookup in NuMa — not just from complement suggestions — so a food you know is in [USDA](#gloss-usda)'s [database](#gloss-database) can still return zero results. Temporarily switch to "All animal foods," search, then switch back.

#### The food I wanted wasn't at the top of the search results {: #ts-search-order}

*Search terms: search order, wrong result first, word order.*

This is usually not a bug — it's the order you typed your search words in. NuMa ranks results first by how many of your search words a name contains, but when there's a tie, it treats the *order* you typed your words in as a signal of priority: matching your earlier words outranks matching your later ones. So searching `milk dry instant` will favor a "milk dry ..." match over a "milk instant ..." match whenever only one of those two words is present in a given result, simply because "dry" was typed before "instant."

If that's not the priority you meant, reorder your search words so the one you care most about comes first — put the word that most distinguishes what you want right after the main food name. See [Ordering food search results](#search-ranking) in Part 6 for the full explanation of how results are ranked.

#### A meal's DCP isn't showing {: #ts-meal-dcp}

*Search terms: DCP missing, no DCP, meal DCP not showing.*

[DCP](#gloss-dcp) now computes and saves automatically every time you add, edit, or remove an item — there's no "mark complete" step required for it to appear, and an in-progress meal already contributes to that day's total. (Marking a meal **Complete** still matters for a different reason: a day containing an unmarked meal is flagged "provisional" in Daily Summary, since its total could still change.)

If DCP is still showing as missing, the real cause is the same as [an "insufficient amino acid data" warning](#ts-missing-aa): none of the meal's food items — and for recipe items, the recipe itself — have amino acid data available yet. Add [AA](#gloss-aa) data to at least one ingredient (or analyze the recipe), and DCP fills in immediately without needing to reopen or reanalyze the meal.

#### Oxalate or glycemic index data isn't showing for a food {: #ts-oxalate-gi}

*Search terms: oxalate missing, GI missing, not showing.*

Both are opt-in and off by default — this is a configuration gap, not a bug. [Oxalate data](#oxalate) needs its Settings toggle switched on (Settings → 1. Your Profile). [Glycemic index](#gi) needs either the built-in reference-table seed or your own annotation on that specific food; NuMa will offer to prompt you for it the first time you add a new food to your Pantry or a meal.

*See also:* [A recipe's "Complete" checkbox doesn't match its protein-completeness score](#ts-complete-confusion).

### E. The numbers don't make sense

#### DCP is capped, or jumped in a way that doesn't add up {: #ts-dcp-cap}

*Search terms: DCP capped, numbers wrong, math wrong.*

This is the single most common "the math looks wrong" report, and it's almost always correct behavior: [DIAAS](#gloss-diaas) itself is not capped (a high-quality food can score above 1.0), but Digestible Complete Protein (DCP) can never exceed the protein you actually absorbed, so NuMa caps it there when the two disagree. A capped DCP is genuinely good news — it means your limiting amino acid is in strong enough supply that none of your absorbed protein is going to waste. See [Why DCP Is Sometimes Capped Below the DIAAS Projection](#dcp-cap) for the full explanation with a worked example.

#### A past day's numbers changed after I updated my profile {: #ts-day-profile}

*Search terms: past day changed, profile changed history.*

This shouldn't happen, and if it does, it's worth [reporting](#feedback) — but first check whether it's actually the documented, intentional behavior: each logged day stays pinned to whichever profile was active *when you logged it*, not whatever profile is active today, specifically so that switching profiles (illness, travel, a deliberate weight change) doesn't silently rescore your history. If the automatic pin doesn't match reality — illness or travel rarely starts exactly at midnight — you can manually reassign which profile a specific day is compared against. See [Per-day profile tracking](#day-profile) for how.

*See also:* [A deleted recipe shows up as "(deleted)" somewhere](#ts-deleted-recipe).

### F. A food's portion or serving-size data looks wrong

*Search terms: portion wrong, serving size wrong, bad portion data.*

Most of what's below isn't NuMa misbehaving, it's a gap or error in the underlying [USDA](#gloss-usda) data NuMa displays. USDA publishes nutrient values reliably, but the *portion* records attached to a food — "1 large," "1 cup, sliced," and so on — are contributed unevenly and sometimes inaccurately. NuMa shows you exactly what USDA supplies; when that's missing or wrong, the fix is to teach NuMa the correct value yourself, once, and it's remembered for every future use of that food. (One entry below — the `pN` shortcut mix-up — is a NuMa naming rule rather than a USDA data gap; it's grouped here because it's still fundamentally a portion-editing question.)

#### A food has no "per piece" or "per egg" portion — only grams {: #ts-no-piece-portion}

*Search terms: no portion, units missing.*

Some foods that obviously come in natural units — a whole egg, a piece of fruit, a slice of bread — still have no [USDA](#gloss-usda)-supplied portion for that unit, only the generic per-100-g figures. This happens because USDA's portion records are contributed per food entry, not derived automatically from the food's description, so some entries simply never got one. It's not something NuMa can infer on its own — "1 egg" isn't a fixed weight (USDA's own size grades range from about 38 g for "Small" to 63 g for "Jumbo").

Two fixes: weigh the item once on a kitchen scale and enter that weight directly (`56g`, for instance), or teach NuMa the unit permanently via the food's [Food Cache](#food-cache-web) entry, **Portions** action. Once the portion exists, every later analysis, recipe, and meal entry for that food can use it by name (`2 eggs`, `1 slice`) or by its `pN` shortcut (`2 p1`) instead of a gram weight.

#### A food has a weight portion but no cup/tablespoon equivalent {: #ts-no-volume-portion}

*Search terms: no cup measure, volume missing.*

NuMa converts a volume measure (cup, tablespoon, teaspoon) to grams using a *density* estimate for that food — mass per milliliter. [USDA](#gloss-usda) doesn't publish density directly; NuMa derives it first from a cup, tablespoon or teaspoon portion in the food's own record, including one you've set yourself in the Portions editor. Only when the food has no such portion does it fall back to a small built-in table of common foods, mostly dried herbs and spices (see [Portion Input Formats](#portion-formats)). Outside those cases, entering a volume measure will prompt you to weigh the amount and enter the grams yourself — this is expected, not a bug, since guessing a density would silently produce wrong nutrient totals.

If you'll be entering this food by volume repeatedly, teach NuMa the conversion once: weigh a level cup (or tablespoon) of it, then use the same Portions editor as above — the [Food Cache](#food-cache-web) entry's **Portions** action. From then on, cup and tablespoon amounts for that food convert automatically.

#### A food's portion or volume conversion looks flatly wrong {: #ts-bad-portion-data}

*Search terms: wrong portion weight, bad conversion.*

Occasionally a [USDA](#gloss-usda) record's portion weight is simply implausible for what it describes — a "1 large" egg listed at a weight that doesn't match a scale, or a "1 cup" measure clearly sized for a different preparation than the one you have. This is a data-entry error on USDA's side, inherited as-is; NuMa doesn't second-guess or adjust USDA's published portion weights, since there'd be no reliable way to tell a genuine correction from a wrong override.

If a portion weight doesn't match what you measure: weigh your actual amount and enter the gram figure directly for that one use, and — if you'll use this food again — replace the bad portion with a corrected one via the same Portions editor (the [Food Cache](#food-cache-web) entry's **Portions** action). Custom portions you add there are yours — they aren't overwritten by a later **Refresh** of the food's nutrient data. If you're confident the USDA source itself is wrong (not just unusual), [let us know](#feedback) — it's worth tracking so other users hit it less often, even though NuMa can't correct USDA's [database](#gloss-database) directly.

*See also:* [Enter food portions as weights, not volume measures, whenever possible](#portion-formats).

#### A food's portion "pN" shortcut points to the wrong portion {: #ts-portion-numbering}

*Search terms: pN wrong, portion shortcut, p1 p2.*

This is not a [USDA](#gloss-usda) data problem, it's a NuMa naming rule that's easy to misread: `p1`, `p2`, … always mean "the food's 1st stored portion, 2nd stored portion, …" in list order — never a portion's own description text. If you add a custom portion and type its own name in the **Description** field — say, you literally type `p1` as the description — that text has no bearing on its shortcut number. A food copied or imported from USDA usually already has a few built-in portions ("oz", "1 cup sliced," and so on) occupying the early slots, so your new one lands further down the list — often `p3` or `p4` — while `p1` still refers to whatever was already first. Typing `p1` in that situation silently applies the *wrong* portion's gram weight, with no error, since `p1` is still a valid shortcut — just not the one you meant.

Two ways to avoid this:

1. **Check the portion list shown right where you type the amount** — Foods, Recipes, and Meals all display the food's full portion set with its real shortcut number next to each entry (e.g. `p1 oz (14.2 g) · p2 1.75" square (3.0 g) · p3 …`) immediately above or below the amount field. Match against that list, not against a portion's name.
2. **Re-check after any portion edit.** Adding, removing, or reordering a food's portions renumbers every `pN` from that point on — so typing `p1` today can give a different weight than it did last week, if you've since added or removed an earlier portion. (Amounts you've already entered are safe: they were saved as grams — see [Editing or changing a food](#food-edit-consequences).) If a `pN` amount doesn't come out the way you expect, re-open that food's [Manage Portions](#food-cache-web) page and count down the list before assuming something's broken.

*See also:* [USDA standard portions and the `pN` shortcut](#portion-formats). A custom food profile copied from an existing food starts with that food's portions carried over unchanged — see [Editing the p1, p2, … portion shortcuts](#custom-foods) — so the same renumbering rule applies there too.

### G. Getting more help {: #quickhelp}

*Search terms: contact, support.*

This is extremely easy, and we want you to do it. When you're having a problem the cause is NOT necessarily you! Regardless of the nature of your problem, contacting us gives us essential information needed to make things better for you and also for every other user. We very much want to hear from you if you have a problem.

1. Text Tom at 435-272-3332. Plainly state that you are having a problem with the program. A brief statement of the problem is all I need. With your phone number I can call you back and get complete details of what I need to know to resolve your problem. I will generally call you back immediately. If you prefer a different time, let me know.

2. For non-urgent problems - which generally are improvements you'd like to see - you can also email me. Provide screenshots, if you think that would help. ALWAYS TEXT ME IF YOU SEND AN EMAIL, as I do not check my email daily, and yours easily can get lost in the 100s I get every day.

---

## Part 9 — Possible Additional Features

*(Reading time: 10 minutes)*

Ideas below are listed in their current likely probability of being implemented. User feedback has a major effect on these probabilities!

---

### Expanding Revised Optimal (Recent Research) targets {: #expand-revised-optimal}

*Search terms: older people, seniors, elderly, older adults, over 65, over-65, 65 and over, aging.*

☑ **Age/sex-banded [RDA](#gloss-rda) (completed, existing feature)** and ☑ **research-backed maximum nutrient levels (completed 2026-08-11)** are both done — see [Daily Nutrient Goals](#goals) for the full RDA age/sex band table and [Maximum Nutrient Limits](#maxlimits) for all 12 built-in Tolerable Upper Intake Levels, each sourced to the [NIH](#gloss-nih) DRI tables[^9].

☒ **Assessed 2026-10-14, not added.** The [Revised Optimal (Recent Research)](#optimal) tier — the *above-RDA* targets, as distinct from the RDA itself — has built-in defaults for three nutrients: vitamin D[^12], [EPA](#gloss-epa) and [DHA](#gloss-dha)[^13]. Three more were candidates. The test for each was the one those three were held to: an expert body's statement or a research consensus, a specific number, and a citation able to stand next to the [DRI](#gloss-dri)-sourced RDA and [UL](#gloss-ul) figures. None of the three passed:

- **Magnesium — not added.** The best evidence for an intake above the RDA in older adults is for sleep: a 2021 meta-analysis pooled three small trials, 151 people in all, and judged the evidence low to very low in quality, "substandard for physicians to make well-informed recommendations"[^96]. Those trials compared magnesium with a placebo, not one intake with another, so there is no number above the RDA to defend.
- **Vitamin K2 — not added, and NuMa couldn't track it anyway.** A Cochrane review found a single small trial, too little to judge whether vitamin K prevents heart disease[^97]. A 2021 review found that the claim of a benefit unique to K2 "is not supported by the results of the limited number of intervention trials conducted to date"[^98]. And [USDA](#gloss-usda) reports only one form of K2 (menaquinone-4), not menaquinone-7, the form in natto and most K2 supplements, so a K2 target would have nothing reliable to measure against. The assessment also turned up a NuMa bug: vitamin K had been read from that menaquinone-4 figure rather than vitamin K1, now [corrected](#vitamin-k-fix).
- **Choline — not added.** The real problem is falling short of the existing [AI](#gloss-ai), not a missing target above it: only about 8% of US adults reach the AI[^99]. Observational studies link adequate choline with better thinking and memory in older people, but there are no intervention studies in older people[^100]. NuMa's choline goal is already the AI, so its shortfall already shows.

**One existing default changed.** The vitamin D default (50 mcg) came from the Endocrine Society's 2011 guideline[^12]. Its 2024 guideline, which replaces it, takes the opposite view for most adults: it suggests *against* vitamin D supplements above the [IOM](#gloss-iom)'s reference intakes for healthy adults under 75, and suggests more only for people 75 and older, pregnant people, children and adolescents, and adults at high risk of diabetes[^101]. NuMa now follows it (14 October 2026): no vitamin D default under 75, and 23 mcg from 75 — see [Revised Optimal targets](#optimal) for where that figure comes from. 

☒ **Suggested optimum nutrition profiles by age group — retired 2026-10-14.** The idea was a few pre-built bundles of Revised Optimal settings, one per life stage ("Adults 65+ bone health," "Endurance athlete"), to load all at once. It depended on the work above producing enough above-RDA targets to make a bundle different from the [RDA](#gloss-rda) itself, and it produced none. With vitamin D now above the RDA only from age 75, a bundle would differ from the RDA by EPA and DHA alone, and the age differences that matter are already built into the RDA's own age and sex bands. 

### Source citations for major assertions in the manual {: #citations-progress}

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
- Appendices [A](#appendix-protein-quality), [B](#appendix-plant-proteins) and [C](#appendix-gl-comparison) — checked claim by claim 2026-10-14. Appendix A's cocoa example had used older reference values, which made cocoa look complete when it falls just short; its chia figures were out of date. Appendix B's amino acid notes for each food are now checked against that food's [USDA](#gloss-usda) record, which corrected almonds, cashews, pecans, walnuts, peanuts and tofu. Appendix C's points on glucose-response variation, prediction apps and carbohydrate counting are sourced.

**☐ Still to source** — research claims stated without a reference: none known at the last review. New sections are checked as they're written.

**☐ NuMa's own choices, to be labeled as such** — these are design decisions, not research findings, so the fix is to say so plainly where they're described rather than to cite anything:

- The 0.95 "near-adequate" floor below which a complement is suggested ([Amino Acid Gaps](#gap)).
- The absorbed-protein ceiling on [DCP](#dcp-cap).
- The default digestibility used when a food has no measured value.
- The 1 g floors below which a food's missing amino acid data, or missing [GI](#gloss-gi), is ignored.

### Antinutrient notes with amounts {: #antinutrient-amounts}

*Search terms: phytate amounts, quantified antinutrients, future feature.*

☐ **Proposed 2026-10-14, not started.** NuMa's [antinutrient](#antinutrients) notes say only *whether* a food carries phytate, oxalate or lectins, not how much. A pinch of sesame gets the same note as a bowl of lentils. Absorption researchers judge phytate's effect on zinc and iron by its ratio to the mineral in the same meal, so a quantified version would show, for a meal or recipe, whether that ratio is high enough to matter.

Why it waits: it needs phytate figures for each food, and [USDA](#gloss-usda) has none. They exist in published tables, but those would have to be found, checked against each other, matched to NuMa's foods, and licensed for use — a separate dataset, like the oxalate table. The thresholds that turn a ratio into "this matters" would also need their own sources. Until then, the notes stay qualitative, and the oxalate table remains the one antinutrient NuMa can quantify.

### What else? Well, know this...

#### Your ideas shape what gets built next {: #feature-ideas}

*Search terms: feature request, suggestion, wish list.*

NuMa is an evolving tool, still actively being built out. This part exists to invite you into that process: if there's something NuMa doesn't do yet that would make it more useful to you, we want to hear about it.

No idea is too small, too ambitious, or too specific to your own situation. A feature that seems minor to you may turn out to matter to a lot of other users too — and one that seems highly personal often points to a real gap in the program. Several of NuMa's existing features started out as exactly this: one user's request.

#### How to contribute an idea

*Search terms: send idea, contact, suggest a feature.*

Use the same channel as [reporting a problem](#feedback):

1. **Text Tom at 435-272-3332** with a brief description of what you'd like NuMa to do, and why it would help you. He will generally call you back to get the full picture.
2. **Or email**, especially for a longer or more detailed idea — a screenshot or example is welcome if it helps explain what you have in mind. If you email, also send a text, since email isn't checked daily and a good idea shouldn't get lost in it.

There's no such thing as a request that's not worth mentioning. If you're not sure whether NuMa can already do what you want, ask anyway — the answer might be a feature you hadn't found yet, or it might be a real gap worth filling.

### Additional features now implemented

Ideas from this Part that have since been fully built, moved here (heading levels demoted) so the list above stays focused on what's still open. Two more that were listed here have moved to where they now live: the Full Nutrient Key is [Appendix G](#nutrient-key), and the [FAO](#gloss-fao) 2013 amino acid reference values are in [Part 4, J](#fao-reference-values).

#### ☑ When to eat protein (completed 2026-10-10) {: #meal-timing-done}

Listed here before as "Meal timing". The research on *when* to eat protein — the daily total first, spreading it across meals, around resistance and endurance exercise, before sleep, and at breakfast — is now its own section: [When to eat protein](#protein-timing). Not yet covered: wider "meal timing" questions beyond protein, such as time-restricted eating.

[//]: # "Earlier resource for the wider topic: https://www.theguardian.com/commentisfree/2026/may/05/game-changer-good-health-scientists-we-are-when-we-eat (Guardian opinion piece by a scientist; not a primary source)"

#### ☑ Protein per meal (completed 2026-10-10) {: #protein-timing-done}

Listed here before as "Protein ingestion timing". Each meal's page now shows whether it carries the per-meal protein amount research associates with muscle maintenance and building — personalized from your weight and age, and judged on digestible complete protein — and each day's pages show how many meals reached it. See [Protein per meal](#protein-per-meal). Clock-time spacing between meals isn't tracked, since NuMa doesn't record when you ate.

#### ☑ Nesting Carbohydrate and Fat subtypes under their parent nutrient (completed 2026-09-19) {: #nesting-carb-subtypes}

Two of NuMa's macronutrient rows are actually parent totals with subordinate rows underneath — Fiber and Sugar are subsets of Carbohydrates, and Saturated/Monounsaturated/Polyunsaturated fat are subsets of Fat, the same relationship a Nutrition Facts label shows by indenting "Dietary Fiber" and "Total Sugars" under "Total Carbohydrate." Every nutrient table in NuMa (food, recipe, meal, daily-summary, and the printable report) now shows those five rows visually indented under their parent instead of as flat, same-looking rows — raised while building the [Full Nutrient Key](#nutrient-key) appendix, which surfaced the same gap. (The Top Contributors nutrient picker and the manual nutrient-entry form were left as-is — a dropdown and a data-entry form don't carry the same visual hierarchy concern a comparison table does.)

#### ☑ CSV export and import for foods and recipes (completed 2026-08-11)

Foods and recipes can now both be exported to [CSV](#gloss-csv) and imported back in — on this or another NuMa install — via **Export CSV**/**Import CSV** buttons on the [Food Cache](#food-cache-web) list and on each [recipe](#recipes)'s page. A recipe's export is self-contained: it bundles every sub-recipe and food ingredient's full data along with it, so nothing has to already exist on the receiving end for the import to work, and anything that already matches by name is reused rather than duplicated. See the August 11 entries in [Recent program updates](#updates-log) for full detail.

#### ☑ Plots of individual nutrients consumed daily in relation to RDAs, user-established optimums, and maximum levels (completed 2026-09-19)

The [Nutrient Plot](#nutrient-plot) plots one or more nutrients over a chosen date range, with a dashed reference line for each nutrient's profile goal (Revised Optimal target, or [RDA](#gloss-rda)/[AI](#gloss-ai) where no Optimal is set) and a dotted reference line for its maximum limit (built-in Tolerable Upper Intake Level, or your own configured cap). See the September 19 entry in [Recent program updates](#updates-log) for full detail.

#### ☑ Glycemic index lookup against the full published reference table, by subject population (completed 2026-09-20)

Every food's [Annotate](#gi) page can search the published glycemic index tables directly — the 2008 edition shipped with NuMa (about 2,500 foods), or the 2021 edition of over 4,000 foods, which you can [add to your own copy](#gi-editions)[^8] — by normal glucose tolerance, impaired glucose tolerance/diabetes, or both, and NuMa lists every plausible match for you to choose from, rather than a single auto-picked guess. **Your glucose tolerance** in [Settings](#settings) makes your own population's results come first. See [Choosing a GI value](#choosing-gi-values) for which result to pick, and [Where GI values come from](#gi-source-para) for the full source detail.

## Part 10 — Appendices

*(Reading time: 1 hour, 12 minutes)*


### A. Raw protein, protein quality, and protein digestibility {: #appendix-protein-quality}
[//]: # "develop"

#### The core problems with protein

*Search terms: protein quality basics.*

When you eat protein, not all of it is equally useful to your body. The usefulness depends on three things: **how much** protein you eat, and **how well-matched** its amino acid composition is to human physiological needs, and **how digestible** it is. 

#### The Nine Essential Amino Acids and their required relationship

Your body requires twenty amino acids to build proteins. Eleven of these it can synthesize from other raw materials. The remaining nine — the essential amino acids ([EAAs](#gloss-eaa)) — must come from food[^16].

These nine must all be present simultaneously for protein synthesis to proceed. They must also be present in the right amount. If any one of them is insufficiently supplied, then to the degree that its amount is short the other cannot be used. The surplus of the other eight cannot be stored and is instead broken down for energy — a functional waste[^110].

In summary, the *pattern* of [EAAs](#gloss-eaa) in a food matters, not just the total protein quantity.

#### The required EAA pattern, established by the FAO

*Search terms: FAO pattern, reference pattern.*

The Food and Agriculture Organization ([FAO](#gloss-fao)) of the United Nations leads international efforts to defeat hunger, achieve food security for all, and make sure that people have regular access to enough high-quality food to lead active, healthy lives.

Research has established human requirements for each [EAA](#gloss-eaa) independently, through controlled human trials. For each amino acid separately, researchers determined how much a healthy adult needs per day to maintain physiological function. From these studies came absolute daily requirement figures for each of the nine [EAAs](#gloss-eaa), expressed in milligrams per kilogram of body weight per day.

Separately, research has established how much total protein a healthy adult needs per day. By dividing each [EAA](#gloss-eaa)'s daily requirement by the total daily protein requirement, researchers produced a normalized figure: how many milligrams of each [EAA](#gloss-eaa) a person needs per gram of protein consumed. These normalized figures are the **[FAO](#gloss-fao) reference values**[^16].

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

**Concrete example — cocoa ([USDA](#gloss-usda) #169593, unsweetened dry powder):**

    Cocoa Protein total:      19.6 g per 100g food
    Tryptophan AA in cocoa:   0.293 g per 100g food

    Step 1:  (0.293 / 19.6) × 1000  =  14.9 mg tryptophan per g protein
    Step 2:  14.9 / 6.6             =  2.26

The [FAO](#gloss-fao) reference value for tryptophan is 6.6 mg/g protein (for anyone over 3 years old)[^16]. Cocoa's protein delivers 14.9 mg/g — 2.26 times what is required.

Think for a moment: what if cocoa contained none of the needed [EAAs](#gloss-eaa)? Then the protein it contained would be unusable, if it were your only protein source. It could only be broken down for energy - the fate of all unusable protein. And what if it contained all the needed [EAAs](#gloss-eaa), in the right amount - except one was totally missing? That one would make all the other unusable.

#### Why Total Protein Is the Denominator

A reasonable question is why the ratio uses total protein (including non-essential amino acids) as its denominator rather than comparing [EAA](#gloss-eaa) amounts in absolute terms.

Total protein is a normalizing device — **a common scale that makes the quality metric meaningful across foods with very different protein concentrations and very different serving sizes.**

The practical interpretation is direct: **if a food's protein clears all nine floors, eating enough of that food to meet your daily protein target will automatically also deliver your daily [EAA](#gloss-eaa) requirements.** No separate [EAA](#gloss-eaa) accounting is needed. A food that fails even one floor means you would reach your protein target before accumulating enough of that [EAA](#gloss-eaa) — the protein source is insufficient on its own.

The non-essential amino acids that make up the rest of the protein are biologically irrelevant to this specific calculation. They appear in the denominator only because total protein is the natural unit for expressing protein intake. They are not required to "activate" the [EAAs](#gloss-eaa) — they are simply passengers.

#### What "Complete" Actually Means

*Search terms: complete protein definition.*

"Complete" does not mean the amino acid ratios are all close to 1.0, or close to each other. It means **every one of the nine ratios is at or above 1.0** — each amino acid clears its own independent floor.

The nine [FAO](#gloss-fao) reference values were determined in separate human trials, one amino acid at a time. They are not ratios between amino acids; they are nine independent thresholds. Having tryptophan at 3.99× its floor while lysine sits at 1.22× its floor creates no imbalance — the tryptophan surplus cannot compensate for a deficit in another amino acid, but it does not create one either.

A food can therefore have wildly varying ratios across its amino acids and still be complete. Chia seed's protein ranges from 1.22 (lysine) to 3.99 (tryptophan) — a factor of more than three between the lowest and highest — and is still complete because nothing falls below 1.0. Cocoa shows the other side: its tryptophan is 2.26, yet it is *not* complete, because leucine (0.99) and [Met+Cys](#gloss-met-cys) (0.98) fall just short. One amino acid below the floor is enough, however small the shortfall.

The floor analogy: imagine a building with nine rooms, each with its own minimum ceiling height requirement. A room that comfortably exceeds its requirement does not help or hurt any other room. Every room must pass independently.

#### The Limiting Amino Acid — A Practical Analogy

When any one [EAA](#gloss-eaa) ratio falls below 1.0, that amino acid is "limiting" — it acts as a bottleneck that caps how much protein your body can fully incorporate into tissue.

A concrete analogy: you are mixing mortar to build a small wall. You have plenty of dry mix but run out of water before you have mixed enough for the full job. Without water, the remaining dry mix is unusable — you can build only 90 bricks worth of wall instead of 150. The water is your [limiting amino acid](#gloss-limiting-amino-acid). The unused dry mix is the protein your body cannot build into tissue, and instead breaks down and excretes.

Complementary proteins work by pooling the [limiting amino acids](#gloss-limiting-amino-acid) from multiple foods — a grain that is low in lysine paired with a legume that is rich in lysine can together clear all nine floors even though neither does so alone.

**The fate of unusable (not "complete") protein.** That unused portion isn't simply carried along or saved for later — your body has no way to bank amino acids the way it banks fat. Protein that can't be matched to the missing (limiting) amino acid is broken apart: the nitrogen-containing amino group is stripped off (deaminated) and converted to urea, which the kidneys excrete in urine; the leftover carbon skeleton is burned for energy or converted into glucose or fat, the same as it would be from a carbohydrate or fat source[^110]. So none of the calories are wasted — but as *protein*, it's gone. It cannot be retrieved later and built into muscle, enzymes, or any other tissue. This is exactly why pairing complementary foods matters: it lets more of what you eat cross the threshold and actually become usable protein, instead of being deaminated and excreted. Wherever NuMa shows digestible complete protein (DCP) alongside raw protein, the gap between the two is this same effect in numbers.
{: #unusable-protein-fate}

#### Digestion, Synthesis, and Catabolism — the Full Path {: #protein-fate-detail}

*Search terms: protein synthesis, protein breakdown.*

The paragraph above is the practical summary. Here is the fuller mechanism, for readers who want it.

Digestion itself doesn't distinguish complete from incomplete protein. Every protein you eat, regardless of amino acid profile, is broken down by digestive enzymes into free amino acids and small peptides, absorbed across the intestinal wall, and released into the bloodstream, joining the body's general pool of circulating amino acids. The "complete vs. incomplete" distinction only starts to matter at the *next* step.

Building new protein — muscle, enzymes, hormones, anything — requires all nine [EAAs](#gloss-eaa) to be present at once, in roughly the ratio the specific protein being built calls for. The body's protein-building machinery can't substitute one amino acid for another. If a meal's amino acid profile is short on one or more EAAs relative to what's needed, that shortfall — the [limiting amino acid](#gloss-limiting-amino-acid) — caps how much new protein can be built from that meal, no matter how abundant the other eight are.

The body has no storage depot for spare amino acids, the way it stores glucose as glycogen or extra energy as fat. Once the amount usable for building new protein is accounted for, whatever amino acids are left over get broken down for other uses (mostly in the liver, with the branched-chain amino acids handled largely in muscle instead). That breakdown happens in two parts: the nitrogen-containing amino group is stripped off and processed through the urea cycle for excretion in urine (some of it gets recycled into other, nonessential amino acids or into nucleotides and hormones instead); and the leftover carbon skeleton is used to make glucose, converted into ketone bodies, burned directly for energy, or stored as fat if there's a surplus[^110].

**Does this mean every meal needs to be a "complete" protein on its own?** No — and this is where the picture gets more reassuring. The classic reasoning here (Young & Pellett, 1994)[^14] is that the body turns over roughly 250–300 g of its own protein every day, far more than a typical meal provides, and the free amino acid pool released by that ongoing turnover can help fill in whatever a given meal's protein is short on. That's the biochemical basis for the now-standard advice that complementary foods (rice with beans, for instance) don't need to be eaten together at the same meal — pairing them anywhere across a varied day is enough. A 2024 controlled feeding study testing this directly[^15] — comparing meals built from complete, complementary, and single incomplete protein sources, all matched for total protein — found no significant difference in how much new muscle protein was built in the hours afterward, even though the amount of certain EAAs available in the bloodstream did differ between conditions. That suggests the real-world cost of an occasional single incomplete-protein meal may be smaller in practice than the classic model implies, though it's an area of active research rather than settled fact.

None of this changes what NuMa reports: it's still true that, gram for gram, a food or meal with a limiting amino acid yields less usable ([DCP](#gloss-dcp)) protein than its raw protein total. What the research adds is context on the time frame that matters — it's your protein pattern across the day, not any single meal in isolation, that determines how much of what you eat actually becomes usable protein.

#### The DIAAS Score

The Digestible Indispensable Amino Acid Score ([DIAAS](#gloss-diaas)) measures how much of a food's protein your body can actually use. For each [EAA](#gloss-eaa), it calculates:

> (mg of that [EAA](#gloss-eaa) actually absorbed per gram of food protein) ÷ ([FAO](#gloss-fao) reference value for that [EAA](#gloss-eaa))

The word "actually absorbed" is critical. Not all amino acids in a food survive digestion intact and cross into the bloodstream. [DIAAS](#gloss-diaas) uses [ileal digestibility](#gloss-ileal-digestibility) — the fraction of each amino acid absorbed by the end of the small intestine — to correct for this. The result is a score based on what your body actually receives, not merely what was in the food[^16].

A ratio of 1.0 means the food **delivers** exactly the required amount of that [EAA](#gloss-eaa) (per gram of protein eaten). A ratio below 1.0 means a shortfall — that [EAA](#gloss-eaa) is limiting. A ratio above 1.0 means a surplus above the floor. **The overall [DIAAS](#gloss-diaas) score for the food is set by whichever [EAA](#gloss-eaa) has the lowest ratio — the weakest link.**

#### A Concrete Example: Chia Seed

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

#### Summary

| Concept | What it answers |
|---|---|
| [FAO](#gloss-fao) reference values | How many mg of each [EAA](#gloss-eaa) a human needs per gram of protein consumed |
| [DIAAS](#gloss-diaas) ratio for one [EAA](#gloss-eaa) | Does this food deliver enough of that [EAA](#gloss-eaa), accounting for digestibility? |
| Overall [DIAAS](#gloss-diaas) score | What is the weakest link — the most limiting [EAA](#gloss-eaa) in this food? |
| Ratio > 1.0 for all [EAAs](#gloss-eaa) | [Complete protein](#gloss-complete-protein): no amino acid short in the food itself (how much is absorbed is the digestibility question) |
| Daily protein target | Separate calculation: how many grams of protein do you need total? |

The [DIAAS](#gloss-diaas) table characterizes the quality of each gram. Hitting your daily protein target is about counting how many grams you eat.

### B. Plant protein sources in your pantry {: #appendix-plant-proteins}

*Search terms: plant proteins, vegan protein, vegetarian protein.*

("pantry" here has two meanings: your actual pantry, and the pantry [database](#gloss-database) that is in NuMa (see the Foods dropdown menu), which is a list of foods in your actual pantry.)

This appendix profiles the plant protein sources currently kept in a typical [NuMa](#gloss-numa) pantry, including nutritional yeast, which is not a plant but is grouped here because it fills the same dietary role. For each source: what form it takes, where it comes from, its essential amino acid ([EAA](#gloss-eaa)) strengths and weaknesses relative to the [FAO](#gloss-fao) reference values described in [Appendix A](#appendix-protein-quality), and its typical role in cooking.

The [EAA](#gloss-eaa) notes below describe general tendencies for each food, not a substitute for running the food itself through [NuMa](#gloss-numa). Growing conditions, processing, and the specific [USDA](#gloss-usda) or Open Food Facts[^3] record behind a given entry all shift the exact numbers — use [NuMa](#gloss-numa)'s own amino acid ratio and [DIAAS](#gloss-diaas) output for precise figures. Sourcing and cost information for these foods is addressed separately, not here.

*The figures quoted below (checked 14 October 2026) are each food's [USDA](#gloss-usda) record[^2], scored by NuMa against the [FAO](#gloss-fao) 2013 reference values[^16], before digestibility: 1.00 means exactly the reference amount. Where a claim isn't one NuMa can compute (storage, cooking, food safety), it's general food knowledge.*

BEFORE GOING ANY FURTHER: You should know that the two most useful foods below (aside from staples like whole wheat flour) are nutritional yeast and hulled hemp seed. Both are incredibly nutritious and useful. Nutritional yeast adds umami to any food, and hulled hemp seed is invaluable when eating legumes.

#### Seeds

**Chia seeds**

- *Form:* tiny oval seeds, black or mottled gray-brown, about 1mm long.
- *Source:* *Salvia hispanica*, a flowering mint-family plant native to Mexico and Guatemala.
- *[EAA](#gloss-eaa) profile:* unusually complete for a plant seed — as worked through in Appendix A, chia clears all nine [EAA](#gloss-eaa) floors, with lysine as its narrowest margin (1.22× the reference). One of the few standalone-complete plant proteins in this pantry.
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

#### Grains & Pseudocereals

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

#### Tree Nuts & Peanuts

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

#### Soy-Based Foods

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

#### Other Protein Concentrates

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

#### Nutritional Yeast

**Nutritional yeast flakes**

- *Form:* yellow flakes of deactivated, dried yeast. Flakes are less dense than powder, so measure by weight rather than volume when precision matters — a point already flagged in this pantry's notes for this item.
- *Source:* *Saccharomyces cerevisiae*, grown on a sugar-based medium, then deactivated (killed) and dried. Deactivation means it will not leaven anything or grow in the gut, unlike active baker's or brewer's yeast.
- *[EAA](#gloss-eaa) profile:* a good-quality protein for a non-legume source, though not quite complete: in NuMa's built-in profile, methionine + cysteine (0.92) and phenylalanine + tyrosine (0.94) fall just short — the sulfur amino acids being its weak point, as for soy and legumes generally.
- *Culinary role:* usually an addition rather than a primary ingredient — its concentrated umami (glutamate-driven) flavor makes it a savory, cheese-like flavoring for popcorn, pasta, sauces, and roasted vegetables, and it thickens liquids when whisked into a roux-based sauce (as in "nooch" cheese sauce). It can also become a primary ingredient in dishes built around it, such as cashew-and-nutritional-yeast "yeast cheese," where it supplies both flavor and a meaningful protein contribution.
- *Also worth knowing:* most commercial brands are fortified with B12 (and sometimes other B vitamins) — worth checking the label, since this is often the primary reason vegans include it in their diet, independent of its protein content.

### C. Glycemic load (GL) and Blood Glucose Comparison {: #appendix-gl-comparison}

*Search terms: GL accuracy, individual response.*

Glycemic load is a useful approximation, but no single formula-derived figure reliably predicts an individual's blood glucose response to a mixed meal. Three reasons account for this:

- The fat and protein suppression effect varies by person, by degree of insulin resistance, and by the specific foods involved[^89].
- Most published [GI](#gloss-gi) values were measured in subjects with normal glucose tolerance and may not translate directly to someone with diabetes or insulin resistance. NuMa's built-in reference table[^8] does include a separate set of values measured specifically in subjects with impaired glucose tolerance — see [Where GI values come from](#gi) — ([what that group covers](#gi-impaired)), but that set is smaller and doesn't exist for every food, so this caveat still applies whenever only a normal-tolerance value is available.
- Individual glucose responses to identical meals vary substantially between people[^112], and even in the same person on different days: in one study, a single person's measured GI for the same white bread varied more from one test to the next than people varied from each other[^113].

[GL](#gloss-gl) is therefore most reliable when comparing meals of broadly similar composition — two different grain-based breakfasts, for example. When meals differ significantly in fat or protein content, the calculated [GL](#gloss-gl) will understate the difference in actual glycemic impact.

#### Continuous Glucose Monitoring

*Search terms: continuous glucose monitor, glucose monitor.*

The practical gold standard today is continuous glucose monitoring ([CGM](#gloss-cgm)) — devices such as the Dexcom G7 or Libre 3 that measure interstitial glucose every few minutes. A person with diabetes can eat a meal, watch their glucose curve in the accompanying app, and directly compare their own real response across different meal choices over time. No formula approaches this for accuracy in individual prediction.

#### Predictive Apps

*Search terms: glucose prediction, personalized nutrition.*

Research has shown that a machine-learning model trained on [CGM](#gloss-cgm) data, together with blood tests, diet, activity and the gut microbiome, can predict an individual's glucose response to a meal before it is eaten, and that diets chosen from those predictions lowered post-meal glucose[^112]. Some commercial apps (January AI, for one) offer predictions of this kind — effectively personalizing the [GI](#gloss-gi) and [GL](#gloss-gl) concepts. These predictions are probabilistic rather than exact, but they represent the closest available alternative to direct measurement.

#### Clinical Practice Without CGM

*Search terms: carb counting, dietitian.*

For clinical guidance without [CGM](#gloss-cgm), dietitians working with people with diabetes typically use carbohydrate counting combined with qualitative judgment about fat and protein content, rather than relying on [GL](#gloss-gl) as a single summary figure. The American Diabetes Association's nutrition consensus report recommends carbohydrate counting for insulin dosing in type 1 diabetes, and says that for a meal with substantial fat or protein, insulin dosing shouldn't rest on carbohydrate counting alone[^114]. [GL](#gloss-gl) remains a reasonable guide for comparing meals similar in structure, but should not be the deciding number when fat and protein differ significantly between the options being considered.

### D. Why some foods appear only in DIAAS-boosting suggestions {: #comp-appendix}

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

### E. Portion Input Formats {: #portion-formats}

*Search terms: portion formats, how to type amounts.*

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

PIECE COUNT (eggs, slices, tablets)

There is no general count unit (`2 pc` isn't recognized), since NuMa can't know what one weighs. But once a food has a portion for one of it (Food Cache → **Portions**, e.g. "1 large egg", 50 g), you can count it by name — `2 eggs`, `2 large eggs` — or with its shortcut, `2 p1`. If two portions share the name ("1 large egg", "1 small egg"), name the one you mean. See [Data entry](#data-entry) for every form NuMa accepts.

[USDA](#gloss-usda) STANDARD PORTIONS

Many [USDA](#gloss-usda) foods include pre-defined portion sizes (e.g. "1 medium egg", "1 cup sliced"). These are listed at the portion prompt and can be selected by number:

    p1         select USDA portion #1
    p2         select USDA portion #2
    1.5 p1     one-and-a-half times USDA portion #1

You can also type a portion's description (`1 large egg`), a count of it (`3 large eggs`), or just its main word (`2 eggs`) when only one portion has that word.

**`p1`, `p2`, … mean "the food's 1st portion, 2nd portion, …" — position in the list, never the portion's own text.** This trips people up specifically when you add a custom portion (via [Food Cache](#food-cache-web) → **Portions**) and happen to *name* it something like `p1`: that name has no effect on its shortcut number. If it's the fourth portion in the list, its shortcut is `p4`, no matter what you called it. Every screen where you type a `pN` shortcut — Foods, Recipes, Meals — also lists that food's full portion set with the real shortcut number next to each one; check that list before typing `pN`, don't guess from a portion's name. Adding, removing, or reordering portions on a food also renumbers every `pN` that follows the changed spot, so re-check the list after any portion edit, too — see [A food's portion "pN" shortcut points to the wrong portion](#ts-portion-numbering) if a `pN` amount doesn't come out the way you expected.

#### Recipes: Servings Instead of `pN` {: #portions-vs-servings}

*Search terms: recipe servings, servings not pN.*

Every `pN` shortcut above belongs to *foods*. Recipes never have a `p1`, `p2`, … list, and that isn't a missing feature — it's because recipes don't need one.

A food is measured in grams, and `pN` exists purely to hide that gram math: `p1` means "don't make me weigh out 1 medium egg myself, just use the preset." A recipe's native unit, by contrast, is already **servings** — so wherever you enter an amount of a recipe (adding it to a meal, or adding it as a nested ingredient inside another recipe), typing `1 serving` (or `1 srv`) already means exactly that. There's no gram math to shortcut, so there's no `pN` to shortcut it with.

**You can also type a recipe's amount as a weight or a volume** — on a meal page, and when adding a sub-recipe on Edit Recipe. The **Amount** box there (and the Edit box of a recipe already in the meal or recipe) takes servings, with the word — `1.125 srv`, `1 1/8 servings`, `1⅛ srv` — or a weight (`200 g`, `8 oz`, or just `200`: a number on its own is grams, the same as for a food), or a volume (`3/4 c`, `2 T`, `250 ml`), and turns it into servings for you: a weight through what one serving weighs; a volume through the recipe's **Total yield volume**, or, if that's blank, through its **Serving description** when that is a measure such as `2/3 cup` (so `3/4 c` of a sauce whose serving is 2/3 cup logs 1.125 servings). The hint under the box says which of these that recipe can take. If NuMa can't convert what you typed, it says why and adds nothing; a plain number for a recipe whose serving weight NuMa doesn't know is refused that way, with a reminder to type servings. The meal or recipe still records servings, and a recipe already in it shows its amount as, say, `1.5 servings`, so saving the box unchanged keeps it.

That doesn't mean a recipe's per-serving weight is undefined — it's derived automatically from two fields on the Edit Recipe page's Recipe details section: **Number of servings** and **Total yield weight**. Divide one by the other and you get grams per serving, live, the moment both are filled in — nothing extra to set. A recipe with `servings = 21` and `total yield weight = 1942.5 g`, for example, already means "1 serving = 92.5 g" everywhere that recipe is used, without you ever typing 92.5 anywhere.

The one place the literal text `p1` *does* work for a recipe is the [Convert](#convert) tool — type `p1` there for a recipe and it resolves to that same auto-derived "1 serving" weight. That isn't a general recipe feature, though: Convert happens to reuse the same portion-parsing code that handles foods' `pN`, and it treats a recipe's one implicit "1 serving" as if it were portion #1. Everywhere else in the app, just use the Servings field directly.

92.5 g is accurate, but it doesn't say what you're actually holding. If a recipe's serving has a natural real-world name — 1 muffin, 1 cookie, 1 slice — set it in the **Serving description** field, right next to Number of servings on the Edit Recipe page. It's a label, not a unit conversion — with one exception: when it is a measure (`2/3 cup`, `250 ml`), a meal page uses it to turn a volume you type into servings (see above). Once set, it shows up as "(1 serving = 1 muffin)" wherever the recipe's serving count is already shown — the recipe's own page, the Recipes list, Convert's named portion, and next to the Servings field anywhere the recipe is added as an ingredient or meal item.

**Where you see that weight.** Anywhere an amount is given in servings — a recipe added to a meal, or a recipe used as an ingredient inside another recipe (a [sub-recipe](#gloss-sub-recipe)) — NuMa now prints the gram weight beside it, as in "2 servings (500 g)", on screen and on a printed recipe alike. It uses the recipe's stated Total yield weight where you have set one, and otherwise the sum of the ingredients, but only when every ingredient has a usable weight: a partial sum would understate the serving by an unknown amount, so nothing is shown at all in that case.

See also [Recipe Ingredient List](#recipe-ingredients) for where these Servings fields appear, and for the Recipe details fields — including Total yield weight and Total yield volume — on the Edit Recipe page.

OMITTING THE SPACE

For all weight and volume units, the space between the number and unit is optional. These pairs are identical:

    2 T    =   2T
    0.25 c =   0.25c
    150 g  =   150g
    3 oz   =   3oz
    1/4 c  =   1/4c

VOLUME WITH EXPLICIT WEIGHT

When you know both the volume measure and the exact gram weight, you can supply both on one line. NuMa records the weight and labels the entry with the volume for readability:

    2 T 30g         →  30 g  (labeled "30 g (2 T)")
    1/4 c 60 g      →  60 g  (labeled "60 g (1/4 c)")

BARE NUMBER

A bare number with no unit is assumed to be grams; each amount field's example text says so directly.

### F. Worked validation example — meal-level DIAAS for pinto beans + quinoa {: #appendix-diaas-validation}

*Search terms: check the math, verify DIAAS, worked example.*

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

The full table, with how to read it, is in [The reference values](#fao-reference-values) (Part 4, J). The relevant values are:

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

*Search terms: nutrient definitions, what each nutrient does, internal names, column names.*

All the nutrient groups from the Nutrient Analysis table are covered below. Each entry gives a plain-language description of one nutrient NuMa tracks, links to where it's discussed elsewhere in this manual, a link to a respected outside source for anyone who wants to go deeper than a nutrient table can show, and, under **Where to find it**, where to get a value a food is missing. Amino acids aren't repeated here — they already have their own extensive treatment; start at [Essential Amino Acids](#aa).

Each entry ends with the nutrient's **[data key](#gloss-data-key)**, the name NuMa uses for it internally. You never need it to use NuMa; it's there so a technically inclined reader can find the nutrient in the program's data files or code.

---

#### When a food has no data for a nutrient {: #key-sources}

*Search terms: where to find values, data sources.*

A food with no figure for a nutrient adds nothing to a meal's or recipe's total for it, so the total comes out too low. Under [Top Contributors](#top-contributors), the list of foods with no data shows which foods those are, with a **Find this data** button beside each; Foods → 9 lists every food you use that has [missing nutrient data](#data-completeness).

**Try these sources in this order.** Each nutrient's entry below says where it differs.

1. **The same food in [USDA](#gloss-usda)**, in a Foundation or [SR](#gloss-sr) Legacy record — the most complete records there are. Branded USDA records list only what's on the package label. *In NuMa:* **Find this data** (or **Fill in nutrients from another food** on the food's page) searches for the food's own name; pick a USDA match and copy the values it lacks. For a food that is already a USDA food, try **Refresh from USDA** on its page first: USDA sometimes adds values.
2. **Another national food table**: the Canadian Nutrient File (searched online), and the UK CoFID, Australian AFCD and French CIQUAL tables bundled with NuMa. *In NuMa:* the same search covers all four; their codes say which a result came from: CNF (Canadian Nutrient File), [CoFID](#gloss-cofid), [AFCD](#gloss-afcd) and [CIQUAL](#gloss-ciqual).
3. **The package label**, for a packaged food: calories, fat, saturated fat, carbohydrate, sugar, fiber, protein and sodium, and on US labels also calcium, iron, potassium and vitamin D. Open Food Facts holds many labels; the same search includes it (code [OFF](#gloss-off)). A label never lists water, amino acids, carotenoids or most vitamins.
4. **A close, similar food** — tomato purée for a tomato sauce, another bean for a bean. Same search; a value borrowed this way is marked *estimated* on the food's page. A homemade dish is usually better entered as a [recipe](#recipes-menu-web) of its ingredients, so its values come from them.
5. **Claude AI.** On Foods → 9, tick the food's group in *Missing nutrient data* and [fetch the missing values from Claude](#fetch). Last, because the figures need checking: ask for the source and look at it. An import only fills blanks.
6. **Nobody has it.** Some nutrients are measured for few foods anywhere (several phytonutrients, below). Then the honest answer is that the total is a minimum. Marking the gap **not needed**, from the Top Contributors list ([how](#contrib-no-data-answers)) or for its whole group in Foods → 9's *Missing nutrient data* list, stops NuMa asking about it and leaves it out of Claude prompts. The total is still a minimum. If you know the food has none, **Has none — record 0** says so instead.

**Amino acids.**{: #key-sources-aa} The same order, with these differences. USDA SR Legacy has full amino acid profiles for thousands of foods, and the Canadian Nutrient File for many; the Australian table has them for about one food in eight; the UK and French tables have none, and labels never list them. When you copy amino acids from a similar food, NuMa scales them to this food's own protein rather than copying them raw (see [Fill in nutrients from another food](#review-incoming)). A food with very little protein can simply be marked **Amino acids not needed** (see [Missing Amino Acid Profiles](#missing-aa-off)).

---

#### Macronutrients

*Search terms: macros.*

**The indentation below shows the real parent/child relationship among these** — Calories, Protein, Carbohydrates, and Fat are the four independent top-level macronutrients (none is a subset of another); Carbohydrates and Fat each break down further into the sub-rows nested beneath them. NuMa's own nutrient tables (food, recipe, meal, and daily-summary pages, plus the printable report) show this same hierarchy visually too — Fiber, Sugar, and the three fat types are indented under their parent row, the way a Nutrition Facts label does (completed 2026-09-19, see [Part 9](#nesting-carb-subtypes)).

##### Calories {: #key-calories}
The energy a food provides, from protein, carbohydrate, fat, and alcohol combined. NuMa estimates your personal daily calorie target using the Mifflin-St Jeor equation and your activity level — see [Daily Nutrient Goals](#goals) for the full calculation and the [RDA](#gloss-rda)/[DRI](#gloss-dri) framework it draws on[^9].

**Where to find it:** the [usual order](#key-sources); every food table and label has it. A food with protein, carbohydrate and fat but no calories doesn't need a source: NuMa works them out from those three and marks the figure *estimated* (see [food data problems](#calorie-checks)).

**[Data key](#gloss-data-key):** *calories*

##### Protein {: #key-protein}
Builds and repairs every cell in the body and is the nutrient NuMa focuses on most closely, since how much of it your body can actually *use* depends on both digestibility and amino acid completeness, not just the gram total on a label. See [Digestible Complete Protein](#dcp) and [Essential Amino Acids](#aa) for how NuMa scores protein quality beyond this raw figure, and [Recommended Dietary Allowances](#rda) for how your target is set. External: MedlinePlus, *Dietary Proteins*[^17].

**Where to find it:** the [usual order](#key-sources); every food table has it.

**[Data key](#gloss-data-key):** *protein_g*

##### Carbohydrates {: #key-carbs}
The body's primary energy source. **Fiber and Sugar below are subsets of this total, not additional to it** — Fiber + Sugar + Starch + a few minor carbohydrate types add up to the Carbohydrates figure, the same relationship a Nutrition Facts label shows by indenting "Dietary Fiber" and "Total Sugars" under "Total Carbohydrate." NuMa uses carbohydrate content, alongside a food's glycemic index, to compute [Glycemic Load](#gl). External: MedlinePlus, *Carbohydrates*[^18].

**Where to find it:** the [usual order](#key-sources); every food table has it. **Watch the definition:** USDA's and the Canadian figure include fiber, but the UK, Australian and French tables give *available* carbohydrate, with fiber left out, so their figure runs lower by the food's fiber. Copying one from those three, add the fiber back if you want it to match USDA's.

**[Data key](#gloss-data-key):** *carbs_g*

- **Fiber**{: #key-fiber} — The indigestible part of plant carbohydrate. NuMa's figure is [USDA](#gloss-usda)'s "total dietary fiber" — **soluble and insoluble combined**, not insoluble alone. The two behave differently: soluble fiber (oats, beans, apples, citrus) dissolves into a gel that slows digestion and is linked to lower cholesterol and better blood-sugar control; insoluble fiber (whole grains, vegetable skins, wheat bran) adds bulk and speeds transit, supporting digestive regularity. NuMa doesn't split the two because USDA FoodData Central only reports that breakdown for a small fraction of foods — reliably showing it would mean leaving it blank almost everywhere. Fiber is one of the few macronutrients using an Adequate Intake rather than a full [RDA](#gloss-rda) — see [Daily Nutrient Goals](#goals) for what that distinction means for your target. External: MedlinePlus, *Dietary Fiber*[^20].
    - **Where to find it:** the [usual order](#key-sources). The UK table has it for only about half its foods; the others for nearly all.
    - **[Data key](#gloss-data-key):** *fiber_g*
- **Sugar**{: #key-sugar} — Simple carbohydrate — both naturally occurring (fruit, dairy) and added (sweeteners) — that NuMa reports as one combined total. High-sugar foods tend to raise [Glycemic Load](#gl) sharply; see that section for how NuMa weighs sugar's blood-glucose impact against a food's fiber and overall carbohydrate. External: MedlinePlus, *Sweeteners – Sugars*[^21].
    - **Where to find it:** the [usual order](#key-sources); nearly every table and label has it.
    - **[Data key](#gloss-data-key):** *sugar_g*
- *Starch is not tracked as its own row — USDA rarely reports it as a distinct value, so it stays folded into the Carbohydrates total along with everything else that isn't Fiber or Sugar.*

##### Fat {: #key-fat}
Total dietary fat. **Saturated, Monounsaturated, and Polyunsaturated fat below are subsets of this total, not additional to it** — the three add up to (approximately) the Fat figure. Fat itself sits at the same level as Protein and Carbohydrates above, not beneath them — it's a third independent macronutrient, not a subset of either. See [Omega-3 Fatty Acids](#omega3) for the specific unsaturated fatty acids NuMa tracks individually and gives their own goals. External: MedlinePlus, *Dietary fats explained*[^19].

**Where to find it:** the [usual order](#key-sources); every food table and label has it.

**[Data key](#gloss-data-key):** *fat_g*

- **Saturated fat**{: #key-saturated-fat} — The fat subtype most consistently linked to cardiovascular risk when eaten in excess; most dietary guidance favors keeping intake low and replacing it with unsaturated fat where possible. External: Examine.com, *Saturated Fat*[^22].
    - **Where to find it:** the [usual order](#key-sources); labels give it too.
    - **[Data key](#gloss-data-key):** *saturated_fat_g*
- **Monounsaturated fat**{: #key-mono-fat} — Found mainly in olive oil, avocados, and many nuts; generally considered neutral-to-beneficial for cardiovascular health when it displaces saturated fat in the diet. External: MedlinePlus, *Dietary fats explained*[^19].
    - **Where to find it:** the [usual order](#key-sources), but not from a label; about three foods in four in the UK and French tables have it.
    - **[Data key](#gloss-data-key):** *mono_fat_g*
- **Polyunsaturated fat**{: #key-poly-fat} — Includes the omega-3 and omega-6 fatty acids NuMa tracks individually — see [Omega-3 Fatty Acids](#omega3) for [ALA](#gloss-ala), [EPA](#gloss-epa), [DHA](#gloss-dha), and linoleic acid specifically, and why ALA is the only one with an official intake goal. External: MedlinePlus, *Dietary fats explained*[^19].
    - **Where to find it:** the [usual order](#key-sources), but not from a label; about three foods in four in the UK and French tables have it.
    - **[Data key](#gloss-data-key):** *poly_fat_g*

---

#### Water

*Search terms: hydration, fluids, fluid intake.*

##### Water {: #key-water}
The water a food or drink contains, measured as its moisture. NuMa adds it up from everything you log, and splits a meal's or day's total into **Water from drinks** (from foods and recipes marked as a drink) and **Water from food** (everything else); the split isn't stored with a food, so a food's own figure is just its water. See [Water: from drinks and from food](#water) for the goals and what counts as water.

**Where to find it:** the [usual order](#key-sources), and almost always at step 1 or 2: [USDA](#gloss-usda), the Canadian Nutrient File and the UK and Australian tables have it for nearly every food, the French table for most. Labels never list it, so a packaged food needs a matching generic food (a jarred tomato sauce takes a USDA or [CIQUAL](#gloss-ciqual) tomato sauce's value). For all your USDA foods at once, Foods → 9 fills it in from USDA (see [Gaps in the data](#water-gaps)). Make sure the match is in the same state: a dry food (flour, powder, dried beans) has very little water, and the same food cooked or soaked a lot (see [A wet food picked for a dry one](#water-wet-dry)).

**[Data keys](#gloss-data-key):** *water_g*; the drinks/food split is *water_drinks_g* and *water_food_g*

---

#### Omega Fatty Acids

*Search terms: fish oil, essential fatty acids, PUFA.*

**Grouped below by fatty acid family (omega-3 vs. omega-6) — a real biochemical classification, but not a sum like Carbohydrates/Fat above:** there's no single "total omega-3" figure these three add up to; [ALA](#gloss-ala), [EPA](#gloss-epa), and [DHA](#gloss-dha) are each reported and goal-tracked independently. See [Omega-3 Fatty Acids](#omega3) for the full discussion, including why only ALA has an official intake goal and how the ALA→EPA→DHA conversion pathway works. External (covers this entire group): Linus Pauling Institute, *Essential Fatty Acids*[^23].

##### Omega-3

- **[ALA](#gloss-ala)**{: #key-ala} — Alpha-linolenic acid, the plant-based omega-3 (flaxseed, walnuts, chia, canola and soy oils). The only omega-3 with an official Adequate Intake, so it's the only one of the three with a Daily Goal.
    - **Where to find it:** [USDA](#gloss-usda) Foundation and [SR](#gloss-sr) Legacy records, the Canadian Nutrient File and the Australian table; the French table for about half its foods; not the UK table as bundled, and never a label. Then Claude, as in the [usual order](#key-sources).
    - **[Data key](#gloss-data-key):** *omega3_ala_mg*
- **[EPA](#gloss-epa)**{: #key-epa} — Eicosapentaenoic acid. No U.S. [DRI](#gloss-dri) exists for EPA on its own; the body makes some from ALA, inefficiently, or gets it directly from fish, algae, and other seafood. Set your own [Revised Optimal target](#optimal) if you want to track it against a number.
    - **Where to find it:** USDA Foundation and SR Legacy records, the Canadian Nutrient File and the Australian table; the French table for about half its foods; not the UK table as bundled, and never a label. Then Claude, as in the [usual order](#key-sources). A plant food missing EPA has essentially none: EPA comes from fish, seafood and algae.
    - **[Data key](#gloss-data-key):** *omega3_epa_mg*
- **[DHA](#gloss-dha)**{: #key-dha} — Docosahexaenoic acid, the omega-3 most concentrated in the brain and retina. Like EPA, it has no official DRI and can be tracked against a self-set [Revised Optimal target](#optimal) instead.
    - **Where to find it:** USDA Foundation and SR Legacy records, the Canadian Nutrient File and the Australian table; the French table for about half its foods; not the UK table as bundled, and never a label. Then Claude, as in the [usual order](#key-sources). A plant food missing DHA has essentially none: DHA comes from fish, seafood and algae.
    - **[Data key](#gloss-data-key):** *omega3_dha_mg*

##### Omega-6

- **Linoleic acid (LA)**{: #key-la} — The essential omega-6 fatty acid. Has a Daily Goal, its Adequate Intake (17 g men, 12 g women under 51); that figure is the typical U.S. intake, and deficiency is essentially unknown on ordinary diets — see [Omega-3 Fatty Acids](#omega3).
    - **Where to find it:** [USDA](#gloss-usda) Foundation and [SR](#gloss-sr) Legacy records, the Canadian Nutrient File and the Australian table; the French table for about half its foods; not the UK table as bundled, and never a label. Then Claude, as in the [usual order](#key-sources).
    - **[Data key](#gloss-data-key):** *omega6_la_mg*

---

#### Minerals

*Search terms: electrolytes, trace elements.*

**Grouped below by the standard nutrition-science split between macrominerals (needed in gram-per-day amounts) and trace minerals (needed in milligram or microgram amounts)** — a categorical family, like Omega-3 vs. Omega-6 above, not a sum relationship.

##### Macrominerals

- **Calcium**{: #key-calcium} — Builds and maintains bone, and supports nerve and muscle function. A major dietary source for many people (dairy, fortified plant milks, leafy greens) is undermined by [oxalates](#antinutrients) in some of those same leafy greens — spinach's labeled calcium is largely unabsorbed. External: Linus Pauling Institute, *Calcium*[^24].
    - **Where to find it:** the [usual order](#key-sources); US labels give it too.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: mainly a supplement risk, not a food risk — getting this much from food alone is difficult. [NIH](#gloss-nih) notes higher-dose calcium supplements are linked to a greater risk of kidney stones, and some research ties them to a higher risk of cardiovascular disease[^48].
    - **[Data key](#gloss-data-key):** *calcium_mg*
- **Magnesium**{: #key-magnesium} — Involved in hundreds of enzyme reactions, including energy production and muscle/nerve function. A candidate for a future [Revised Optimal](#optimal) target above the [RDA](#gloss-rda) — see [Part 9](#expand-revised-optimal) — though the evidence for a specific above-RDA number is less settled than for vitamin D. External: Linus Pauling Institute, *Magnesium*[^25].
    - **Where to find it:** the [usual order](#key-sources), but not from a label.
    - **[Data key](#gloss-data-key):** *magnesium_mg*
- **Phosphorus**{: #key-phosphorus} — Works alongside calcium in bone structure and is also central to cellular energy (ATP). Deficiency is rare in any diet with adequate protein, since phosphorus is present in most protein-rich foods. External: Linus Pauling Institute, *Phosphorus*[^26].
    - **Where to find it:** the [usual order](#key-sources), but not from a label.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: NIH notes high intakes seldom cause problems in otherwise healthy people; the real concern is chronic kidney disease, where the kidneys can't clear excess phosphorus and it builds up in the blood, worsening bone and kidney health[^49].
    - **[Data key](#gloss-data-key):** *phosphorus_mg*
- **Potassium**{: #key-potassium} — Supports fluid balance, nerve signaling, and healthy blood pressure; typically under-consumed relative to its Adequate Intake in a typical Western diet. External: Linus Pauling Institute, *Potassium*[^27].
    - **Where to find it:** the [usual order](#key-sources); US labels give it too.
    - **[Data key](#gloss-data-key):** *potassium_mg*
- **Sodium**{: #key-sodium} — The one nutrient in NuMa's tables with its own Maximum column entry rather than a Minimum — see [Recommended Dietary Allowances](#rda) for the Maximum-vs-UL distinction and [Maximum Nutrient Limits](#maxlimits) for how NuMa flags approaching it. External: Linus Pauling Institute, *Sodium*[^28].
    - **Where to find it:** the [usual order](#key-sources); every table and label has it. A label that gives salt instead: sodium is salt ÷ 2.5 (1 g salt = 400 mg sodium).
    - **[Data key](#gloss-data-key):** *sodium_mg*

##### Trace Minerals

- **Iron**{: #key-iron} — Carries oxygen in red blood cells. Plant (non-heme) iron absorbs far less efficiently than animal (heme) iron and is further blocked by [phytates](#antinutrients) — NuMa raises the iron [RDA](#gloss-rda) target 1.8× on a Vegetarian or Plant-based dietary preference to reflect this; see [Diet-Aware Bioavailability Notes](#diet-bioavailability)[^4]<sup>,</sup>[^5]. External: Linus Pauling Institute, *Iron*[^29].
    - **Where to find it:** the [usual order](#key-sources); US labels give it too.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: acute overdose (often accidental, in children) can cause severe gastrointestinal damage and organ failure; chronically, people with hemochromatosis (an inherited iron-overload condition) should avoid iron and vitamin C supplements, since excess iron builds up and can damage the liver and heart[^50].
    - **[Data key](#gloss-data-key):** *iron_mg*
- **Zinc**{: #key-zinc} — Supports immune function and wound healing; absorption is reduced by the same [phytates](#antinutrients) that affect iron. NuMa raises the zinc RDA target 1.5× on a Vegetarian or Plant-based preference — see [Diet-Aware Bioavailability Notes](#diet-bioavailability)[^4]<sup>,</sup>[^6]. External: Linus Pauling Institute, *Zinc*[^30].
    - **Where to find it:** the [usual order](#key-sources), but not from a label; the French table has it for about two foods in three.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: nausea, vomiting, and gastric distress in the short term. Sustained high doses interfere with copper absorption, which can itself cause neurological problems (loss of coordination, numbness, weakness) if it leads to copper deficiency[^51].
    - **[Data key](#gloss-data-key):** *zinc_mg*
- **Iodine**{: #key-iodine} — Required for thyroid hormone production. Iodized salt is the primary dietary source in most Western diets; those avoiding it (and not eating much seafood or dairy) are the main deficiency risk group. External: Linus Pauling Institute, *Iodine*[^31].
    - **Where to find it:** Often missing. The Australian table has it for every food, the UK table for about half and the French for about a third; USDA records rarely have it and the Canadian file doesn't. Outside NuMa, the [USDA](#gloss-usda), FDA (Food and Drug Administration) and [NIH](#gloss-nih) *Database for the Iodine Content of Common Foods* covers US foods; take a value from it to Claude or a similar food. Then the [usual order](#key-sources).
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: ironically similar to deficiency — high intakes can trigger goiter and thyroid gland inflammation. Very large single doses (gram-range, essentially unreachable from food) can cause burning of the mouth and throat, fever, and vomiting[^52].
    - **[Data key](#gloss-data-key):** *iodine_mcg*
- **Selenium**{: #key-selenium} — An antioxidant-supporting trace mineral; Brazil nuts are an unusually concentrated source (a couple a day can exceed the daily target). External: Linus Pauling Institute, *Selenium*[^32].
    - **Where to find it:** the [usual order](#key-sources), but not from a label; the UK table has it for about three foods in five, the French for about one in three.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: chronic over-intake causes selenosis — hair loss, brittle nails, a garlic odor on the breath, and nausea are the classic signs; very high intakes can affect the nervous system and, rarely, the heart[^53].
    - **[Data key](#gloss-data-key):** *selenium_mcg*

---

#### Vitamins

*Search terms: multivitamin, B vitamins.*

**Grouped below by the standard fat-soluble vs. water-soluble split** — fat-soluble vitamins are stored in body fat and can build up to toxic levels with excess supplementation; water-soluble vitamins are not stored the same way and excess is typically excreted in urine (vitamin B6 is a partial exception at very high supplemental doses). Again a categorical family, not a sum relationship.

##### Fat-Soluble

- **Vitamin A**{: #key-vitamin-a} — Supports vision, immune function, and cell growth. NuMa's figure is already expressed in mcg RAE (Retinol Activity Equivalents) — [USDA](#gloss-usda)'s own standardized unit that converts provitamin-A carotenoids (see Beta-carotene and Alpha-carotene under Phytonutrients below) into vitamin-A-equivalent amounts using their own conversion factors, not a simple sum. External: Linus Pauling Institute, *Vitamin A*[^33].
    - **Where to find it:** the [usual order](#key-sources), with a caution: the Canadian and French figures in NuMa count only retinol, the animal form, so for a plant food they understate it, often to zero. For a plant food prefer USDA, the UK or the Australian table.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9] (that UL applies to preformed vitamin A specifically, a narrower figure than the mcg RAE total NuMa tracks — see the note there; [NIH](#gloss-nih) notes there's no established UL for beta-carotene and other provitamin-A carotenoids).
    - Risk of excess: getting too much preformed vitamin A (usually from supplements, liver, or certain medicines, rarely from food alone) can cause headache, blurred vision, nausea, dizziness, and coordination problems; long-term excess is also linked to reduced bone strength and, in pregnancy, to birth defects[^54].
    - **[Data key](#gloss-data-key):** *vitamin_a_mcg*
- **Vitamin C**{: #key-vitamin-c} — An antioxidant vitamin also needed for collagen synthesis; notably, vitamin C consumed at the same meal significantly improves absorption of non-heme iron from plant foods — see [Antinutrients](#antinutrients). External: Linus Pauling Institute, *Vitamin C*[^34].
    - **Where to find it:** the [usual order](#key-sources); the French table has it for about half its foods.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: mostly mild — diarrhea, nausea, and stomach cramps at high intakes. In people with hemochromatosis (an iron-overload condition), high-dose vitamin C can worsen iron overload and tissue damage[^55].
    - **[Data key](#gloss-data-key):** *vitamin_c_mg*
- **Vitamin D**{: #key-vitamin-d} — Supports calcium absorption and bone health. NuMa's built-in [Revised Optimal](#optimal) default goes above the standard [RDA](#gloss-rda) based on Endocrine Society guidance[^12] — see that section for why. External: Linus Pauling Institute, *Vitamin D*[^35].
    - **Where to find it:** the [usual order](#key-sources); US labels give it too. Often missing for plant foods because there's almost none to measure; mushrooms grown under ultraviolet (UV) light are the exception, and a fortified food's label has it.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: essentially a supplement-only risk (sun exposure and food don't cause it). Excess vitamin D drives calcium too high in the blood (hypercalcemia) and urine, which in turn can cause nausea, weakness, and mineral deposits in soft tissue and blood vessels[^56].
    - **[Data key](#gloss-data-key):** *vitamin_d_mcg*
- **Vitamin E**{: #key-vitamin-e} — An antioxidant vitamin that protects cell membranes from oxidative damage; found concentrated in nuts, seeds, and vegetable oils. External: Linus Pauling Institute, *Vitamin E*[^36].
    - **Where to find it:** the [usual order](#key-sources); the French table rarely has it.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: a supplement-only risk — NIH notes no adverse effects from vitamin E in food, only from high-dose supplements. The main concern is bleeding risk, since high doses reduce the blood's ability to clot; this is especially relevant alongside blood-thinning medication like warfarin[^57].
    - **[Data key](#gloss-data-key):** *vitamin_e_mg*
- **Vitamin K**{: #key-vitamin-k} — Needed for blood clotting and bone metabolism. NuMa tracks vitamin K1 (from the RDA); vitamin K2, a distinct form with separate emerging research on cardiovascular and bone benefits, is not yet reflected in an official [DRI](#gloss-dri) — see [Part 9](#expand-revised-optimal) for that as a candidate future addition. External: Linus Pauling Institute, *Vitamin K*[^37].
    - **Where to find it:** USDA [SR](#gloss-sr) Legacy and the Canadian Nutrient File; the French table for about a third of its foods; the UK table rarely and the Australian not at all. Then Claude, as in the [usual order](#key-sources).
    - **[Data key](#gloss-data-key):** *vitamin_k_mcg*

##### Water-Soluble

- **Thiamin (B1)**{: #key-thiamin} — Needed for converting food into energy and for nerve function. Deficiency (beriberi) is rare in a varied diet but historically arose in populations relying heavily on unenriched white rice. External: Linus Pauling Institute, *Thiamin*[^38].
    - **Where to find it:** the [usual order](#key-sources), but not from a label (except an enriched or fortified food's).
    - **[Data key](#gloss-data-key):** *thiamin_mg*
- **Riboflavin (B2)**{: #key-riboflavin} — Supports energy production and functions as an antioxidant; widely available in dairy, eggs, meat, and fortified grains, so deficiency is uncommon. External: Linus Pauling Institute, *Riboflavin*[^39].
    - **Where to find it:** the [usual order](#key-sources), but not from a label (except an enriched or fortified food's).
    - **[Data key](#gloss-data-key):** *riboflavin_mg*
- **Niacin (B3)**{: #key-niacin} — Involved in energy metabolism and [DNA](#gloss-dna) repair. Corn-based diets can carry a deficiency risk (pellagra) unless the corn is nixtamalized — see **Bound niacin** under [Antinutrients](#antinutrients). External: Linus Pauling Institute, *Niacin*[^40].
    - **Where to find it:** the [usual order](#key-sources), but not from a label (except an enriched or fortified food's).
    - **[Data key](#gloss-data-key):** *niacin_mg*
- **Vitamin B6**{: #key-b6} — Involved in amino acid metabolism and neurotransmitter synthesis. One of the few water-soluble vitamins where very high long-term supplemental doses (not food intake) carry a real toxicity risk (nerve damage). External: Linus Pauling Institute, *Vitamin B6*[^41].
    - **Where to find it:** the [usual order](#key-sources), but not from a label.
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: people almost never get too much B6 from food. Taking high-dose supplements for a year or longer can cause severe, sometimes irreversible nerve damage (loss of control of body movements), along with painful skin patches and extreme sun sensitivity[^58].
    - **[Data key](#gloss-data-key):** *b6_mg*
- **Folate**{: #key-folate} — Essential for cell division and DNA synthesis; especially critical before and during early pregnancy to prevent neural tube defects. External: Linus Pauling Institute, *Folate*[^42].
    - **Where to find it:** the [usual order](#key-sources); the French table has it for about two foods in five.
    - **[Data key](#gloss-data-key):** *folate_mcg*
- **Vitamin B12**{: #key-b12} — Needed for nerve function and red blood cell formation. Almost exclusively animal-sourced[^7] — NuMa shows a specific low-intake warning on a Plant-based only dietary preference; see [Diet-Aware Bioavailability Notes](#diet-bioavailability). External: Linus Pauling Institute, *Vitamin B12*[^43].
    - **Where to find it:** the [usual order](#key-sources). An unfortified plant food missing it has essentially none; a fortified one (plant milk, nutritional yeast, cereal) has it on its label.
    - **[Data key](#gloss-data-key):** *b12_mcg*

---

#### Phytonutrients

*Search terms: phytochemicals.*

**Grouped below into carotenoids (a defined chemical family) vs. everything else** — again categorical, not a sum. Phytonutrients have no established Dietary Reference Intake, so none of these show a "% of daily target" figure the way vitamins and minerals do — see [Recommended Dietary Allowances](#rda).

##### Carotenoids

- **Beta-carotene**{: #key-beta-carotene} — A provitamin-A carotenoid (orange/red pigment in carrots, sweet potatoes, squash); the body converts it to vitamin A, feeding into the Vitamin A (RAE) figure above via [USDA](#gloss-usda)'s own conversion factor rather than a simple sum.
    - **Where to find it:** USDA, the Australian table, the UK table (whose figure is total carotene) and the French table for about half its foods. Then Claude, as in the [usual order](#key-sources). Foods that aren't orange, red or green have little.
    - **[Data key](#gloss-data-key):** *beta_carotene_mcg*
- **Alpha-carotene**{: #key-alpha-carotene} — A second provitamin-A carotenoid, generally present alongside beta-carotene in orange vegetables, converted to vitamin A less efficiently.
    - **Where to find it:** Mostly USDA Foundation and [SR](#gloss-sr) Legacy records; the Australian table for about two foods in three; not the other tables. Often measured nowhere: step 6 of the [usual order](#key-sources) is a fair answer.
    - **[Data key](#gloss-data-key):** *alpha_carotene_mcg*
- **Lycopene**{: #key-lycopene} — The red carotenoid in tomatoes and watermelon; unlike the two above, it has no vitamin A activity — it's tracked purely for its own antioxidant interest.
    - **Where to find it:** Almost only USDA Foundation and SR Legacy records. Only red foods (tomato, watermelon, pink grapefruit, guava) have much, so a missing value elsewhere is usually near zero; for a tomato product, a USDA tomato match is worth finding.
    - **[Data key](#gloss-data-key):** *lycopene_mcg*
- **Lutein + Zeaxanthin**{: #key-lutein} — Carotenoids concentrated in the retina, where they're associated with eye health; found in leafy greens, corn, and eggs. Also no vitamin A activity. External (covers all four carotenoids above): Linus Pauling Institute, *Carotenoids*[^45].
    - **Where to find it:** Almost only USDA Foundation and SR Legacy records. Often measured nowhere: step 6 of the [usual order](#key-sources) is a fair answer.
    - **[Data key](#gloss-data-key):** *lutein_zeaxanthin_mcg*

##### Other Phytonutrients

- **Choline**{: #key-choline} — Needed for cell membrane structure and neurotransmitter synthesis; a meaningful share of adults fall short of even its Adequate Intake — a candidate for a future [Revised Optimal](#optimal) target, see [Part 9](#expand-revised-optimal). External: Linus Pauling Institute, *Choline*[^44].
    - **Where to find it:** [USDA](#gloss-usda) [SR](#gloss-sr) Legacy and Foundation records and the Canadian Nutrient File only; none of the other tables or labels. Then Claude, as in the [usual order](#key-sources).
    - Has a built-in Tolerable Upper Intake Level (UL) — see [Maximum Nutrient Limits](#maxlimits)[^9].
    - Risk of excess: a fishy body odor is the classic tell (from a choline metabolite excreted in sweat and urine); [NIH](#gloss-nih) also lists low blood pressure, sweating, and liver damage at high intakes, with some research linking very high intakes to cardiovascular risk[^59].
    - **[Data key](#gloss-data-key):** *choline_mg*
- **Beta-sitosterol**{: #key-beta-sitosterol} — A plant sterol structurally similar to cholesterol; dietary intake is associated with modestly lower [LDL](#gloss-ldl) cholesterol. External: Linus Pauling Institute, *Phytosterols*[^47].
    - **Where to find it:** USDA only, and for few foods (nuts, seeds, oils, legumes mainly). Usually measured nowhere: step 6 of the [usual order](#key-sources) is a fair answer.
    - **[Data key](#gloss-data-key):** *beta_sitosterol_mg*
- **Isoflavones**{: #key-isoflavones} — Plant compounds with mild estrogen-like activity, found mainly in soy; frequently discussed in the context of soy's role in a plant-based diet. External: Linus Pauling Institute, *Soy Isoflavones*[^46].
    - **Where to find it:** USDA, for soy foods mainly; outside NuMa, USDA's separate *Database for the Isoflavone Content of Selected Foods* is the standard source, worth giving to Claude. A food without soy or other legumes has essentially none.
    - **[Data key](#gloss-data-key):** *isoflavones_mg*

---

## Part 11 — Recent program updates log {: #updates-log}

*(Reading time: 1 hour, 9 minutes)*


<!-- "Aside from being an update log for the user to access, this section is also used by create_release.py when a release is cut. New dated entries go below the "Insert new updates below here" marker, under today's "#### Month Day updates" heading and beneath the running "#### Next release summary to this point" heading, which sits directly under the marker and above the dated entries; each entry starts with MANUAL: or PROGRAM:, and each also gets a one-line bullet added under that running heading. At release time, create_release.py takes everything between the marker and the nearest "#### Release ... summary" heading as that release's notes, and renames that "Next release summary to this point" heading in place to "#### Release <tag> summary" -- the entries themselves are never rewritten or moved, so the running summary simply becomes that release's summary. The "(dated details below)" suffix is appended only when dated entry sections actually follow the summary. On the release page itself the running heading reads "#### Summary" instead, since work that is "next" in the manual is exactly what that release shipped (create_release.py rewrites that one line in the notes it sends, not in the manual). Once a release is cut, its notes are copied into the GitHub release body permanently -- nothing re-reads the manual afterward, so anything below a release summary heading is safe to prune anytime; it can't retroactively change a past release's notes."-->
<!-- # "If there is nothing pending under the marker at release time, create_release.py falls back to the generic "Automated build from main." message instead of real notes." -->

Program updates, and major manual updates, are logged here. They are grouped by program release dates.

Each entry has a bold-font title and a plain-language description — anywhere from one sentence to a short paragraph — of what you can now do or what changed.

<!-- Many entries also carry a fenced "Scope:" block underneath, with the technical detail (menu path, files touched, root cause). It is developer-facing only: the next comment explains why it is wrapped in an HTML comment and therefore never reaches a reader of the built manual. -->
<!-- Scope blocks below are hidden from the rendered manual (and from GitHub's rendered release notes, which pull this section verbatim -- see scripts/create_release.py) for the reason above: they're developer-facing detail with no value to the average user reading the Recent program updates log. Left visible only in this markdown source for anyone editing it. -->
<!-- Insert new updates below here -->

#### Next release summary to this point (dated details below)

Version overview: GI processing and GL (glycemic load) calculation and analysis fully implemented, including an estimated GI for meals and recipes. Water intake from drinks and food now fully tracked. Daily Summary can add up every nutrient for any date range or chosen meals, and show days in blocks. Vitamin K from USDA corrected: it had been read from the wrong USDA figure, so most foods showed little or none, and Foods 9 now fixes foods saved earlier in one click. Protein complement suggestions reworked to count each food at its own digestibility and stay within a sensible amount per meal, and meal and day pages now check each meal against the amount of protein per meal that research recommends for building and keeping muscle, based on your weight and age. Many interface improvements and bug fixes.

- **126.** Buttons now have a blue outline, and a button that acts on what's in the box beside it turns solid blue once there's something there to act on, as **Create Meal** always has (on Meals & Log: **Show** and **Calculate**).
- **125.** Search meal history, now on its own line on Meals & Log, can also list every meal that *doesn't* contain a food or recipe, and takes a cached food's bare FDC ID number as well as a name or code.
- **124.** MANUAL: Weekly sweep — the Glossary now explains EFSA, seven more sections are found by everyday words (hydration, fish oil, versus...), the Annotate section describes its **DIAAS needed** button, and the updates log is trimmed to the last two weeks.
- **123.** Merging duplicate foods (Foods → 9 → **Find duplicate foods**) now first shows any values or portions the copies being deleted have that the kept one lacks or has differently, with your own edits marked and preselected, so nothing you corrected is lost; and a food can no longer end up in your pantry twice.
- **122.** MANUAL: The manual now uses American spelling throughout (labeled, liters, color, fiber, license); published titles quoted in the notes keep their own spelling.
- **121.** MANUAL: The manual's search now finds about 200 more sections by everyday words they don't use themselves, such as *food diary* for Meals & Log, *salt* for sodium, *fish oil* for omega-3s, or *prediabetes*.
- **120.** MANUAL: The manual's *Search terms* lines no longer show on the page; the manual's search still finds sections by them, and says so when that's how a section matched.
- **119.** **Today's summary** on Daily Summary, with no meals logged yet today, now says so beside the button.
- **118.** A day's full analysis is now one page, whether you open it from a meal (**Analyze full day**) or from Daily Summary, and it has every analysis section a meal page has, pooled over the day: Top Contributors, Missing Amino Acid Profiles and Anti-nutrients are new there.
- **117.** MANUAL: Searching the manual for *older people*, *seniors*, *over 65* or *over-65* now finds every section about older people's needs.
- **116.** The Settings section shortcuts (**Alt+Shift+1** to **Alt+Shift+0**) now work; they had been passed to the browser, which in Firefox switched to the first tab instead.
- **115.** **Alt+Shift+I** puts the cursor in the page's search box, on every page that has one (a meal, a recipe, Foods: Search, Pantry, Food Cache, Compare and more).
- **114.** Save buttons that never lit up when you typed in their boxes now do: a complement suggestion's **Save limit for this food**, Settings' nutrient-target rows, and a food's portion rows; on the Annotate page the right button (**Save annotation**) now lights up.
- **113.** The "Added ..." line after adding a food or recipe to a meal or recipe now says how much was added, with its weight in grams.
- **112.** A food's Annotate page now always opens at its top, with the cursor in the GI box when the food has no GI yet; when it has a GI but no DIAAS, a **DIAAS needed, click to go there** button takes you straight to the DIAAS box.
- **111.** A food with no GI anywhere and very little carbohydrate, such as hemp seed: the manual now explains how to save a labeled estimate, and the Annotate page's "No matches found" advice now recommends one instead of "Don't prompt me", which left glycemic load incomplete.
- **110.** Opening **Add Food or Recipe** or **Add Ingredient** puts the cursor in its search box; after a search the cursor goes to the first result's amount, and stays put — page and all — when the online results arrive.
- **109.** On Compare, a food that has portions can now be given its amount as a number of one of them (2 × 1 slice) as well as in grams.
- **108.** Compare has a **Clear the list and start over** button beside Search, to start a new comparison.
- **107.** Search meal history now takes a code too: U171477 or R21 lists every meal that food or recipe is in.
- **106.** List filters now take a code as well as a name: R21 on the Recipes list, U171477 on Food Cache, Annotate and My Pantry, and either on the Food Use pages.
- **105.** Compare now shows a recipe's serving description ("1 muffin") beside its serving weight, and under its name in the nutrient table when servings are compared.
- **104.** Compare's per-100 g figures for a recipe now use the recipe's own total weight when it has one, the weight of the finished dish, instead of always adding up the raw ingredients.
- **103.** On Compare, a recipe that has a weight per serving can now be given its amount in grams as well as servings.
- **102.** Compare now has a Contents list down the side, and its two Show comparison buttons say which amounts they show, with the one matching your amounts in blue.
- **101.** Adding a search result to a meal, a recipe or your pantry now leaves the search results showing, so you can add several from one search; a new search replaces them.
- **100.** Compare keeps every food you tick when you search again, so a comparison can be gathered from several searches, and each item can now be compared at an amount you set: grams of a food, servings of a recipe.

- **99.** A food's Annotate page now offers, under the GI lookup, a ready-made prompt asking Claude AI to research that food's glycemic index, for when the lookup finds nothing suitable.
- **98.** The Home page reminder that your profile isn't set yet now says just that, and has a checkbox to stop it reminding you; the New User Manual banner no longer shows alongside a program-update banner.
- **97.** Protein complement suggestions from your pantry now show the food's current name, with its `* ` mark, and pantry and meal lines left on a food's old name are brought up to date.
- **96.** Daily Summary can now add up every nutrient for any date range, or for meals you pick by ID, and can show Recent Days in blocks of N days (a week at a time by default), each averaged per day.
- **95.** Clicking "Compare nutrition of selected" with nothing ticked in the Compare column now says so, instead of opening an empty Compare page.
- **94.** A food with no amino acid data now says, under its Macronutrients table, why there is no Digestible Complete Protein row or DIAAS.
- **93.** Deleting a Food Cache food that is still in use no longer reloads the list: the reason it can't be deleted now appears right under that food, and your filter and place stay put.
- **92.** Meal, day and summary pages now list a supplement as tablets or capsules ("2 capsules"), not as the "100 g" per tablet NuMa uses inside; the Edit box offers the count too.
- **91.** Daily Summary's Recent Days list, trends and plots now include what you add, replace or remove across many meals at once from Food Use in Meals or What-if; until now those days kept their old totals there.
- **90.** Food Use in Meals: a food's **pick dates** link lists the days it was eaten, so a replace, remove or add can reach just the dates you tick.
- **89.** Correct vitamin K from USDA now finishes: foods USDA skips when asked 20 at a time are asked for one by one, and foods USDA has no record of are no longer retried on every click.
- **88.** Food Use in Meals can now remove a food or recipe from every selected meal, or add one to every selected meal at an amount you give, alongside replacing one.
- **87.** Compare's opening line now says which amounts it's comparing; it had promised per 100 g even when a recipe was being shown whole or per serving.
- **86.** Anti-nutrient notes now go only on foods they apply to (no more notes on peaches, goat cheese, coffee or sweet corn), the dried-bean note gives the FDA's soaking and boiling times, and a recipe that cooks dried beans in a slow cooker shows a food-safety warning, on screen and in print.
- **85.** The recommended vitamin D target now follows the Endocrine Society's 2024 guideline: none above the RDA under age 75, and 23 mcg from 75 (it was 50 mcg for everyone).
- **84.** MANUAL: Appendices A–C checked claim by claim and sourced: the cocoa and chia examples now use NuMa's own reference values, and each pantry food's amino acid note matches its USDA record (almonds, cashews, pecans, walnuts, peanuts and tofu corrected).
- **83.** MANUAL: The Antinutrients and Oxalate sections now cite their sources, and say to boil dried beans for at least 30 minutes after soaking, not 10, as the FDA advises.
- **82.** MANUAL: Part 9 now records why magnesium, vitamin K2 and choline got no Revised Optimal default, and the vitamin D default carries a caveat: the guideline behind it has been replaced by one that advises against going above the RDA for most adults under 75.
- **81.** Vitamin K from USDA is now right: NuMa had been reading it from the wrong USDA figure, so most foods, leafy greens included, showed little or none. Foods → 9 corrects the foods you saved before, in one click.
- **80.** MANUAL: Weekly sweep — the protein complement section now explains "% increase", the water section says a drink with no water value gets an estimate, the public README lists water tracking, supplements and protein per meal, and the updates log is trimmed to the last two weeks.
- **79.** Any food can now be renamed from its own page, a USDA food included; the new name reaches every recipe, meal and pantry line, and a later Refresh from USDA leaves it in place.
- **78.** A day's glycemic load is now rounded once, at the end, instead of meal by meal, so several small meals no longer lose a little each.
- **77.** A meal's Top Contributors now has a second table that keeps each recipe whole, ranking the meal's items as logged: whole recipes and foods eaten on their own.
- **76.** Supplements are now their own kind of item: a food marked **This is a supplement** (automatic in supplement mode) skips every food check, weighs nothing, reads per tablet, and every nutrient table shows how much of each nutrient came from supplements.
- **75.** Foods → 9's Food data problems list now offers a fix for each problem it can: filling in missing calories, converting kilojoules or per-serving calories, dividing a milligram figure entered as grams, and more. Each fix is recorded on the food's page, with why.
- **74.** When a recalculation fails (a System Issue), a red alert now appears at the top of every page, not just Home, until you dismiss it.
- **73.** Settings sections are in a new order: Protein Digestibility Overrides is now 4, Nutrient Targets (renamed Nutrient Targets - Researched) 5, USDA API Key 6, then the glycemic index table, glycemic load, water, Meals & Log columns and Starter Data, with Keyboard Shortcuts 12 and System Issues last; the Alt+Shift keys follow the new numbers.
- **72.** The GI lookup on the Annotate page now finds sensible rows for a food's full name as it first appears in the search box, such as "Peas, split, mature seeds, cooked, boiled", instead of unrelated foods.
- **71.** The GI lookup on the Annotate page now says when the table has no row for the food you searched, only foods containing it, and offers plain rows for its ingredients (such as Peanuts for peanut butter) as labeled stand-ins; plain foods now come before branded products.
- **70.** Foods → 9 has a new **Foods: days eaten** list: every food eaten in the days you choose (30 ending today by default), counting foods inside recipes, with the foods missing a GI or a carbohydrate value ranked by days.
- **69.** The Nutrient Plot now draws daily glycemic load for a day where foods with a GI make up at least 80% of its carbohydrate, as a hollow point, and says under the plot when a chosen nutrient has no data to draw.
- **68.** On Food Cache, Add to pantry, Refresh and the starter button now bring you back to the same filtered list at the same place; Pantry's and Recipes' Archive and Delete buttons keep your filter in every case too.
- **67.** The Annotate page now has a prominent warning beside the GI box to pick the GI for the form you actually eat (raw or cooked), with a stronger one for foods named raw, dry or flour.
- **66.** The GI lookup on the Annotate page now lists a plain ingredient, such as wheat flour, ahead of the dishes made with it.
- **65.** A new day on Meals & Log now starts out scored against your current profile (its "current profile" switch ticked); untick it to keep that day's profile as it was.
- **64.** Ticking "This food is a drink" on a food with no water value (most branded drinks) now fills in an estimated water value, so its water counts toward your drinks.
- **63.** Settings → 8 turns glycemic load on or off everywhere (on by default); meal and day pages now show the day's glycemic load so far under their title.
- **62.** Meals & Log has a GL column after Calories, showing each meal's glycemic load with its band, or how much of its carbohydrate has a GI when the figure is incomplete; the list can also be sorted by GL.
- **61.** The Annotate page has a box for where each GI and DIAAS value came from, shown on the food's page; it also says what to try when the GI lookup finds nothing, and how to estimate a DIAAS.
- **60.** Meals, recipes and days now show an estimated GI under their glycemic load, with the conditions that go with it. A recipe flags raw, dry or flour ingredients whose GI may not match how they're eaten, and has a switch to stop flagging them.
- **59.** Glycemic load now counts available carbohydrate (fiber left out), as GI is defined; USDA, Canadian, Open Food Facts and your own foods used to count their fiber too, which overstated GL for high-fiber foods.
- **58.** MANUAL: The manual can now bookmark sections: **Bookmark this section** in the sidebar, a **Bookmarks** drop-down list to jump back or clear them, and ★ marks in the table of contents.
- **57.** Compare, opened from a food's Fill in nutrients from another food page, has a button for each compared food that goes straight to filling the first food in from it.
- **56.** Linoleic acid (omega-6) now has a Daily Goal, its official Adequate Intake.
- **55.** MANUAL: The essential amino acids, protein complements, omega-3 and glycemic load sections now cite their sources, and the omega-6 note now says correctly that linoleic acid has an official Adequate Intake.
- **54.** A number typed on its own as a recipe's amount (in a meal, or as a sub-recipe) now means grams, the same as for a food; servings need the word, such as "1 1/8 srv".
- **53.** Every food and recipe search box now takes a code, such as R21 or U171477, and shows just that food or recipe.
- **52.** Foods → 9's missing nutrient data list has a **has none (0)** box under each gap, for a food that truly has none of that group; its Food data problems list has a **These calories are right** button; its list of foods with no amino acid data links each one to a search for a similar food's amino acids.
- **51.** Each food in Top Contributors' list of foods with no data now has **Has none — record 0** and **Not needed for this food** buttons, and foods marked not needed leave that list, with an undo.
- **50.** The list of foods with no data under Top Contributors now has a **Find this data** button for each food, and a link to that nutrient's entry in Appendix G, which now says, for every nutrient, which sources to try and in what order; the bundled UK, Australian and French food tables now include water.
- **49.** MANUAL: The manual's table of contents now opens one level at a time — click a ▸ arrow to see the next level down, double-click it to open everything below.
- **48.** Top Contributors can show, in a second table beneath it, the foods with no data for the ranked nutrient.
- **47.** A sub-recipe's amount on Edit Recipe can now be typed as servings with fractions, a weight, or a volume, like a recipe in a meal.
- **46.** A recipe's amount on a meal page can now be typed as servings with fractions (1 1/8, 1.125), a weight, or a volume such as 3/4 c.
- **45.** A food's page shows its notes, and the prep context from its Annotate page, and they can go on its printout; a recipe's notes also show when you analyze a portion of it.
- **44.** Food use in recipes can show just the foods and recipes whose name contains the words you type.
- **43.** Renaming a food now renames it in your recipes, logged meals and pantry too.
- **42.** Compare's nutrient table now includes the omega fatty acids, iodine and selenium — everything a food's own analysis shows — and names, in a yellow box, any nutrient left out because none of the items has data for it.
- **41.** Settings' list of improved starter recipes shows each recipe's code.
- **40.** Compare can now show recipes as written, per serving or whole, instead of per 100 g.
- **39.** Compare's per-100 g figures for a recipe that uses a sub-recipe with no total weight of its own are now right; that sub-recipe used to count as weighing nothing, which made every figure far too high.
- **38.** Every food and recipe name now shows its code wherever it appears, including all of Compare's tables; a test now checks every page for it.
- **37.** MANUAL: The glossary now explains PDCAAS, the older protein-quality score that DIAAS replaced, which some food notes quote.
- **36.** The manual's search says plainly, in a yellow box, when nothing matches.
- **35.** Meals & Log explains the percentages under its figures.
- **34.** Saving your profile now re-scores today straight away; Settings can then apply it to earlier days too, and each day has a "current profile" switch, on its day pages and on Meals & Log, that flips between your current profile and the one the day was pinned to.
- **33.** A day's page notes, under its Water rows, what NICE's weight-based fluid figure comes to for you (for comparison only), and reminds you about drinks on a high-protein day.
- **32.** A clinician's fluid limit can now be set on Water from drinks as well as on Water; with either set, NuMa stops nudging you to drink more.
- **31.** Water past its goal is shown plain, not green: going past a water goal gains nothing.
- **30.** Your profile can take its water goals from the IOM (the default) or from EFSA, the European authority, whose figures are lower.
- **29.** Meals & Log's Calories column now sits after "% of goal", and it and every nutrient column after it show, under each meal's figure, that meal's share of the day's goal for the nutrient, in parentheses.
- **28.** Foods → 9's water section has a **Show these foods in the list below** button, which turns on the Water column in the missing nutrient data list and jumps to it — the way to deal with foods USDA has no water value for.
- **27.** Foods → 9's missing nutrient data list has a **Mark column not needed** button under each group's heading, and a **Refresh list** button.
- **26.** Deleting a recipe now warns you first when it's logged in any meal, as well as when another recipe uses it — from the Recipes list as well as the recipe's page — and suggests Archive instead.
- **25.** MANUAL: The water section now says what its goal is based on, that coffee, tea and dilute alcohol count as water, and why a high-protein diet needs water.
- **24.** Total water, from drinks and food together, keeps its daily goal (3.7 L men, 2.7 L women); the drinks part now has a goal of its own as well (3.0 L men, 2.2 L women). From age 65, a day's page warns when its drinks fall below the older-adult minimum (2.0 L men, 1.6 L women). Water from food shows its share of the day's water.
- **23.** A food named dry (a flour, powder, dried...) whose data says it's mostly water is flagged in recipes, meals and Foods → 9, the sign of a wet food picked for the dry one; every other food there shows its water. Search now labels USDA's okara as the wet pulp.
- **22.** Settings → 9 turns water tracking on or off; off hides it everywhere and deletes nothing.
- **21.** Searching for okara now offers USDA's okara; it used to offer an entry named "Okara" that actually held raw celery's data.
- **20.** Foods → 9 can fill in the water value for all your USDA foods at once, from USDA, without changing anything else about them.
- **19.** NuMa now tracks water from everything you log, split into water from drinks and water from food, against a daily total-water goal; foods and recipes each have a "this is a drink" checkbox, also on Food use in meals.
- **18.** A food's Protein Quality table shows each amino acid in the food and after digestion, with Met / Short following the after-digestion score; a note explains a food that is incomplete despite every amino acid being met in the food; "DIAAS" there now shows the real DIAAS, with digestibility beside it.
- **17.** A complement suggestion's "% increase" now measures from the real current DCP, named under each table, so small amounts no longer show a false decrease; capped foods' rows say "per-meal limit", not "full".
- **16.** Complement suggestions sorted by DCP achieved now follow exactly the figure each one shows, with a note explaining it; single-food pages no longer overstate that figure.
- **15.** Complement suggestions stay within a most-per-meal amount for each food (yours, saved right under the suggestion, or a default by food type), and show what that amount achieves; the limit can be lifted for one page.
- **14.** Protein complement amounts now count each food at its own digestibility, so well-digested foods like soy isolate get a realistic amount for the main gap; a suggestion sized for a different gap now says which.
- **13.** MANUAL: New section "When to eat protein" (Part 4, Z): the daily total first, spreading protein across meals, around resistance and endurance exercise, before sleep, and at breakfast — each point sourced.
- **12.** MANUAL: The FAO 2013 amino acid reference values now have their own table in Part 4, J; Part 9 is tidied, and its source-citation item is now a checklist of what's sourced and what isn't yet.
- **11.** Meal pages show whether the meal carries the per-meal protein amount research recommends for muscle (personalized from your weight and age, judged on digestible complete protein), and day pages show how many meals reached it.
- **10.** Settings has a **Help me choose a target** panel for the daily glycemic load target: three starting points — scaled to your calories, the common 80, or a step down from your own average — each explained, with sources, in the manual.
- **9.** The note beside a GI value measured in people with diabetes now follows your profile's glucose tolerance: it says whether the value fits you or is an approximation for you.
- **8.** You can set an optional daily glycemic load target in your profile; day pages, Recent Days, day averages and What-if show each day against it. Also, saving your profile in Settings now keeps the active profile's name.
- **7.** MANUAL: New sections "What you can do with GI and GL", with a worked example, and "What 'impaired glucose tolerance' means here" — what that label covers and how to use such a value if you don't have diabetes; every place NuMa marks such a value now links to it.
- **6.** Compare shows each item's GI and glycemic load per 100 g; Recent Days has a Day GL column; every glycemic load band now has a one-line note on how to read it.
- **5.** A GI value measured in people with impaired glucose tolerance or diabetes is now marked wherever it's used — the food and Annotate pages, glycemic load figures, Top Contributors and swap suggestions.
- **4.** Foods → 9 has a new list, foods you use with carbohydrate but no GI, and lower-GI swap suggestions now say they come only from foods with a GI, with a link to that list.
- **3.** Top Contributors can rank a meal's or recipe's foods by glycemic load, and when that load is Medium or High, NuMa suggests lower-GI foods from your Food Cache to swap in, each opening What-if with the swap filled in.
- **2.** What-if pages now show glycemic load before and after your changes, and say when a swap to a food with no GI makes the "after" look better than it is; every incomplete GL figure now says how much of the carbohydrate it covers.
- **1.** A meal's or recipe's Missing Amino Acid Profiles section now has a button beside each food to mark its amino acids "not needed" (for a supplement, say), which stops it being listed; it and the Calories note both link to how to turn their check off.

#### October 22 updates

**PROGRAM: BUTTONS ARE OUTLINED IN BLUE, AND TURN BLUE WHEN READY**

Buttons now stand out with a blue outline. A button that acts on what you type or pick beside it turns solid blue with white lettering once there's something there to act on, the way **Create Meal** has always looked: on Meals & Log, **Show** (with a number in *Number shown*) and **Calculate** (with a range picked) now start out blue. Save buttons still light up their own way, with "Unsaved changes" beside them, and Search buttons as before.

<!--

```
Scope: every page; web/static/style.css (.btn-outline-secondary border vars,
.btn-input-ready), web/templates/base.html (new input-ready script after the
search-button script). The script finds every submit button styled
btn-outline-secondary / btn-outline-primary / btn-secondary and toggles
.btn-input-ready while any text/number/date/select/textarea box in its form
(form.elements, so form="" boxes count too) is non-blank. Skipped: Search /
Filter labels and data-search-button (the search-button script's), Save...
labels (dirty-tracking's job; their boxes are always filled), forms with no
such boxes (hidden-only Remove/Delete rows, checkbox-only forms).
Tests: tests/test_input_ready_button_js.py.
```

-->

**PROGRAM: MEALS THAT DON'T CONTAIN A FOOD**

Search meal history now has its own line on Meals & Log, with a choice beside it: **Meals that contain** a food or recipe, as before, or **Meals that don't contain** it, which lists every logged meal it isn't in. Type part of its name, a code such as U171477 or R21, or a cached food's FDC ID number on its own. [learn more...](#meal-history)

<!--

```
Scope: Meals & Log, Search meal history; web/templates/meals.html,
meals_search.html, web/backend.py meals_search() (new mode=contains|lacks
query param; a bare all-digits query is read as an FDC ID). "Doesn't
contain" = every meal from db.meal_list_recent(limit=-1) whose id isn't
among the matching items' meal ids; recipe ingredients still aren't
searched, so a meal holding a recipe made with the food is listed as
lacking it (said on the page). Test: test_meal_history_search_lacks.
```

-->

**MANUAL: WEEKLY SWEEP**

The Glossary now explains [EFSA](#gloss-efsa), the European source NuMa can take your water goals from. Searching the manual for words such as *hydration*, *fish oil*, *versus*, *acronyms* or *multivitamin* now finds the sections about them, and the [Annotate](#annotate) section describes how the page opens and its **DIAAS needed, click to go there** button. The updates log now keeps the last two weeks.

<!--

```
Scope: user-manual.md, README.md, README-numa-documentation.md, tests/test_web.py,
tests/test_usda.py. Weekly sweep 2026-10-22, items 1-10. Items 1-3 clean (CLAUDE.md
layout, NuMa capitalization, Bootstrap 5.3.8 still latest). Item 4: log pruned to
Oct 8 onward (Sep 30 - Oct 7 entries and the v2026-10-07-2026 / v2026-10-05-0748
summaries removed). Item 5: Annotate opening/DIAAS-jump sentence added. Item 6:
README.md Food use (remove/add, picked dates), date-range summaries, two British
spellings. Item 7: new test_compare_clear_button_starts_an_empty_list. Item 8:
internal links pass; 19 new external URLs, the 7 that returned 403 to curl are
registered DOIs (doi.org handle API). Item 9: gloss-efsa added. Item 10: 3 older
terms lines reread (still fit); terms lines added to Comparison Tables, Glossary,
TOC help, and Appendix G Water / Omega / Minerals / Vitamins. Mutation churn check:
usda_nutrients.py and profile.py flagged and run; 2 new TestAntinutrientMatching
tests (suppress-check continue->break, _word_re builder), 263 -> 252 survivors;
profile.py unchanged at 224.
```

-->

#### October 21 updates

**PROGRAM: MERGING DUPLICATE FOODS KEEPS YOUR EDITS; NO MORE DOUBLE PANTRY ENTRIES**

On Foods → 9 → **Find duplicate foods**, each copy now shows which values you've edited on it. When you keep one copy and the others have values it lacks or has differently, you choose value by value which to keep before anything is deleted, with your own edits preselected; values copied over count as your edits, so a Refresh from USDA won't quietly undo them. Adding a food that's already in your pantry now reuses its entry, existing doubles are merged when NuMa starts, and the same page lists any that remain with a **Merge into one** button. [learn more...](#duplicate-foods)

<!--
```
Scope: Foods -> 9 -> Duplicate Foods (/food/cache/duplicates, new /review step,
new /pantry POST); data_quality.py (_edited_labels, merge_review), db.py
(pantry_add reuses an existing entry for the same food; pantry_duplicate_groups,
pantry_merge_duplicates; merge_food_into now folds pantry rows), backend
startup + pantry link path; templates food_duplicates.html,
food_duplicates_review.html.
Root cause of the double pantry entry (U170148 hemp seed): pantry_add never
checked for an existing row, and merge_food_into re-pointed both foods'
pantry rows at the kept food. Merge review: one option per distinct value,
"mine" from db.food_edited_keys; default = fill blanks, else the user's edit
on a dropped copy unless the kept value is also theirs. Chosen values go in
via merge_user_supplied_nutrients (mark_edited) with a note naming the
source copy; estimated flags carry over. Pantry merge keeps the oldest
non-starter row (clearing starter data deletes starter rows by id).
```
-->

**MANUAL: SEARCH FINDS SECTIONS BY EVERYDAY WORDS**

The manual's search now finds about 200 more sections by the everyday words people search with, even where a section doesn't use them itself: *food diary* finds Meals & Log, *salt* finds sodium, *fish oil* finds omega-3s, *hotkeys* finds the keyboard shortcuts. [learn more...](#search-terms)

<!--
```
user-manual.md: 205 new hidden "*Search terms: ...*" lines (Part 1: 18; Parts
2-10: 187), each with only terms its section doesn't already contain (checked
by script). tests/test_manual_abbreviations.py now skips Search terms lines,
which readers never see.
```
-->

**MANUAL: AMERICAN SPELLING THROUGHOUT**

The manual now uses American spelling everywhere: labeled, liters, color, gray, fiber, license, program, and so on. The titles of published sources quoted in the notes keep their original spelling. NuMa's own screens and messages now use American spelling too.

<!--
```
82 lines changed, Part 11 included. Kept as published: footnote titles,
journal names and URLs (ASA "Glycaemic index", Mechanisms of Ageing and
Development, "Dietary fibres, fibre analogues", "glycaemic index tables",
"non-hospitalised"). The program's own screens and messages were converted
the same day (templates, backend/claude_fetch/csv_import messages); the unit
parser still accepts "litre"/"millilitre" as typed input.
```
-->

**MANUAL: SEARCH TERMS LINES HIDDEN, STILL SEARCHED**

The italic *Search terms: ...* lines at the top of some sections no longer show. The manual's search still finds those sections by the words they list, and when one matched only that way, the count under the search box says **this section is listed under that search**. [learn more...](#search-terms)

<!--
```
scripts/build_manual.py: hide_search_terms() turns each "*Search terms: ...*"
line into <span class="search-terms" hidden> (still in textContent, which the
section index reads); highlighter skips .search-terms; count_words() drops
the lines; check_search_terms() fails the build on a malformed one (it caught
the protein-per-meal line, which had prose on the same line, now split).
Rule written into CLAUDE.md ("Search terms lines"); README: mechanism,
weekly sweep item 10 (Search terms coverage), and a whole-manual pass in the
monthly full manual audit. Tests: tests/test_manual_search_terms.py.
```
-->

**PROGRAM: TODAY'S SUMMARY SAYS WHEN NOTHING IS LOGGED YET**

On Daily Summary, clicking **Today's summary** before any meal is logged for today now shows a message beside the button saying there is nothing to summarize yet, with a link to Meals & Log.

<!--
```
Analysis -> Daily Summary. The button linked to /summary/<today>, which
redirected straight back to /summary when the date had no meals, so the click
looked dead. summary_index now passes today_has_meals; without meals the
button is a type=button that unhides #today-empty-note. A /summary/<date> URL
with no meals now renders an empty Full Day page ("No meals are logged for
...") rather than redirecting.
```
-->

**PROGRAM: ONE FULL DAY PAGE, WITH THE WHOLE ANALYSIS**

A day's analysis is now the same page whether you reach it from a meal or from Daily Summary; only the breadcrumb differs, so it still leads back the way you came. It now has every analysis section a meal page has, pooled over the day, including Top Contributors (by food and by meal item, with lower-GL swaps), Missing Amino Acid Profiles and Anti-nutrients. A **Show another date** box on it opens any other day. [learn more...](#full-day)

<!--
```
/meal/<id>/day and /summary/<date> both render meal_day.html from one
builder, backend._day_context(meal_date, from_meal_id) (replaces
_meal_day_context and summary_date's own copy); day_url in the context is the
URL in use, for the profile form/switch, Top Contributors form and print link.
summary.html lost its date-detail half (now just the landing page). New:
/summary/<date>/print (shared _day_print_response); day print gains the
Anti-nutrients section. Contributors run over _day_analysis()'s leaf
ingredients; GL swap What-if links scope to all the day's meal IDs (comma
list). Anti-nutrients and oxalate over the same leaves. Day page now also
shows the calorie, recalculation and diet-aware notes the old dated summary
had, and keeps its data-remember panel memory. Fixed: the profile switch's
"next" URL on meal_day.html was a literal "{{ from_meal_id }}" string (Jinja
expression nested in a string literal), so switching came back to a bad URL.
Tests: test_day_page_same_from_summary_and_meal,
test_summary_today_button_explains_empty_day.
```
-->

#### October 20 updates

**MANUAL: SECTIONS ON OLDER PEOPLE FOUND BY SEARCH**

A manual search for *older people*, *seniors*, *elderly*, *over 65* or *over-65* now finds every section about older people's needs: protein per meal, breakfast protein, water, the age bands behind the vitamin and mineral targets, and the opening sections on why protein matters. [learn more...](#water-older)

**PROGRAM: ALT+SHIFT+DIGIT SHORTCUTS IN SETTINGS NOW WORK**

**Alt+Shift+1** through **Alt+Shift+0** now open their Settings section, rather than switching browser tabs. [learn more...](#web-shortcuts)

<!--

```
Scope: web/templates/base.html, Alt+Shift keydown handler. With Shift held, e.key
for a digit is the shifted character ("!" for 1 on a US layout), so no data-ak
digit ever matched, the event was not preventDefault()ed, and Firefox ran its own
Alt+1 select-first-tab. Digits now come from e.code (Digit1/Numpad1); letters keep
e.key so they follow the keyboard layout, falling back to e.code KeyX only when
e.key is not a plain letter (macOS Option+Shift special characters).
```

-->

**PROGRAM: ALT+SHIFT+I JUMPS TO THE SEARCH BOX**

On any page with a search box — a meal, a recipe, Foods: Search, Analyze a food portion, Pantry, Food Cache, Annotate, Compare, Recipes, Meals search and the rest — **Alt+Shift+I** now puts the cursor in it with its text selected, ready for a new search, opening its section first if it's closed. [learn more...](#web-shortcuts)

<!--

```
Scope: web/templates/base.html (Alt+Shift handler: an <input> target opens every
enclosing <details>, then focus()+select() instead of click()); data-ak="i" on the
main search input of meal, recipe_edit, search, food_analyze_portion, compare,
pantry (the add search, not the list filter), food_cache, recipes, food_annotate,
meals_search, food_convert, food_fill_from, oxalate_link; Settings 12 lists it.
```

-->

**PROGRAM: SAVE BUTTONS LIGHT UP WHEREVER YOU TYPE**

A Save button now lights up, with "Unsaved changes" beside it, as soon as you type in its box, in four places that had been missing it: a complement suggestion's **Most I'd add to a meal** limit, Settings' nutrient-target rows, a food's portion rows in Food Cache, and the Annotate page, where the "give me a prompt" link used to light up instead of **Save annotation**.

<!--

```
Scope: web/templates/base.html (unsaved-changes script), _complement_limit.html,
settings.html, food_cache_portions.html. The tracker only looked at fields inside
the <form> element and took its first submit button. Now: the submit button must
belong to the form (button.form === form), so one naming another form via form=""
is skipped; data-dirty-outside opts a form into tracking boxes tied to it by form=""
(opt-in, so Compare/Fetch tick-box selection forms stay untracked); data-dirty-group
tracks a few boxes with their own formaction Save button inside a larger GET form.
```

-->

**PROGRAM: "ADDED" LINE SHOWS THE AMOUNT**

After you add a food or recipe from the search results on a meal or recipe page, the confirmation now says how much you added, e.g. **Added Hummus — 1.8 servings (180 g).**, with the note about the search results on the next line.

<!--

```
Scope: web/backend.py meal_add_food, meal_add_recipe_item, recipe_ingredient_add,
recipe_ingredient_add_recipe pass added_amount; _added_amount() gives the typed amount
plus grams when not typed in grams; recipes show servings plus grams when the serving
weight is known. meal.html / recipe_edit.html render it.
```

-->

#### October 18 updates

**PROGRAM: ANNOTATE PAGE OPENS AT THE TOP, WITH A JUMP TO DIAAS**

Clicking **Add or edit GI / DIAAS estimates** on a food's page now opens the Annotate page at its top, so you read it from the start; when the food has no GI yet, the cursor is already in the GI estimate box. When a GI is on file and only DIAAS is still wanted, an orange **DIAAS needed, click to go there** button at the top takes you down to the DIAAS box with the cursor in it. [learn more...](#annotate)

<!--

```
Scope: Foods -> a food's page -> Add or edit GI / DIAAS estimates (also Annotate a Food); web/templates/food_annotate.html, web/templates/base.html, tests/test_web.py.
Cause: the Skip for now / Back without saving / Back to list link carried [autofocus], so the browser scrolled down to it on load, leaving the DIAAS field at the top of the window and focus on a link whose ring was easy to miss. base.html's remembered-scroll restore (keyed on path + query) then brought that offset back on later visits. Fix: autofocus removed; a [data-no-scroll-restore] marker on the edit view makes base.html skip the restore; a page script focuses (preventScroll) the GI box if empty, else the new #diaas-jump button, else the back button, then scrollTo(0,0). #diaas-jump (shown when gi_estimate is on file and DIAAS is in missing) replaces the orange "Asking for this one" badge on the DIAAS label; its click scrolls #diaas-label to the top and focuses #diaas_estimate. Verified in Chromium and Firefox via Playwright.
```

-->

**PROGRAM: GI FOR FOODS WITH LITTLE CARBOHYDRATE AND NO GI ANYWHERE**

For a food like hemp seed, which has no measured GI and very little carbohydrate, the manual now explains why no value exists and how to save a clearly labeled estimate, so meals using it get a complete glycemic load. The Annotate page's advice when the GI lookup finds nothing now says the same. [learn more...](#gi-low-carb)

<!--
```
Scope: user-manual.md new section #gi-low-carb (after #choosing-gi-values,
which now links to it); web/templates/food_annotate.html gi-no-match-help
"Still nothing?" item. The old advice (tick "Don't prompt me" for a
low-carb food) left the food a not_wanted gap, so GL stayed incomplete;
only foods under NEGLIGIBLE_CARBS_G (1 g in the amount eaten) count as zero,
and a typical serving of a seed or nut is just over it.
```
-->

**PROGRAM: SEARCH FOCUS STAYS WHERE YOU ARE TYPING**

Clicking **Add Food or Recipe** (meal page) or **Add Ingredient** (recipe edit) puts the cursor straight in the search box. After a search, the cursor lands in the first result's amount box, recipe or food, and when the online results arrive moments later neither the cursor nor the page moves.

<!--

```
Scope: web/templates/base.html (details-toggle autofocus; shared [data-search-results] swap), web/templates/meal.html (add-food search script), web/templates/recipe_edit.html.
The toggle autofocus required the clicked <summary> to be document.activeElement, which Firefox/Safari don't do on a mouse click, so it silently did nothing there; a capture-phase click tracker now counts a just-clicked summary too. meal.html's first-result selector looked for portion_str/servings, but recipe rows use "amount", so a recipe listed first was skipped. After the online merge meal.html called focusFirstResultField() again, which stole focus back and scrolled; now both it and the shared swap record the focused row field (row key + name + radio value), caret and scroll position before replacing the tbody and restore them afterwards with preventScroll. Two more culprits, found in a real browser (Chromium + Firefox via Playwright): an older add-food-details toggle script near the bottom of meal.html focused the first food portion box on open (and on load), overriding both the search-box and first-result rules -- removed; and the first-result focus used setTimeout(0), which on this long page fired before base.html's later autofocus-to-Search-button script ran (the parser yields), so the button won -- it now waits for DOMContentLoaded (meal.html and recipe_edit.html).
```

-->

**PROGRAM: COMPARE: A FOOD'S AMOUNT AS A NUMBER OF ITS PORTIONS**

On Compare, a food with portions now has a g / portion choice beside its Amount box, so you can compare, say, 2 slices of bread against 1 cup of rice instead of working out the grams. [learn more...](#comparison-amounts)

<!--
```
Scope: Compare (web/backend.py _parse_compare_amounts, _compare_amount_token,
compare_set_amounts, _load_compare_entry; web/templates/compare.html).
A food's item token takes "@<count>p<n>" (f748967@2p1 = 2 x portion 1); the
unit_food_<id> select posts "g" or "p<n>". Grams = count x the portion's
gram_weight from the cached portions_json (or the fetched detail for an
uncached food). A portion index that no longer exists falls back to 100 g
with a note under the Amount box. Saved lists keep the unit as-is.
```
-->

**PROGRAM: COMPARE: CLEAR THE LIST AND START OVER**

Compare now has a **Clear the list and start over** button beside the Search button, in place of the Clear comparison button that sat further down the page. [learn more...](#comparison)

**PROGRAM: SEARCH MEAL HISTORY BY CODE**

Search meal history now takes a food or recipe code as well as a name: **U171477** or **R54** lists every meal that one food or recipe was logged in, and nothing that just shares a word with it. [learn more...](#search-by-code)

<!--
```
Scope: Meals & Log -> Search meal history; db.py
(search_meal_history_by_item), web/backend.py (meals_search),
meals_search.html. A code is matched on meal_items.fdc_id (item_type food)
or recipe_id (item_type recipe), not on the stored name copy.
```
-->

**PROGRAM: FILTER ANY LIST BY CODE**

The Recipes list, Food Cache, Annotate, My Pantry and the Food Use pages now find an item by its code as well as its name: type **R54** in the Recipes filter, or **U171477** in Food Cache's, and just that recipe or food is listed, even if it's archived. [learn more...](#search-by-code)

<!--
```
Scope: Recipes list, Food Cache, Annotate, My Pantry filter, Food Use in
Recipes name filter, Food Use in Meals replacement type-ahead; db.py
(search_cached_foods), web/backend.py (_typed_code), five templates.
db.search_cached_foods() now returns just the one food when the whole query
is a food code (food_ids.parse_code) or a cached bare FDC ID — so every
caller (Food Cache, Annotate, copy-from search, replacement type-ahead)
gets it. Recipe codes are matched in recipes_list (searching all recipes,
archived included, not just the 200 most recent) and the type-ahead.
```
-->

**PROGRAM: COMPARE SHOWS EACH RECIPE'S SERVING DESCRIPTION**

On Compare, a recipe's serving description, such as "1 muffin", now appears beside its serving weight in the list of items, and under its name in the nutrient table whenever servings are being compared. [learn more...](#comparison-amounts)

**PROGRAM: COMPARE USES A RECIPE'S OWN TOTAL WEIGHT FOR PER 100 G**

On Compare, a recipe's per-100 g figures are now per 100 g of the finished dish, using the total weight you entered for the recipe, so cooking loss is allowed for, and 100 g matches what a meal logs as 100 g. A recipe with no total weight still adds up its ingredients, as before. [learn more...](#comparison-estimate)

<!--
```
Scope: Compare; web/backend.py (_load_compare_entry), compare.html text.
Batch weight = recipe_serving_grams() × servings when that is known (stated
total weight, else a complete ingredient sum), else the possibly incomplete
db.recipe_compute_weight() sum, still marked "(estimate)". Before, the
100 g basis always used recipe_compute_weight() while a meal (and Compare's
grams amounts) used recipe_serving_grams(), so R50 showed 187.4 kcal/100 g
on the 100 g basis and 184.9 at "100 g" set as an amount.
```
-->

**PROGRAM: COMPARE A RECIPE BY GRAMS**

On Compare, a recipe with a weight per serving now has a servings-or-grams choice beside its Amount box, so you can compare, say, 100 g of your hummus with 30 g of peanut butter. [learn more...](#comparison-amounts)

<!--
```
Scope: Compare; web/backend.py, web/templates/compare.html.
Amounts are now (value, unit) — CompareAmount; a recipe token "r12@150g" is
grams, "r12@2" servings; foods are always grams. Grams convert to servings
by recipe_serving_grams() (stated total weight, else complete ingredient
sum), the same figure a meal uses. Grams with no serving weight fall back to
1 serving with a red note. Saved lists store "unit". Also removed the lone
"Compare" breadcrumb above the page heading.
```
-->

**PROGRAM: COMPARE CONTENTS LIST, CLEARER SHOW COMPARISON BUTTONS**

Compare now has a Contents list down the side, for jumping between its tables. Its two buttons now read **Show comparison for 100 g of each item** and **Show comparison at the amounts set above**, and the blue one follows what you've asked for: the amounts one as soon as you type an amount. The Compare amounts choice is now there for foods-only comparisons too. [learn more...](#comparison-amounts)

<!--
```
Scope: Compare; web/templates/compare.html, tests/test_gl_swaps.py.
analysis-page layout + sidebar_nav (only when items exist); section ids
cmp-ingredients / cmp-protein / cmp-gl / cmp-nutrients / cmp-save /
compare-items. The 100 g button is now a link that sets basis=100g (it used
to be a bare #comparison anchor that showed whatever basis was remembered).
Primary class: server-side from basis/amounts, swapped live by a small
script on the Amount inputs. Basis selector no longer gated on any_recipe.
The GL test now slices by section id, since the sidebar repeats the titles.
```
-->

**PROGRAM: ADD SEVERAL FOODS FROM ONE SEARCH**

On a meal's Add Food or Recipe search, a recipe's Add Ingredient search and My Pantry's search, adding a result now leaves the results showing, with a line naming what you just added, so you can pick another from the same list. Running a new search replaces them as before. [learn more...](#search-keeps-results)

<!--
```
Scope: Meal page, Edit Recipe, My Pantry; web/backend.py (meal_add_food,
meal_add_recipe_item, meal_update_item_post, serving-weight, recipe
ingredient add / add-recipe, pantry_add), _add_food_row.html,
_pantry_search_rows.html, meal.html, recipe_edit.html.
A successful add used to redirect with an explicit empty q=, which made the
persist-search JS in base.html forget the search. Now each add posts the
current q (meal add-recipe form gained it; pantry rows post search=) and the
redirect carries it back plus added=<name>, shown as #just-added. Pantry's
"link" mode still returns to the plain list. Edit Recipe's scroll restore
no longer jumps to the Ingredients section after an add from the results.
```
-->

**PROGRAM: COMPARE FOODS FROM SEVERAL SEARCHES, AT AMOUNTS YOU SET**

On Compare, tick a food, then just search for the next one: what you ticked is added first, so a comparison of quite different foods can be built up search by search. Each item in the list now has an Amount box (grams for a food, servings for a recipe); **Compare at the amounts set above** shows every table at those amounts. [learn more...](#comparison-amounts)

<!--
```
Scope: Compare (/compare); web/backend.py, web/templates/compare.html.
Ticks were lost because a new search was a plain GET that never posted the
results form. Now the search form, when results are ticked, submits the
results form to /compare/add-multiple with then_search = the search's query
string (search/source/limit only); add-multiple appends it to its redirect.
Amounts ride in the items string as "@n" suffixes (f174@150, r12@2), parsed
by _parse_compare_amounts() and re-emitted by _compare_items_str(); every
add/remove/save/load keeps them (saved lists store an "amount" key). New
basis "amounts" (_COMPARE_BASES): food grams / recipe servings scale
nutrients, DIAAS, GL and ingredient rows. New POST /compare/amounts.
```
-->

#### October 17 updates

**PROGRAM: ASK CLAUDE AI FOR A FOOD'S GI FROM ITS ANNOTATE PAGE**

When the GI lookup on a food's Annotate page has nothing suitable, the line under it, **give me a prompt asking Claude AI**, opens a ready-made prompt in a new tab asking Claude AI to research that food's glycemic index and say where the value comes from. Copy it into claude.ai, then type the number Claude gives into the GI box, or import the reply to save it for you. [learn more...](#fetch)

<!--
```
Foods -> Annotate a food (/food/annotate/<id>); web/templates/food_annotate.html,
claude_fetch.html, web/backend.py food_cache_claude_fetch(), claude_fetch.py.
New gi_only form field on POST /food/cache/claude-fetch: asks for "gi" alone (no
nutrient keys, no DIAAS), even when a GI is already saved, since the user asked
outright; the import still only fills a blank GI unless overwrite is ticked.
Annotate page submits it via an external form (forms can't nest), target=_blank.
Targeted-prompt line for a food with no keys wanted now reads "none are wanted for
this food" instead of claiming every nutrient value is present.
```
-->

**PROGRAM: HOME PAGE PROFILE REMINDER CAN BE TURNED OFF**

Until your profile is saved, the Home page says so: NuMa needs it to work out your daily targets. Tick **Don't remind me about this again** to stop the reminder. When a program update is available, the separate New User Manual banner is no longer shown too, since the update brings its own manual. [learn more...](#home-page-tour)

<!--
```
Scope: Home page (web/templates/home.html, web/backend.py). The "NEW TO NUMA?" banner is renamed
"YOUR PROFILE ISN'T SET YET" and reworded to the one thing it checks (no saved profile); new
POST /profile-notice/ack-banner sets prefs.json profile_notice_dismissed. Manual-update banner
condition is now manual_update_available and not update_available. Same session: the manual's
Preface excerpt was removed from the Home page, and
NEW_VERSION_NOTE is no longer printed there (it goes into this log as the Version overview).
```
-->

#### October 16 updates

**PROGRAM: PANTRY AND MEAL LINES FOLLOW A FOOD'S NAME**

A protein complement suggestion from your pantry now names the food exactly as its own page does, `* ` mark included. Pantry and meal lines that still showed a name the food no longer had are brought up to date the next time NuMa starts, and a food's new name from Refresh from USDA or an import now reaches them too, as a rename already did. Recipe ingredient lines are left as they are, since you may have chosen their names yourself.

<!--

```
Scope: db.py (cache_food() now calls propagate_food_name() when the name changes;
new sync_food_name_copies(), run at startup in web/backend.py _lifespan with
cascade_food_change() per food touched; propagate_food_name() gains a tables=
filter), web/backend.py (_web_pantry_candidates() names a candidate by
foods.name; POST /food/{id}/rename cascades when copies changed); tests in
tests/test_db.py and tests/test_web.py.
Root cause: cache_food()'s upsert changed foods.name without propagating, so
re-caches (Refresh, imports, starter updates) left pantry/meal/recipe copies on
the old name; complement candidates read the pantry copy, which keeps its own
"* " marker (per-table by design), so a starter food showed without it. The
repair skips recipe_ingredients because a line name there can be hand-edited.
Digestibility is looked up by line name, hence the cascade after each repair
and after a rename.
```

-->

**PROGRAM: NUTRIENT TOTALS FOR A DATE RANGE OR CHOSEN MEALS, AND BLOCKS OF DAYS**

Daily Summary has two new buttons. **Nutrient totals for a date range or meals** adds up every nutrient across any dates you choose, or across meals you list by ID (ranges like 20-24 work), with the per-day average beside the total. **Blocks of days** shows Recent Days a block at a time — 7 days per row by default, any size you like — so you can compare one week with the next. [learn more...](#range-totals)

<!--

```
Scope: Analysis -> Daily Summary; web/backend.py (summary_trend body moved into
_multi_day_context(), shared with new /summary/range; new /summary/blocks;
_nutrient_sections rows now carry "key"), web/templates/trend.html (range mode:
Total column, date-range and meal-ID forms), new web/templates/summary_blocks.html,
summary.html buttons; tests in tests/test_web.py.
Range totals expand meals live (_meal_expand_for_diaas), like the trend view. In
meal-ID mode a date's GL is the combined GL of the chosen meals on it, not
day_gl_total() of the whole day. Blocks read meal nutrient snapshots
(day_nutrient_raw_totals) like Recent Days, so many blocks stay fast; % of goal
is against the profile pinned to each block's last logged day.
```

-->

**PROGRAM: COMPARE BUTTON WITH NOTHING TICKED NOW SAYS SO**

If you click "Compare nutrition of selected" before ticking anything in the Compare column, NuMa now tells you to tick boxes there first, instead of opening an empty Compare page. On Food Cache this is easy to hit: the first column there is Fetch (for Claude AI), and Compare is the second. [learn more...](#comparison)

<!--
```
Scope: Food Cache, Foods search, My Pantry, Recipes, Compare (every form posting to
/compare/add-multiple). web/templates/base.html: one document-level submit listener
stops an add-multiple submit with no fdc_id/recipe_id and alerts. web/backend.py
compare_add_multiple(): if nothing was posted at all, the redirect carries an error
message as a fallback (JS off, etc.). Reported as "compare gives a bare page";
reproduced with Playwright against a copy of the live DB: the Compare-column flow
worked, so the empty items= came from ticks in the Fetch column.
```
-->

#### October 15 updates

**PROGRAM: FOOD PAGE EXPLAINS A MISSING DCP ROW**

A food that has protein but no amino acid data now has a note under its Macronutrients table: it has no Digestible Complete Protein (DCP) row and no DIAAS because both are worked out from the amino acid profile. Fill in that data to see them. [learn more...](#fetch)

**PROGRAM: FOOD CACHE KEEPS YOUR PLACE WHEN A DELETE IS REFUSED**

When you try to delete a [Food Cache](#food-cache-web) food that a pantry entry, recipe or meal still uses, the explanation of where it's used, and how to clear it, now opens right under that food. The list stays as it was: same filter, same place on the page.

<!--

```
Scope: Foods -> Food Cache; web/backend.py (food_cache_delete), web/templates/base.html
(js-row-remove handler), new web/templates/_food_delete_blocked.html (moved out of
food_cache.html, which now includes it), tests/test_web.py.
The fetch-based delete replied {"ok": false} for a referenced food, and base.html then fell
back to a real form submit -- a full reload to the top of the page. Now the AJAX reply
carries blocked_html (the same explanation partial, rendered server-side) and base.html
inserts it as a full-width row under the food's row (replacing any earlier one there);
anything without blocked_html still falls back to a real submit as before.
```

-->

**PROGRAM: SUPPLEMENTS LISTED AS TABLETS, NOT GRAMS, IN MEALS**

Meal, day and summary pages now list a supplement by the tablet or capsule — **1 capsule**, **2 capsules**, **0.5 tablet** — instead of as 100 g per tablet, and its Edit box offers the same count. Nothing about your totals changes. [learn more...](#supplements)

<!--
```
Scope: meal page, meal day page, Daily Summary day page, meal search, print.
backend._supplement_count() turns a supplement's internal grams (one unit =
100 g, supplements.py) into "N <unit>s"; _annotate_food_amounts() sets
supp_count and amount_display (the count when it reparses against the food's
"1 tablet" portion, else grams); _food_amount.html shows supp_count in place
of grams. Old meal lines whose saved label is "100 g" read correctly too —
only display changed, stored amounts untouched. Test:
test_supplements.py test_meal_pages_show_a_supplement_as_tablets_not_grams.
```
-->

**PROGRAM: BULK MEAL CHANGES NOW REACH DAY TOTALS**

After you add, replace or remove a food or recipe across many meals at once (Food Use in Meals, or What-if's Apply for real), the Recent Days list on Daily Summary, the nutrient trends and the Nutrient Plot now show the new totals. Until now they kept each day's old totals, while the day's own page showed the new ones.

<!--
```
Scope: Analysis -> Food Use in Meals (replace / remove / add), What-if: meals
Apply for real. db.substitute_item_in_meals() and db.remove_item_from_meals()
now flag every meal they change in stale_meals (via meals_with_direct_item);
the Food Use bulk add flags each meal it adds to. The stale-meals middleware
then recomputes each meal's stored DCP / calories / nutrients_snapshot_json
on the next page load. Found 2026-10-15: "Water, overnight - 2 c" added to 12
meals in bulk; Recent Days showed 821 g water for 2026-10-02 against 1294 g
on the day page. Test: test_food_use_changes_refresh_stored_meal_totals.
```
-->

**PROGRAM: REPLACE, REMOVE OR ADD ON CHOSEN DATES ONLY**

On Food Use in Meals, click **pick dates** beside a food's day count to list the dates it was eaten, and tick the ones you want: a replace, remove or add then reaches only the meals on those dates. [learn more...](#fooduse-pick-dates)

<!--
```
Scope: Analysis -> Food Use in Meals; web/backend.py (analysis_food_use rows
carry "dates": [{date, weekday, meal_ids}]; analysis_food_use_substitute takes
only_meals and intersects it with the on-screen selection, never widening it;
empty intersection is an error), web/templates/analysis_food_use.html (per-row
hidden date sub-row with checkboxes, hidden only_meals field, limit summary,
confirm text), tests/test_web.py test_food_use_change_limited_to_picked_dates.
```
-->

#### October 14 updates

**PROGRAM: VITAMIN K CORRECTION FINISHES**

**Correct vitamin K for N USDA foods from USDA** on Foods → 9 now clears its whole list. Foods USDA skips when asked for 20 at a time are asked for one by one, and a food USDA has no record of is named in the result and left alone, instead of staying on the list for good. [learn more...](#vitamin-k-fix)

<!--
```
Scope: Foods -> 9 (numa_app/services/vitamin_k_repair.py, food_cache_db_check.html).
USDA's bulk /foods?format=abridged&nutrients=430 silently omits some Branded records
(1626275, 1628000, 2025844, ...) that /food/{id} serves, so they never got checked and the
button kept offering the same 10 foods with nothing changing. Missing ids now fall back to
get_food_detail per food; a 404 there (ids that aren't USDA records: 111, 26126, 640661,
44000047764) marks the food checked with its value untouched (status not_in_usda); other
errors leave it for a retry. run() now resets its own counts (start() did; tests calling
run() directly saw the previous run's not_found).
```
-->

**PROGRAM: REMOVE OR ADD A FOOD ACROSS MANY MEALS**

Food Use in Meals can now take a food or recipe out of every meal you've selected, or add one to every selected meal at the amount you give, as well as replacing one with another. [learn more...](#fooduse-remove-add)

<!--
```
Scope: Analysis -> Food use in meals (web/templates/analysis_food_use.html, _replace_picker.html;
web/backend.py analysis_food_use_substitute + new _food_use_back; db.remove_item_from_meals).
The substitute POST takes action=replace|remove|add (default replace, so old forms still work).
Remove deletes direct meal_items only, like substitute. Add parses `amount` exactly as the meal
page does (_parse_portion_str for a food, parse_recipe_amount for a recipe, bare number = grams)
and inserts one line per selected meal; refused with no meals selected. Panel gets an action
radio group; the shared picker's read-back line follows the action (recipes page unchanged).
Tests: test_food_use_remove_from_selected_meals, test_food_use_add_to_every_selected_meal.
```
-->

**PROGRAM: COMPARE SAYS WHICH AMOUNTS IT'S COMPARING**

Compare's opening line now names the amounts in use. When **Compare amounts** is set to one serving or the whole recipe, it says so, and points you to the choice that puts everything back on per 100 g. [learn more...](#comparison-basis)

<!--
```
Scope: Analysis -> Compare (web/templates/compare.html intro; web/backend.py _load_compare_entry).
The intro always read "compare them per 100 g", but the basis choice is remembered in
prefs.json (compare_basis), so a page opened later with "recipe" in force showed whole-recipe
amounts under a per-100 g promise. Intro is now basis-aware. Also: a typed measure that is
itself grams ("1580 g") was shown again beside the grams ("1580 g (1580 g)"); the check only
caught a bare "g". Tests: TestCompareBasis in tests/test_recipe_serving_weight.py.
```
-->

**PROGRAM: ANTI-NUTRIENT NOTES CORRECTED; SLOW-COOKER BEAN WARNING**

Anti-nutrient notes now appear only on foods they really apply to: peaches, goat cheese, coconut milk, nutmeg, coffee, jelly beans, cornstarch and sweet corn no longer get one, and hummus and hemp protein now do. The note on dried beans gives the FDA's advice: soak at least 5 hours, then boil for at least 30 minutes. A recipe that uses dried beans and mentions a slow cooker in its instructions now shows a red food-safety warning, which also appears on its printout. [learn more...](#slow-cooker-beans)

<!--

```
Scope: usda_nutrients._ANTINUTRIENT_TABLE rewritten as whole-word regex patterns + suppress
patterns (was substring keywords: "pea" matched peaches, "oat" goat, "nut" nutmeg/doughnut/
nutritional yeast, "bean" jelly beans/coffee, "corn" cornstarch/popcorn/sweet corn); flags now
carry "group". Compared old vs new over all 334 food names in the owner's DB; every change
reviewed (two suppressions fixed: "gluten" only as vital wheat gluten; pasta/noodles out of the
dried-bean note). Lectin note text follows the FDA Bad Bug Book. New
usda_nutrients.slow_cooker_bean_risk(names, instructions); _recipe_detail_context() passes
slow_cooker_beans over every leaf food (sub-recipes opened); recipe_detail.html alert + card,
print.html above Instructions. Tests: TestAntinutrientMatching, TestSlowCookerBeanRisk
(tests/test_usda.py), tests/test_slow_cooker_beans.py. Part 9 gains #antinutrient-amounts.
```

-->

**PROGRAM: VITAMIN D DEFAULT FOLLOWS THE 2024 GUIDELINE**

**Load recommended Revised Optimal targets** in Settings → 5 now sets a vitamin D target only for a profile aged 75 or older, at 23 mcg; under 75, the RDA is your target. This follows the Endocrine Society's 2024 guideline, which advises against vitamin D above the RDA for healthy adults under 75. A vitamin D target you've already saved isn't changed. [learn more...](#optimal)

<!--

```
Scope: profile.compute_optimal_defaults() (VITAMIN_D_DEFAULT_MIN_AGE = 75,
VITAMIN_D_DEFAULT_75_PLUS_MCG = 23.0); tests/test_profile.py, tests/test_web.py; manual Part 4 V
and Part 9. Was a flat 50 mcg from Holick 2011 ([^12]). Demay 2024 ([^101]) names no optimal
dose; 23 mcg = weighted-average daily dose (~900 IU) of the trials behind its 75+ recommendation
(Recommendation 6, technical remarks). Saved targets untouched: a user who loaded the old
default keeps 50 mcg (the manual tells them).
```

-->

**MANUAL: APPENDICES A–C CHECKED AND SOURCED**

Appendices A–C now cite a source for each claim of fact. Appendix A's cocoa example uses NuMa's own reference values (cocoa turns out to fall just short of complete), and its chia figures are current. Each pantry food's amino acid note in Appendix B matches that food's USDA record. [learn more...](#citations-progress)

<!--

```
Scope: user-manual.md Part 10 A–C; footnotes [^110]–[^114]. A: cocoa example was USDA #169594
(alkali-processed, 18.1 g protein) with tryptophan reference 7; the 19.6 g / 0.293 g figures
are #169593, and FAO 2013's 6.6 gives 2.26; by NuMa's constants cocoa is incomplete (leucine
0.99, Met+Cys 0.98), so the "complete, 1.02-2.25" example moved to chia (1.22-3.99). Chia
table refreshed (Met+Cys 2.62, was 1.62), labeled pre-digestibility; "efficiently usable"
and the summary table's "full usability" reworded. B: every food scored from its USDA record
(protein_completeness); corrected almonds (most protein-dense nut here, short in lysine AND
Met+Cys), cashews (complete; not sulfur-poor), pecans/walnuts (lysine only), peanuts (lysine,
not Met+Cys), wheat (no threonine gap), tofu (firm-tofu record's low cystine), flax, oats,
cornmeal, nutritional yeast; Brazil nut selenium from USDA + Thomson 2008; chia "passes
undigested" claim dropped. C: Zeevi 2015, Vega-Lopez 2007, Evert 2019. Code comments in
usda_nutrients._AA_PAIRS said 22/38 mg/g (WHO 2007 adult); constants are FAO 2013's 23/41.
Open: chia's DIAAS figures disagree across NuMa's tables (0.82 digestibility in diaas.py,
0.56 and 0.77 in usda_nutrients.py).
```

-->

**MANUAL: ANTINUTRIENTS AND OXALATE SOURCED, BEAN COOKING ADVICE CORRECTED**

The Antinutrients and Oxalate sections now cite their sources. Following them, the advice for dried kidney beans is now to soak for at least 5 hours and boil for at least 30 minutes, as the US Food and Drug Administration recommends, and never to cook them in a slow cooker. [learn more...](#antinutrients)

<!--

```
Scope: Part 4 L and M; footnotes [^102]–[^109], [^11] enlarged. Corrections the sources forced:
sourdough phytate reduction "50-90%" -> Lopez 2001's 62% (yeast 38%, pre-fermented bran ~90%);
"boil at least 10 minutes destroys lectins and trypsin inhibitors" -> FDA Bad Bug Book: 10 min
destroyed PHA in one study but advises >=5 h soak + >=30 min boil, no slow cookers; trypsin
inhibitors more heat-stable (Aviles-Gaxiola 2018); "plants make these as a defense" -> true of
lectins/trypsin inhibitors, phytate is the seed's phosphorus store (Schlemmer 2009); spinach 5%
vs dairy 30% -> Heaney 1988's 5.1% vs 27.6%; nixtamalization "fully bioavailable" softened (WHO
2000). Oxalate: 40-50 mg/day sourced (U Michigan) with OHF's looser 100 mg; the five bands
labeled as NuMa's own cut-offs. Harvard spreadsheet confirmed "Posted Nov. 2023".
```

-->

**MANUAL: REVISED OPTIMAL TARGETS ASSESSED; VITAMIN D CAVEAT**

Part 9 now records, with sources, why magnesium, vitamin K2 and choline were not given a Revised Optimal default, and retires the age-group bundles idea that depended on them. The vitamin D default now carries a caveat: the 2011 guideline behind its 50 mcg has been replaced by the Endocrine Society's 2024 guideline, which advises against supplements above the RDA for healthy adults under 75. [learn more...](#expand-revised-optimal)

<!--

```
Scope: Part 9 (#expand-revised-optimal, bundles retired); Part 4 Revised Optimal section caveat;
footnotes [^96]-[^101]. Magnesium: Mah & Pitre 2021 (3 RCTs, 151 people, low/very low quality,
placebo-controlled only). K2: Hartley 2015 Cochrane; Shea 2021; USDA reports MK-4 only, not MK-7.
Choline: Wallace & Fulgoni 2017 (~8% of US adults meet the AI); Obeid & Karlsson 2023 (no
intervention studies in the elderly). Vitamin D: Demay 2024 (JCEM 109(8):1907) replaces Holick
2011 ([^12]). Default value unchanged pending the owner's decision (drop, or 75+ only).
```

-->

**PROGRAM: VITAMIN K FROM USDA CORRECTED**

USDA foods now get their real vitamin K, the vitamin K1 that leafy greens carry and that the daily goal is based on. Foods you saved before today showed little or none: raw spinach showed none at all. The Home page tells you how many are affected, and **Correct vitamin K for N USDA foods from USDA** on Foods → 9 fixes them in about a minute, keeping any vitamin K value you entered yourself. [learn more...](#vitamin-k-fix)

<!--

```
Scope: usda_api.NUTRIENT_MAP 1183 (menaquinone-4) -> 1185 (phylloquinone); the abridged
NUTRIENT_NUMBER_MAP "430" was already phylloquinone, so the two USDA paths disagreed.
Found while assessing a vitamin K2 Revised Optimal target (Part 9): 32 of 235 cached USDA
foods had any vitamin K, all MK-4 figures. New foods.vitamin_k_checked (migration: 0 for
fdc_id > 0); db.cache_food(vitamin_k_checked=True), demo_data passes False (starter_data.json
predates the fix). New numa_app/services/vitamin_k_repair.py, POST /food/cache/vitamin-k-repair,
Foods -> 9 section, Home notice. usda.get_nutrient_values(ids, number) generalizes
get_water_values() and keeps only requested ids (USDA answers an unknown id with ~50 unrelated
foods). db.replace_source_nutrient() replaces or removes in nutrients and source copy, skips a
user edit. water_backfill._cascade() takes the log wording. tests/test_vitamin_k_repair.py.
Curator follow-up: regenerate starter_data.json from a repaired DB.
```

-->

**MANUAL: WEEKLY SWEEP — "% INCREASE" EXPLAINED, DRINK WATER ESTIMATE DOCUMENTED**

The protein complement suggestions section now explains what a suggestion's "% increase" is measured from, and the water section says what happens when you tick **This food is a drink** on a food with no water value. The updates log is trimmed to the last two weeks. [learn more...](#tier-1-gap-closers)

<!--

```
Scope: weekly sweep 2026-10-14 (README-numa-documentation.md, Maintenance → Weekly sweep).
Item 1: CLAUDE.md package layout gained water.py and water_backfill.py; its nutrient-key
list gained water_g (was in NUTRIENT_MAP, not listed). Item 4: Sep 25-29 entries pruned. Items 2/3: clean (NuMa
capitalization; Bootstrap 5.3.8 still latest). Item 5: changelog bullets 1-79 checked
against the manual body; #17 (% increase from the real DCP) and #64 (estimated water on
ticking a drink) existed only in this log — now in Part 4 B Tier 1 and the water
section. Item 6: README.md Key features gained protein per meal, water tracking,
supplements; GL bullet gained estimated meal GI, daily target, swaps. Item 7: no gaps
found by identifier search. Item 8: link tests pass; 31 new external URLs, all DOIs
registered (403s are publisher bot-blocks); eatrightpro.org [^64] loops through an SSO
redirect to a 404 for curl but works in a browser (owner-checked) — its title corrected
to the page's own, "A Primer on Glycemic Index". Item 9: clean. Mutation churn:
usda_nutrients, complements, profile, glycemic_load flagged and run the same day
(88 new tests; details in README-numa-documentation.md's mutation log).
```

-->

**PROGRAM: RENAME ANY FOOD, USDA'S INCLUDED**

Every food's page now has **Rename this food** under its name. The new name reaches every recipe, meal and pantry line that uses the food. A USDA food stays linked to USDA: **Refresh from USDA** offers USDA's name beside yours, unticked, instead of putting it back by default. [learn more...](#rename-food)

<!--
```
Scope: food page (#rename), POST /food/{id}/rename -> db.rename_food_by_user() (sets
foods.name_by_user, propagate_food_name; not user_edited, names aren't tracked data).
incoming_review.meta_review(name_mine=) unticks the source's name and marks it "yours".
db.update_food_fields(name=) — Refresh taking a name — now also propagates it to
recipes/meals/pantry (it didn't before) and clears name_by_user.
```
-->

**PROGRAM: A DAY'S GLYCEMIC LOAD ROUNDED ONCE, NOT MEAL BY MEAL**

A day's glycemic load is now the meals' exact figures added up and then rounded, instead of the meals' rounded figures added up. The difference is at most a few tenths, but for small meals it always went the same way: two meals of 0.04 each used to add up to 0.0. [learn more...](#gl)

<!--
```
Scope: glycemic_load._result() adds "total_exact" (unrounded); combine_gl() sums it.
Top Contributors' by-item GL sums per-food _food_share() unrounded (an item was rounded
to 0.1 before summing). Found by tests/test_contributors_by_item_properties.py, which now
checks each item's GL against food_gl()/recipe_gl() total_exact. test_web's day-GL
figure for 100 g + 50 g rice is 30.7 (30.675), not 30.6.
```
-->

**PROGRAM: TOP CONTRIBUTORS WITH RECIPES KEPT WHOLE**

On a meal page with a recipe in it, Top Contributors now has a second table, **By meal item, recipes kept whole**. It ranks the meal's items as you logged them, so each recipe is one row instead of being split into its foods. It follows the same **Rank by** choice, including protein (each item's standalone DCP) and glycemic load. [learn more...](#contrib-by-item)

<!--
```
Scope: meal page Top Contributors. backend _meal_expand_for_diaas(): every leaf carries
item_id / item_name / item_fdc_id / item_recipe_id (its meal item). top_contributors.
rank_by_meal_item(): groups leaves by item — nutrient sum; GL via gl_for_leaves(); DCP via
diaas.meal_level_diaas() on the item's leaves pooled. meal_detail computes it only when a
recipe item exists, sliced to the same top_n; _top_contributors.html by_item() macro.
```
-->

**PROGRAM: SUPPLEMENTS, AND HOW MUCH CAME FROM THEM**

A food can now be marked **This is a supplement** on its page, and saving a custom food in supplement mode (a serving of 1 tablet, capsule, scoop and so on) marks it automatically. A supplement is never checked for calories, amino acids, GI or portions, weighs nothing, and reads per tablet; typing `2` when adding it means 2 tablets. Its nutrients still count everywhere, and every nutrient table for a meal, day, summary or recipe now shows how much of each nutrient came from supplements. [learn more...](#supplements)

<!--
```
Scope: numa_app/services/supplements.py (new): tag() adds "<key>__supp" copies at
summation (next to water.tag in recipe_nutrients, _meal_expand, whatif), supp_amount(),
unit_name(). db: foods.is_supplement (backfilled from supplement mode; those meals marked
stale), set_food_is_supplement(), supplement_ids(); recipe_compute_weight skips them.
Checks skipped: data_quality SUPPLEMENT_SKIPS (scan, issues_for_food, Claude fetch),
_foods_in_use, days-eaten carbs, water_backfill, db-check gaps, food-page gaps and AA
suggestion, _calorie_warnings, DIAAS missing-AA list, top_contributors no-data, GL
(_accumulate, gl_for_leaves), recipe_dcp per-100 g. UI: _supplement_toggle.html +
POST /food/{id}/supplement (cascades); food page per-tablet label; add-food row prefills
"1 tablet" (supplement_unit global); _parse_portion_str bare number = count units for a
supplement-mode portion; _nutrient_sections row "supp" -> "N from supplements" in meal,
day, summary, recipe, portion, trend and print tables.
```
-->

**PROGRAM: FIX FOOD DATA PROBLEMS IN ONE CLICK**

The **Food data problems** list on Foods → 9 now offers a fix under each problem it can solve. Where the figures point to a likely cause, such as kilojoules entered as calories or one serving's calories entered as per 100 g, it says so and offers that fix first. Each food also gets links to fix it by hand. Every fix is recorded on the food's page (what changed, from what, to what, and why), and on a USDA food a later Refresh shows the source's figure beside your correction instead of replacing it. [learn more...](#data-problem-fixes)

<!--
```
Scope: Foods -> 9 (food_cache_db_check.html), food page (#corrections), Refresh review.
data_quality: food_issues() issues carry "fixes" (_fix: id, label, changes, reason,
hint, estimated); _impossible_items() (negatives, mg->g, sugar->carbs, fat from parts),
_calorie_fixes() (kj_to_kcal when stored/4.184 passes calorie_mismatch, per_serving
from a gram serving_size, use_estimate marked estimated), estimate_calories;
apply_fix() re-derives fixes from the food as it is now (stale page -> fix_stale=1).
db: foods.corrections_json + correct_food_values() (sets/removes, estimated marks,
refresh_user_edited so outside-food corrections are "yours") + food_corrections()
(still-in-force only). POST /food/{id}/data-fix cascades (recipe_dcp). Per-row hand
fixes: Refresh from USDA (USDA ids), Fill in from another food, Edit values (custom).
```
-->

**PROGRAM: SYSTEM ISSUES ALERT ON EVERY PAGE**

When an automatic recalculation fails, a red alert now sits at the top of every page, Home included, with a link to Settings → 15. System Issues. Tick **Got it. Don't remind me again.** to hide it; you stay on the page you were on. [learn more...](#system-issues-howto)

<!--
```
Scope: base.html (#system-issues-banner, under the restart banner), backend
_system_issue_count() Jinja global (unacked recompute_errors; 0 on any DB error so it
can never break a page), /recompute-errors/ack-banner now takes return_to
(_safe_return_to). Home page's own copy of the banner removed.
```
-->

**PROGRAM: SETTINGS SECTIONS REORDERED**

The Settings page's sections are in a new order: 1–3 unchanged, then 4. Protein Digestibility Overrides, 5. Nutrient Targets - Researched (renamed from Nutrient Targets), 6. USDA API Key, 7. Glycemic Index Reference Table, 8. Glycemic Load, 9. Water Tracking, 10. Meals & Log columns, 11. Starter Data, 12. Keyboard Shortcuts, 13. Browser to Launch, 14. Data Quality Reminder, and 15. System Issues. The Alt+Shift shortcuts follow: digits for 1–9, `0` for 10, and `T`, `K`, `B`, `D`, `Y` for 11–15. [learn more...](#settings)

<!--
```
Scope: settings.html (sections moved, renumbered; data-ak keys; Keyboard Shortcuts list),
every "Settings -> N" reference in code comments, templates (home.html, _water_mark,
food_detail, _gl_result), README, and the manual's main text and pending log entries
(released entries left as written). Test test_settings_sections_order_and_shortcut_keys
pins the order, names and keys.
```
-->

**PROGRAM: GI LOOKUP UNDERSTANDS A FOOD'S FULL NAME**

The GI lookup's search box starts with the food's full name, and a long name such as "Peas, split, mature seeds, cooked, boiled, without salt" now finds peas, boiled ones first, instead of unrelated foods such as salted cassava. [learn more...](#gi-stand-in)

<!--
```
Scope: Foods -> Annotate -> Look up a GI value. gi_lookup.search() sends any query containing a
comma to _search_by_words(): rows must contain every word of the first comma part (the second if
the first is a USDA category: nuts, spices, beverages, seeds; else just its first word), ranked
generic before branded, then by shared remaining words (+1 when the row's own first part is the
food). Falls back to whole-string difflib matching when nothing qualifies. Typed queries without
a comma are unchanged.
```
-->

**PROGRAM: GI LOOKUP SAYS WHEN YOUR FOOD ISN'T IN THE TABLE, AND OFFERS STAND-INS**

When no row in the GI table is the food you searched for, only foods containing it, the Annotate page's lookup now says so above the results. Below them it offers plain rows for each word of the search as possible stand-ins, such as Peanuts for peanut butter. A stand-in you pick is saved with a source that says it was a stand-in. Plain foods are also listed before a named company's product when they match equally well. [learn more...](#gi-stand-in)

<!--
```
Scope: Foods -> Annotate -> Look up a GI value. gi_lookup.py: is_branded() (TM/(R) sign,
company form in brackets, or bracketed list ending in a country) leads _tiebreak();
has_direct_match() (plural-, word-order- and run-together-tolerant: "Cornflakes" for
"corn flakes"); stand_ins() returns plain rows per query word, excluding names already
in the results. /food/annotate/{id}/gi-lookup now returns direct_match and stand_ins;
food_annotate.html renders the note and a stand-ins table (row rendering factored into
rowHtml()), appending "used as a stand-in for ..." to the saved gi_source. Prompted by
"peanut butter": the 2021 table has no plain peanut butter row, only 20+ products
containing it.
```
-->

**PROGRAM: FOODS → 9 RANKS FOODS BY DAYS EATEN, AND FINDS THE GAPS THAT HIT THE MOST DAYS**

Foods → 9 has a new **Foods: days eaten** list. Choose how many days, and the date to go back from, and it shows every food you ate in them and on how many days, counting foods inside recipes. Two more tables pick out the foods with no GI that left a day's glycemic load incomplete, and the foods with no carbohydrate value, most days first. [learn more...](#days-eaten)

<!--

```
Scope: Foods -> Food Cache -> Database check (/food/cache/db-check), new section
#days-eaten; GET params de_days (default 30, 1-3650) and de_end (default today), bad
values fall back to defaults; the section opens when either is given.
data_quality.foods_days_eaten(conn, end_date, days): distinct meal_date per food, direct
or through logged recipes (_recipe_food_ids, recursive, memoized, cycle-safe);
gi_gap_days from glycemic_load's own day gaps (no_gi + not_wanted), so foods under the
1 g carbohydrate floor (spices) never count -- the per-100 g GI_LIST_MIN_CARBS rule
listed cinnamon/nutmeg/coffee powder at the top of the owner's real data; no-carbs
table skips foods whose "macros" group is marked not needed (supplements).
```

-->

**PROGRAM: DAILY GLYCEMIC LOAD SHOWS ON THE NUTRIENT PLOT FOR MOSTLY ANNOTATED DAYS**

The [Nutrient Plot](#nutrient-plot) now draws a day's glycemic load when foods with a GI make up at least 80% of its carbohydrate, as a hollow point meaning "at least this much", and a note under the plot says how many days are partial and how many were left out. Any nutrient you chose that has no data at all in the range is now named in a yellow note, instead of just not appearing.

<!--

```
Scope: Analysis -> Daily summary -> Nutrient Plot. glycemic_load.py: new
PLOT_MIN_GL_COVERAGE_PCT (80) and day_gl_plot_values() -> {date: (gl, partial)};
day_gl_total()/day_gl_totals() unchanged, so trend averages and the daily GL target
stay strict. backend.py: _nutrient_plot_raw_series uses it, tags the GL series with
partial/thin dates; _smoothed_plot_series turns them into a per-axis "hollow" list,
appends "(hollow = partial)" to the legend label (the image also shows on Home and in
print), and adds gl_partial_days / gl_thin_days / empty_series to the info dict.
plotting.line_plot_image: optional "hollow" list redraws those points as open circles.
nutrient_plot.html: the two notes. Cause: on the owner's real 30-day range every day had
some carb food without a GI, so the strict rule made every GL point nan and the series
silently drew nothing.
```

-->

#### October 13 updates

**PROGRAM: ROW BUTTONS KEEP YOUR PLACE IN FOOD CACHE, PANTRY AND RECIPES**

Clicking **Add to pantry**, **Refresh** or the starter button on a [Food Cache](#food-cache-web) row now brings you back to the same list — same filter, same sort, archived items shown or hidden as before — scrolled to where you were. Archive and Delete on Food Cache, Pantry and Recipes already work in place; now they keep your filter even when the page has to reload, and Pantry's show/hide-archived button keeps its filter as well.

<!--

```
Scope: Foods -> Food Cache, Foods -> My Pantry, Recipes list; web/templates/base.html,
food_cache.html, pantry.html, recipes.html, web/backend.py, tests/test_web.py.
New sitewide keep-scroll script in base.html: a form/link with class js-keep-scroll and
data-return-to="<list URL>" saves {url, scrollY, time} in sessionStorage; restored only
when exactly that URL (decoded, no hash) loads again within 30 min, so unrelated later
visits start at the top. Replaces food_cache.html's own starter-toggle-only version.
Food Cache's next URLs (pantry add, review-incoming, toggle-starter) now carry
show_archived and drop the #food-N anchor that jumped the page to the row.
Pantry/Recipes Archive/Remove/Delete forms carry a hidden next (the filtered list URL);
the non-fetch fallback redirects there via new _list_return() (flags appended), default
unchanged for callers without next. Pantry's archived_toggle now passes filter.
```

-->

**PROGRAM: RAW-OR-COOKED WARNING BESIDE THE GI BOX**

The Annotate page now shows a yellow warning right under the GI box: pick the GI for the form you actually eat, since raw and cooked versions of one food can differ fourfold. When the food's own name says it is raw, dry, uncooked or a flour, the warning says so and suggests using the GI of what you make from it, or leaving it blank. [learn more...](#annotate)

<!--
```
Scope: Foods → Annotate a Food; web/templates/food_annotate.html (#gi-raw-cooked-warning),
web/backend.py food_annotate_edit_get (looks_uncooked flag, reusing
glycemic_load.looks_uncooked — same name match the recipe ingredient flag uses),
tests/test_web.py::test_annotate_page_warns_raw_versus_cooked_gi.
```
-->

**PROGRAM: GI LOOKUP PUTS THE PLAIN INGREDIENT FIRST**

Searching the Annotate page's GI lookup for a common ingredient such as "wheat flour" now lists the ingredient itself first, ahead of the cakes, breads and muffins made with it. [learn more...](#annotate)

<!--
```
Scope: Foods → Annotate a Food → GI lookup; gi_lookup.py (_tiebreak, search), tests/test_gi_lookup.py.
Every name containing the query scored a flat 0.9, so the 264 rows of the 2021 table
containing "wheat flour" tied and kept table order; only the first 8 are shown, all cakes.
Ties now break by: first comma-separated part equals the query, name starts with the
query, first part contains the query, then shorter name.
```
-->

**PROGRAM: NEW DAYS FOLLOW YOUR CURRENT PROFILE**

A day you log for the first time is now scored against your current profile from the start, with its **current profile** switch already ticked, so its goals follow every profile change you save. Untick the switch to keep that day's profile as it was when you logged it. [learn more...](#day-profile)

<!--

```
Scope: Meals & Log / day pages; numa_app/services/day_profile.py ensure_day_profile() now pins
then calls db.day_profile_set_following, so the first snapshot becomes the kept original and
follows_current = 1. restore_pinned() returns to that snapshot. Applies to startup backfill too.
Tests that needed a frozen day now call restore_pinned() after ensure_day_profile().
```

-->

**PROGRAM: A DRINK WITH NO WATER VALUE GETS AN ESTIMATED ONE**

Ticking **This food is a drink** on a food that has no water value, which is true of most branded drinks since US labels don't list water, now fills one in: 100 g minus the food's protein, carbs and fat. The food's page says it's an estimate. A measured water value is never replaced. [learn more...](#water)

<!--

```
Scope: food page drink toggle (POST /food/{fdc_id}/drink, web/backend.py); water.estimate_water();
food_detail.html note. Before, the flag saved but a branded food (e.g. APPLE CIDER, 2440745) has no
water_g, so tag() added nothing and no water from drinks appeared. Written with db.fill_source_nutrient
(source copy too, so not taken for a user edit) and marked in estimated_keys. Ignores ash/alcohol,
so slightly high. Only on ticking; unticking leaves the value.
```

-->

**PROGRAM: GLYCEMIC LOAD SWITCH, AND THE DAY'S GL SO FAR**

Settings → 8 has a **Show glycemic load** switch, on by default. Turned off, every glycemic load figure, column, sort, plot series, trend and target disappears, along with the estimated GI; GI values stay, and nothing is deleted. With it on, a meal's page now shows the day's glycemic load up to and including that meal under its title, and a day's page shows the day's total so far. [learn more...](#glycemic)

<!--

```
Scope: Settings → 8 (#gl-tracking, POST /settings/gl, prefs track_gl,
default True; _track_gl(), Jinja global show_gl()). Off: GL sections and
sidebar entries on meal/day/recipe/summary/recipe-portion pages, food
page GL (GI kept), trend average card, Meals & Log and Recent Days
columns and GL sort (show_gl_col = _track_gl() and not _gi_opt_out()),
Top Contributors' GL rank option (and a stale ?rank=gl), print section
"glycemic_load", Compare gl_rows, plot series key "gl", What-if summary
cell / recipe row. The Settings → 1 daily target box is hidden, not
removed, so a profile save keeps it. New _gl_day_so_far(): combine_gl of
the day's meals up to this one (db.meal_list_by_date order, created_at)
+ gl_target_status against the date's pinned target; meal_day uses its
existing whole-day gl. Shared macro _gl_result.gl_so_far_line(). 3 tests.
```

-->

**PROGRAM: GLYCEMIC LOAD ON MEALS & LOG**

Meals & Log now has a GL column right after Calories: each meal's glycemic load, with its band beneath it. When some foods have no GI value, it reads "≥ 9.1" over "49% with GI", the share of the meal's carbohydrate that does have one. A note under the table explains both, and the list can be sorted by GL. [learn more...](#meals-list)

<!--

```
Scope: Meals & Log (web/backend.py _meals_list_ctx, meals_list,
_meals_sorted_by_gl; web/templates/meals.html). GL is worked out live per
row with meal_gl() (_compute_gl), hidden with every other GL figure when
GI is opted out (show_gl_col, as Recent Days). Sort "gl" is new in
_MEALS_SORT_KEYS: GL isn't stored, so it fetches every meal in range
(meal_list_recent limit=-1), computes each, sorts by (no figure,
-total) stably, then slices; falls back to date when GI is opted out.
Coverage is written "N% with GI" rather than "(N%)", since parentheses
in this table already mean a meal's share of the day's goal. 3 tests.
```

-->

**PROGRAM: NOTE WHERE A GI OR DIAAS VALUE CAME FROM**

The Annotate page now has a box under each of the GI and DIAAS values for where that value came from. The GI one fills itself in when you pick from the lookup. The food's page shows both. When the GI lookup finds nothing, the page now lists what to try next, and the DIAAS box explains how to estimate a value from the food's main protein source. [learn more...](#annotate)

<!--

```
Scope: Foods → Annotate a Food (web/templates/food_annotate.html), the
food's page, Claude imports. New food_annotations.diaas_source column
(migration); set_food_annotation()/upsert_food_annotation() take
diaas_source, and set_ drops it when diaas_estimate is None (as gi_source).
gi_source is now a visible text input; the page script clears it on a
hand-typed GI only while it holds a lookup citation (LOOKUP_SOURCE_RE on
the lookup's wording), never a typed source. claude_fetch writes the
reply's diaas_source to the column instead of appending "DIAAS source: ..."
to the food's notes. GI no-match advice is a <template> swapped into the
results box. Tests: test_web.py (typed sources saved/shown, orphan source
dropped, no-match and DIAAS help), test_claude_fetch.py, two e2e tests.
```

-->

**PROGRAM: ESTIMATED GI FOR MEALS, RECIPES AND DAYS**

Under the glycemic load of a meal, recipe or day you now see an estimated GI: each food's GI, weighted by its carbohydrate. It says how much of the carbohydrate it covers, isn't given under 10 g of carbohydrate, notes when it is close to a band boundary, and in a recipe flags raw, dry or flour ingredients whose GI may not be for the form they're eaten in, with a **These ingredients are eaten as listed** switch to stop that. [learn more...](#mixture-gi)

<!--

```
Scope: recipe, recipe portion, meal, day, Daily Summary and print pages
(web/templates/_gl_result.html gi_estimate(), called at the end of
gl_figure()); numa_app/services/glycemic_load.py. _result() gains gi
(100 x GL / carbs with a GI, rounded), gi_band / gi_near (bands 55/69,
"close to" within 5 of a boundary), gi_too_little_carb (counted available
carbs < GI_MIN_CARBS_G = 10), mixture (False for food_gl, whose GI is the
food's own) and uncooked [{name, recipe_id, recipe}]. looks_uncooked()
matches raw|uncooked|unprepared|dry|flour, not "dried"; checked only for a
recipe's direct ingredients whose GI counts with >= 1 g carbs, unless the
recipe's new recipes.gi_as_eaten column is set (POST
/recipe/{id}/gi-as-eaten). combine_gl() merges the flags. Method and
cautions from glycemic-index-food-mixture.md (Dodd 2011, Spolar 2006 —
new footnotes 94, 95). New manual section #mixture-gi.
```

-->

**PROGRAM: GLYCEMIC LOAD USES AVAILABLE CARBOHYDRATE**

Glycemic load now counts only available carbohydrate, the part that's digested to glucose, as GI itself is defined. Foods from USDA, the Canadian table, Open Food Facts and your own entries have their fiber taken off; the UK, Australian and French tables already leave it out. High-fiber foods such as beans now show a lower, more accurate GL. [learn more...](#glycemic)

<!--

```
Scope: every GL figure, Top Contributors' GL ranking and lower-GL swaps.
glycemic_load.available_carbs_100g(nutrients, fdc_id): carbs_g as stored
for CoFID/AFCD/CIQUAL (food_ids.source_key(), new), else max(carbs_g -
fiber_g, 0); used by _food_share() (now takes fdc_id), top_contributors
rank_contributors_by_gl() and gl_swaps.suggest_swaps(). Older food
versions are treated as total carbohydrate (nearly all USDA). EU products
on OFF already exclude fiber, so they now read low by their fiber — the
label doesn't say which convention it uses. data_quality's
GI_LIST_MIN_CARBS check still uses total carbs (deliberately unchanged).
```

-->

**MANUAL: BOOKMARKS IN THE MANUAL**

The manual's sidebar now has a **Bookmark this section** button and a **Bookmarks** drop-down list: bookmark the section you're reading, jump back to any bookmark from the list, and remove one or all of them there. Bookmarked sections get a ★ in the table of contents. [learn more...](#bookmarks-howto)

<!--

```
Scope: user manual page (scripts/build_manual.py — #bm-bar HTML, CSS, a new
Bookmarks script). Bookmarks are heading ids in localStorage
(numa_manual_bookmarks, [{id, text}]); the scroll-spy now fires a
"manual-section" event naming the section being read, which the toggle
button bookmarks. List sorted in manual order, with the enclosing headings
as a path; a vanished id stays listed as no longer in the manual. TOC links
get .toc-bookmarked (★) and their ancestors .toc-bookmark-inside (☆).
Outside click / Escape close the drop-down; a storage event keeps other open
manual tabs in step. New Part 7 section F (#bookmarks-howto);
tests/e2e/test_manual_bookmarks_e2e.py.
```

-->

#### October 12 updates

**PROGRAM: FILL IN A FOOD STRAIGHT FROM COMPARE**

When you compare search results from a food's **Fill in nutrients from another food** page, Compare now has a **Fill in ... from ...** button for each of the other foods; it opens the review screen to copy that food's values in. [learn more...](#review-incoming)

<!--
```
Scope: Compare (/compare with return_to=/food/<id>/fill-from...); web/backend.py
_compare_fill_target() reads the fill-from target out of return_to, compare.html
renders one review-incoming?source=food link per other compared food (recipes and
the target itself skipped). Also: Review incoming's nutrient columns now show 3
decimal places.
```
-->

**PROGRAM: LINOLEIC ACID NOW HAS A DAILY GOAL**

The omega-6 row (Linoleic) now has a Daily Goal, the official Adequate Intake: 17 g a day for men and 12 g for women under 51, 14 and 11 g from 51 on. It's the typical U.S. intake rather than a measured need, so read a small shortfall loosely. [learn more...](#omega3)

<!--

```
Scope: profile.compute_rda() adds omega6_la_mg (minimum), IOM 2005 AI in mg: 17000/12000 under 51,
14000/11000 at 51+, "other" = midpoint (14500/12500). tests/test_profile.py TestOmega6La. Manual: goals list
(#goals) gains an Omega-6 linoleic acid entry; #omega3 last paragraph and Appendix G #key-la rewritten to match.
```

-->

**MANUAL: SOURCES FOR AMINO ACIDS, PROTEIN COMPLEMENTS, OMEGA-3 AND GLYCEMIC LOAD**

Four more parts of Part 4 now have footnotes for their research claims: why nine amino acids are essential and why Met+Cys and Phe+Tyr are scored as pairs, the main claims behind protein complement suggestions, how poorly ALA converts to EPA and DHA, and how fat, protein, fiber and vinegar soften a meal's blood-glucose rise. The omega-6 note also now says correctly that linoleic acid has an official Adequate Intake. [learn more...](#citations-progress)

<!--

```
Scope: user-manual.md Part 4 sections A (#aa), B (#comp), O (#gl, #gl-uses), U (#omega3); Part 9 #citations-progress
checklist (four items moved from Still to source to Sourced); footnotes 86-93 added (Mathai 2017, Davis &
Kris-Etherton 2003, Burdge & Calder 2005, Moghaddam 2006, Jenkins 1978, Wolever 2006, Flint 2004, Ostman 2005),
existing 13/14/15/16/60 cited at new points. Corrections made while sourcing: the inline "<sup>[FAO 2013]</sup>"
replaced by footnote 16 and the vague "good quality for a varied diet" by FAO's actual "good" band (0.75-0.99);
"commonly cited 5-10% ... considerably less for DHA" made exact (under 5-10% EPA, 2-5% DHA); omega-3 section
previously said only ALA has an AI and that most diets "comfortably exceed" linoleic acid's AI -- both wrong (IOM
2005 sets LA AI at 17/12 g, at median US intake). No program change: profile.py still gives no LA Daily Goal.
```

-->

**PROGRAM: A PLAIN NUMBER FOR A RECIPE'S AMOUNT NOW MEANS GRAMS**

Typing a number on its own as a recipe's amount (in a meal's Items or add-food panel, or as a sub-recipe on Edit Recipe) now means grams, just as it does for a food: `29` is 29 g. For servings, add the word: `1 1/8 srv` or `2 servings`. Amounts already shown in those boxes include the word, so saving one unchanged keeps it. [learn more...](#portions-vs-servings)

<!--

```
Scope: numa_app/services/portions.py parse_recipe_amount() — no unit -> grams through serving_g (EntryError naming the bare-number rule when the serving weight is unknown); servings only with srv/serving/servings. Callers in web/backend.py: meal add-recipe default "1 serving" (older numeric `servings` field read as "<n> servings"); sub-recipe add likewise (precedence-safe rewrite). Prefills now "<n> serving(s)": meal.html Items edit box, recipe_edit.html sub-recipe edit box; _add_food_row.html and _recipe_search_rows.html default "1 serving"; placeholders/hints say a bare number = grams. Found when "29" for R54 in meal 184 logged 29 servings (~1,015 g). Tests: test_portions.py (bare number = grams, needs serving weight), test_web.py recipe/sub-recipe amount tests, test_recipe_serving_weight.py updated to the new rule.
```

-->

**PROGRAM: SEARCH FOR A FOOD OR RECIPE BY ITS CODE**

Any food or recipe search box, such as a meal's add-food panel, now takes a code: type **R21**, **U171477** or **UD4** and that one recipe or food is the result, instantly, even offline. A plain number works too for a food in your Food Cache. [learn more...](#search-by-code)

<!--

```
Scope: every search screen, via web/backend.py _run_food_search() -> new _code_search_results() (food_ids.parse_code, or a bare digit string that is a foods.fdc_id). One-row result, code_match flag; bypasses Source filter and archived; respects foods_only / exclude_recipe_id / exclude_fdc_id; unknown code falls through to the normal name search. _search_local_results' row building split into _recipe_search_rows() / _cached_search_rows() for reuse. Search inputs (search, meal, recipe_edit, compare, convert, analyze-portion, fill-from, custom-food pickers) get a title tooltip. Tests: test_search_by_typed_code_finds_that_one_item.
```

-->

**PROGRAM: FOODS → 9 CAN RECORD "HAS NONE", CONFIRM CALORIES, AND FIND AMINO ACIDS**

In Foods → 9's *Missing nutrient data* list, each gap now has a **has none (0)** box beside **not needed**: tick it for a food that truly has none of that group (no phytonutrients in meat), save, and NuMa records 0 for each missing value, so the food counts as 0 everywhere. **Mark column has none** ticks a whole column. The *Food data problems* list has a **These calories are right — stop flagging them** button beside each calorie mismatch, and the list of foods with no amino acid data has a **find amino acid data** link beside each food. [learn more...](#data-completeness-has-none)

<!--

```
Scope: Foods -> 9 (web/templates/food_cache_db_check.html, web/backend.py food_cache_completeness_save / food_cache_db_check_get). New `zero` form field ("fdc_id:group") -> data_completeness.group_none_keys() (blank keys of the group only; never "aa") written as 0 via db.merge_user_supplied_nutrients (user edit; calorie save-check runs), then recipe_dcp.cascade_food_change per food; redirect carries zeroed=N for the saved note. JS confirm before saving any "has none" ticks; "Mark column has none" shares the column-toggle code with "Mark column not needed". Food data problems rows: calories_mismatch gets the existing /food/{id}/data-ignore calories_ok POST with next=#calories. missing-aa rows get fill_url (top_contributors.fill_url, is_dcp; custom profiles -> Edit page). Save button relabelled. Tests: test_db_check_has_none_records_zero_for_group.
```

-->

**PROGRAM: ANSWER THE NO-DATA LIST UNDER TOP CONTRIBUTORS IN ONE CLICK**

Each food in the list of foods with no data under Top Contributors now has two more buttons. **Has none — record 0** stores 0 for a food that truly contains none of that nutrient (no B12 in a plant food), so it counts everywhere. **Not needed for this food** stops listing a food whose gap is too small to matter (the iodine in a pinch of spice), for that nutrient only. Foods marked not needed move to a line under the list with an **undo**, and their own pages show the mark too. [learn more...](#contrib-no-data-answers)

<!--

```
Scope: meal and recipe pages, Top Contributors (web/templates/_top_contributors.html missing_table + _gap_button; new POST /food/{fdc_id}/data-gap with action none|not_needed|needed, key, dcp, next). data_completeness: IGNORE_KEYS, ignore_key() (DCP -> "aa"; one-nutrient group water -> "water"; else the nutrient key itself, stored in food_data_ignores alongside group keys), nutrient_ignored() (nutrient or its group), none_keys() (DCP: protein_g only when absent). top_contributors.missing_contributors() takes ignores and returns ignored/can_zero per row; backend _build_contributors passes db.food_data_ignores. "none" writes blank keys only via merge_user_supplied_nutrients + cascade_food_change. Per-nutrient ignores are also dropped from Claude gap prompts (claude-fetch requested keys) and listed with (undo) on the food page (data_nutrients_ignored). The list's buttons return via next=location + #contrib-missing, which reopens the folded list. Previously a "not needed" mark never removed a food from this list. Tests: test_top_contributors.py (flags, helpers), test_web.py test_top_contributors_no_data_answers.
```

-->

#### October 11 updates

**PROGRAM: FINDING DATA A FOOD IS MISSING**

When Top Contributors lists foods with no data for a nutrient, each one now has a **Find this data** button. It opens **Fill in nutrients from another food**, already searching USDA, the other food tables and your Food Cache for that food's name, so you can copy the missing value from a match. A **where to find it** link under the list opens that nutrient's entry in Appendix G. Every entry there now has a **Where to find it** line saying which sources have that nutrient and which to try first, and a new section gives the general order: USDA, then the other national tables, the label, a similar food, Claude, and finally accepting that nobody has measured it. The UK, Australian and French food tables bundled with NuMa now include water, so a food missing water can usually take it from one of them. [learn more...](#contrib-find-data)

<!--
```
Scope: Top Contributors no-data list (meal, recipe pages) -> Fill in from
another food; manual Appendix G; bundled static datasets.
- top_contributors.source_anchor(key, is_dcp) maps every _NUTRIENT_GROUPS
  key to its Appendix G anchor (DCP -> #key-sources-aa, unknown ->
  #key-sources); registered as Jinja global contrib_source_anchor.
- top_contributors.fill_url() builds /food/{id}/fill-from?q=<name>&want=<key>
  (starter "* " prefix stripped); a custom profile (user_drafted, id < 0)
  gets its Edit page with nutrient_source_q / aa_source_q instead, matching
  food_detail.html's own button rule; None for recipe / name-only rows.
  _build_contributors() looks each missing row's food up for that.
- food_fill_from: optional want= (aa or a known nutrient key) shows an info
  box naming the nutrient and linking its Appendix G entry; a hidden input
  keeps it across a new search. Unknown want is ignored.
- Manual: Appendix G gets "When a food has no data for a nutrient"
  (#key-sources, #key-sources-aa), a new Water group/entry (#key-water),
  and a "Where to find it" line on every nutrient, written from measured
  per-key coverage of the bundled tables (CoFID omega 0%, AFCD AA ~12%,
  choline only USDA/CNF, etc.). Notes two traps: CoFID/AFCD/CIQUAL carbs
  are available carbohydrate (fiber excluded), and CNF/CIQUAL vitamin A is
  retinol only. Top Contributors section gets #contrib-find-data; the
  water section's "bundled tables don't include it yet" line corrected.
- build_cofid/afcd/ciqual_data.py map water ("Water (g)", "Moisture
  (water) (g)", "Water (g/100g)"); data files regenerated from the same
  editions (unchanged scripts reproduced the committed files byte for
  byte first), so the diff is water_g additions only: CoFID 2855/2886,
  AFCD 1588/1588, CIQUAL 2934/3484 foods.
- Tests: test_top_contributors (anchor for every key exists in the manual
  with a Where-to-find line; fill_url cases), test_web (row link, manual
  link, fill-from want box), test_cofid/afcd/ciqual (shipped file has water).
```
-->

**MANUAL: TABLE OF CONTENTS OPENS ONE LEVEL AT A TIME**

The manual's table of contents now starts closed and opens one level at a time: click the small ▸ arrow beside a title to see the next level down, or double-click the arrow to open everything below it. A short "How to use this list" box under the contents explains this the first time you open the manual. [learn more...](#toc-howto)

<!--
```
Scope: user-manual.html sidebar TOC -- scripts/build_manual.py (JS + CSS).
Toggles were only on h2-level entries, and opening one showed its whole
outline at every depth. Now every TOC li with a child ul gets a toggle;
all start collapsed (scroll-spy's expandAncestors opens the path to the
current section). Single click on the arrow opens one level and closes
any descendants; dblclick (which arrives after two clicks that cancel
out) opens or closes the whole branch based on the starting state.
Expand all / Collapse all now acts on every level and starts as
"Expand all"; it moved from the search row (where it read as part of
search's ▲/▼ buttons) to the Contents h2. New #toc-tips box appended
under the TOC, dismissed via
localStorage numa_manual_toc_tips_hidden; a "How to use this list" link
in the Contents h2 re-shows it. New Part 7 section E (#toc-howto).
```
-->

**PROGRAM: TOP CONTRIBUTORS NAMES THE FOODS WITH NO DATA**

Under the Top Contributors table on a meal or recipe page, you can open a second table of the foods that have no data for the nutrient you ranked by (for Protein, no amino acid data), with the amount used, so you can see what the total may be missing. [learn more...](#top-contributors)

<!--
```
Scope: meal and recipe pages, Top Contributors. New
top_contributors.missing_contributors() (absent key = no data; stored 0 is
data; DCP = protein but no has_amino_acid_data(), or no protein figure);
_build_contributors() returns "missing", computed over leaf foods (recipe
page passes calorie_leaves, since its ranking keeps sub-recipes whole);
_top_contributors.html missing_table() in a folded <details>. Not for GL
(gl_gaps already covers it). Tests: test_top_contributors.py, test_web.py.
```
-->

**PROGRAM: TYPE A SUB-RECIPE'S AMOUNT AS SERVINGS, WEIGHT OR VOLUME**

Adding a recipe as an ingredient on Edit Recipe, or editing one already there, now takes the same amounts as a recipe in a meal: servings with fractions (`1 1/8`), a weight (`150 g`), or a volume (`3/4 c`). [learn more...](#portions-vs-servings)

<!--
```
Scope: Edit Recipe search rows (_recipe_search_rows.html) and ingredient Edit
box (recipe_edit.html); POST /recipe/{id}/ingredient/add-recipe (field amount;
old servings + amount_unit=g still read) and /recipe/{id}/ingredient/{ing}/edit,
both through portions.parse_recipe_amount(). The number box + servings/grams
select is gone. Also fixed: the Edit box prefill used
round(2)|replace('.0',''), which showed 10.05 servings as "105" and 1.125 as 1.13.
```
-->

**PROGRAM: TYPE A RECIPE'S AMOUNT IN A MEAL AS SERVINGS, WEIGHT OR VOLUME**

When you add a recipe to a meal, or edit one already there, its Amount box takes servings with fractions (`1 1/8`, `1.125`), a weight (`200 g`), or a volume (`3/4 c`), converting a volume through the recipe's Total yield volume or, failing that, a serving description such as "2/3 cup". [learn more...](#portions-vs-servings)

<!--
```
Scope: meal page add row (_add_food_row.html) and logged recipe Edit box
(meal.html); POST /meal/{id}/add-recipe (field amount) and /meal/{id}/update/{item}.
New portions.parse_recipe_amount() + _volume_ml(); Jinja global
serving_volume_ml(). Root cause: three type="number" boxes held by the browser
to step 0.01, so 1.125 servings was refused; volume needed Total yield volume
and took only a bare number in its unit. Radios + recipeAmtSwitch() JS removed.
Tests: test_portions.py, test_web.py.
```
-->

**PROGRAM: A FOOD'S NOTES SHOW WITH ITS ANALYSIS**

A food's page now starts with its notes, and the prep context you gave it on the Annotate page, and its printout can include them. A recipe's notes also show when you analyze a portion of it. [learn more...](#food-notes)

<!--

```
food_detail.html: new "Notes" section (sec-food-notes, own sidebar entry), shown only when
foods.notes or food_annotations.prep_context is set; neither was displayed anywhere except their
edit forms. _food_detail_context() puts both on ctx["food"]; _food_available_sections() offers
"notes" for the food printout; print.html renders it. food_analyze_recipe_portion.html shows
recipes.notes (the recipe page and its printout already did).
```

-->

**PROGRAM: FOOD USE IN RECIPES CAN FILTER BY NAME**

Analysis → Food use in recipes has a name box, so you can show just the foods and recipes whose name contains the words you type. [learn more...](#fooduse-recipes-name)

<!--

```
GET /analysis/food-use-recipes ?name= (name_filter, alias "name": the aggregation loop's own
`name` variable would shadow it). All-words, case-insensitive substring match on the row name,
applied after protein_only; counts/percentages unchanged. Carried through the substitute POST and
its redirect. Heading shows "N of M rows"; an empty match has its own message.
```

-->

**PROGRAM: RENAMING A FOOD RENAMES IT IN YOUR RECIPES, MEALS AND PANTRY**

When you rename a food, the new name now shows on every recipe ingredient, logged meal item and pantry entry that uses it, so the old name no longer lingers there. [learn more...](#food-rename)

<!--

```
Foods -> food Edit page (and any update_cached_food_profile() caller: USDA refresh, AA estimate,
copy nutrients). db.update_cached_food_profile() now reads the old name first and, when it changed,
calls new db.propagate_food_name(): recipe_ingredients (fdc_id match, not sub-recipe lines),
meal_items (item_type 'food') and pantry rows take the new name, each keeping its own "* " starter
marker; a diaas_overrides row under the old name moves to the new one (digestibility is looked up
by the line's name). Returns the count, shown as a note on the Edit page. rename_cached_food()
(the curator starter toggle) deliberately unchanged. Tests: tests/test_db.py
TestFoodRenamePropagates.
```

-->

**PROGRAM: COMPARE SHOWS EVERY NUTRIENT, AND SAYS WHICH HAVE NO DATA**

Compare's nutrient table now has every nutrient a food's own analysis shows, including the omega fatty acids, iodine and selenium, and a yellow box above it names any nutrient left out because none of the items has data for it. [learn more...](#compare-nutrients)

<!--

```
Compare -> Nutrient comparison. usda_nutrients.COMPARE_GROUPS had never gained the Omega Fatty Acids
group, iodine_mcg or selenium_mcg that _NUTRIENT_GROUPS (web/backend.py) got, so those rows could
never appear. COMPARE_GROUPS now mirrors _NUTRIENT_GROUPS (Water as its own group, water_g only --
the drinks/food split is a day/meal-total thing) plus Amino Acids; a test checks the two stay in
step. New _compare_omitted() lists the shown-but-empty nutrients for the alert in compare.html.
```

-->

**PROGRAM: STARTER RECIPES IN SETTINGS SHOW THEIR CODES**

The list of improved starter recipes in Settings now shows each one's code beside its name.

**PROGRAM: COMPARE RECIPES AS WRITTEN**

Compare has a new **Compare amounts** choice: per 100 g (as before), one serving of each recipe as written, or each whole recipe as written, with every ingredient's typed measure beside its grams. [learn more...](#comparison-basis)

<!--
```
web/backend.py _COMPARE_BASES / _compare_basis() (prefs compare_basis);
_load_compare_entry(basis): scale 100/batch g, 1/servings, or 1; entry
basis_label for the nutrient table heading and the CSV header; typed unit
shown with the grams in "recipe" mode; weight_complete forced True outside
per-100 g (nothing is weight-scaled). compare.html: selector above the
tables (only when a recipe is compared), headings and notes per basis.
Starter recipes: demo_data._relevant() adds recipe_ids (name -> local id),
used by settings.html's improved-recipes list.
```
-->

**PROGRAM: RECIPES BUILT ON A SUB-RECIPE NOW WEIGH WHAT THEY SHOULD**

Compare now weighs a recipe correctly when it uses a sub-recipe that has no total weight of its own: NuMa adds up that sub-recipe's own ingredients instead. Before, such a sub-recipe counted as weighing nothing, so the recipe looked far lighter than it is and every per-100 g figure on Compare (nutrients, and each ingredient's share) came out far too high. [learn more...](#comparison-estimate)

<!--
```
Reported on /compare?items=r23,r66,r69: R66 and R69 differ only by 2 T salsa +
1 t soy sauce in R69, yet okara flour showed 100 g/100 g in R66 vs 47 g in R69.
db.recipe_compute_weight() read a sub-recipe's stored total_weight only, so the
smoothie-core sub-recipe (R63, no total weight) added 0 g: R66 = 33 g (okara
alone), R69 = 70 g. Now _sub_recipe_serving_grams(): stated total weight,
converted from its unit (it was taken as grams), else the sub-recipe's own
ingredients, recursively, with a cycle guard. A deleted sub-recipe line
(ref_recipe_deleted) now makes the sum incomplete instead of adding its
"1 serving" amount as 1 g. R66 now 140 g, R69 177 g (okara 23.6 vs 18.6 g/100 g).
Also feeds recipe_serving_grams() (meal amounts in grams) through the same
path. Tests: tests/test_recipe_serving_weight.py TestComputeWeightThroughSubRecipes.
```
-->

**PROGRAM: EVERY FOOD AND RECIPE NAME SHOWS ITS CODE**

Wherever NuMa shows a food or recipe by name, its code (U171477, R21 ...) now shows beside it, including the headings of all four tables on Compare and every row of its ingredient table. A test now checks every page, so a new one can't leave the code out.

<!--
```
Compare: three table headings and the ingredient rows had no code; ingredient
rows are now keyed by food/recipe ID, so two different foods sharing a name
stay separate rows. Also fixed: food-search result rows (Analyze portion,
Convert), calorie and food-data notes, What-if recipe lists, Annotate, Foods ->
9 lists (completeness, data problems, amino acids/portions/GI, old copies,
orphaned meal items), Convert, Fill-from / Review-incoming / Copy-fields /
Oxalate-link headings, the Add-to-pantry form, meal/day/summary/recipe
digestibility tables (recipe rows), antinutrient cards, oxalate tables and
"No oxalate data for", missing-AA lists, meal-history search, recipe-edit
ingredient rows and relink choices, translate preview, print pages, starter
data lists, stale-amounts table. Data added: oxalate rows/missing_ids,
antinutrient fdc_id/recipe_id, starter recipe id and improved-food code.
tests/test_food_id_tags.py scans web/templates; exemptions (meal names,
import previews, name-keyed DIAAS overrides) listed with reasons.
```
-->

**MANUAL: PDCAAS IN THE GLOSSARY**

The glossary now has an entry for PDCAAS, the older protein-quality score that DIAAS replaced. Some foods' notes quote a PDCAAS figure from their source; the entry says why it isn't the same as a DIAAS. [learn more...](#gloss-pdcaas)

**PROGRAM: MANUAL SEARCH SAYS SO WHEN NOTHING MATCHES**

A manual search that finds nothing now says so in a yellow box, naming what you searched for, instead of a line of tiny gray text that was easy to miss. [learn more...](#search-howto)

<!--
```
scripts/build_manual.py: setCount(txt, none) toggles #search-count.search-none
(14px bold, amber box); the message names the query and suggests unticking
"Only show things you can do" / Match case / Whole words only when ticked.
```
-->

**PROGRAM: MEALS & LOG EXPLAINS ITS PERCENTAGES**

A note above the Meals & Log table now says what the percentages in parentheses are: each meal's share of the day's goal for that nutrient. [learn more...](#meals-list)

**PROGRAM: PROFILE CHANGES REACH TODAY, AND ANY DAY YOU CHOOSE**

Save your profile and today is re-scored against it at once. Settings then offers to apply it to earlier days from a date you pick, and every day has a **current profile** switch, on its Summary and Full Day pages and under its date on Meals & Log, to score it against your profile as it is now, or put back the profile it was pinned to. [learn more...](#day-profile)

<!--
```
Before: a day was pinned to a profile snapshot on its first meal and never
moved, so a Settings change (e.g. IOM -> EFSA water) had no visible effect,
even on today; the Change control was hidden with only one profile.
db.py: day_profile gains original_name/original_json/original_overridden and
follows_current; day_profile_set_snapshot (UPDATE, not REPLACE),
day_profile_set_following (keeps the first original via COALESCE),
day_profile_restore_original. day_profile.py: follow_current, restore_pinned,
refresh_after_profile_save (today unless overridden + all following days),
follow_current_between (skips overridden). web/backend.py: _after_profile_save()
after every save_profile (Settings profile, nutrient target, load defaults),
refreshing day_pct_goal; POST /settings/profile/apply-to-days; POST
/day/<date>/profile-mode. _day_profile_switch.html macro on summary.html,
meal_day.html (profile line now a div, since a form can't sit in a p) and
meals.html.
```
-->

**PROGRAM: A WEIGHT-BASED WATER FIGURE, AND A HIGH-PROTEIN REMINDER, ON DAY PAGES**

Under a day's Water rows, NuMa now shows what NICE's hospital fluid figure, 25–30 mL per kg a day, comes to at your weight, for comparison only, with a note when it falls below your goal. On a day when your protein is one and a half times your goal or more, a second note reminds you that extra protein takes extra water to clear. [learn more...](#water-weight)

<!--
```
Day pages (/summary/<date>, the full-day meal view). profile.nice_water_band()
+ ideal_body_weight_kg() (Devine; used when BMI >= 30; each end capped at
3 L, NICE CG174); web/backend.py _water_day_notes() -> water_notes, rendered
by _water_notes.html after the nutrient section holding Water
(section["has_water"]). Protein note at _HIGH_PROTEIN_FACTOR (1.5) x the
protein goal. Both off with water tracking off, no profile, or a fluid limit.
From the fluid-intake research report's Recommendations, item 2 and 5.
```
-->

**PROGRAM: A FLUID LIMIT CAN BE SET ON DRINKS**

Settings → Nutrient Targets now takes a maximum limit for Water from drinks, as well as for Water, since a heart-failure fluid limit usually counts only what you drink. With either set, the water goals lose their color and the over-65 drinks warning and water notes go. [learn more...](#water-reference)

<!--
```
water_drinks_g added to _NUTRIENT_TARGET_GROUPS. _water_capped(max_limits)
clears rda_css/day_rda_css on the water_g and water_drinks_g rows in
_nutrient_sections() and Recent Days' % goal cells, and skips the
drinks_floor label.
```
-->

**PROGRAM: WATER PAST ITS GOAL IS NO LONGER SHOWN AS SUCCESS**

A water goal's percentage is colored as usual below the goal, but plain at or above it, never green: going past a water goal gains nothing. [learn more...](#water-reference)

<!--
```
compute_rda() types water_g and water_drinks_g "goal" (new). rda_status():
"goal" below 100% as a minimum, at/above it "reached" -> .rda-reached (bold,
no color); legend gains a "plain" entry; _RDA_TYPE_ABBR/TITLE "goal";
What-if's days-unmet count treats "reached" as met.
```
-->

**PROGRAM: CHOOSE IOM OR EFSA WATER GOALS**

Settings → 1, Your Profile, has a new **Water goals from** choice: the US Institute of Medicine's figures (3.7 L men, 2.7 L women, the default) or EFSA's (2.5 and 2.0 L). The drinks goal follows the choice. [learn more...](#water-reference)

<!--
```
UserProfile.water_reference ("iom" | "efsa", WATER_REFERENCES); stored in the
profile so pinned day snapshots keep their goals. EFSA drinks = 80% of total
(2.0 / 1.6 L), EFSA's own food-share assumption. The select shows only while
water tracking is on; settings_post keeps the saved value when it's absent.
```
-->

**PROGRAM: EACH MEAL'S SHARE OF THE DAY'S GOAL, ON MEALS & LOG**

On Meals & Log, Calories now sits after "% of goal", and it and every nutrient column after it show, under each meal's figure, that meal's share of the day's goal for the nutrient — "(23%)" — so you can see at a glance how much of a day's need a meal covers. [learn more...](#meal-columns)

<!--
```
web/backend.py _meals_list_ctx(): per date, the pinned profile's compute_rda()
(day_profile.get_profile_for_date + _load_rda); m["nutrient_pcts"][key] =
meal snapshot value / that date's goal value x 100, only where the goal is > 0.
web/templates/meals.html renders it as muted small text under the raw figure,
uncolored (a single meal against a whole day's goal would otherwise read as
"low" almost everywhere). The fixed Calories column moved from before Meal DCP
to after % of goal, with m["calories_pct"] against the date's calorie goal.
```
-->

**PROGRAM: A BUTTON TO REACH THE FOODS USDA CAN'T FILL IN WATER FOR**

Foods → 9's water section now has a **Show these foods in the list below** button. It turns on the Water column in the missing nutrient data list and takes you there, so you can ask Claude AI for those foods' water or mark them not needed. [learn more...](#water)

<!--
```
web/templates/food_cache_db_check.html, water section. A GET form re-sends the
currently remembered "Groups to check" plus water (saved to prefs the usual
way) and lands on #completeness; once water is already checked it becomes a
plain jump link. Before, the only pointer was a small-text "tick Water under
Groups to check" note, and Water is off by default.
```
-->

**PROGRAM: MARK A WHOLE COLUMN NOT NEEDED, AND REFRESH THE LIST**

In Foods → 9's missing nutrient data list, each group's heading now has a **Mark column not needed** button that ticks "not needed" for every food in that column at once, and a **Refresh list** button redraws the list without leaving the page. [learn more...](#data-completeness)

<!--
```
web/templates/food_cache_db_check.html, Missing nutrient data table. Column
button (.js-col-not-needed, data-group) toggles the column's .gap-ignore-cb
boxes and relabels itself "Unmark column" once all are ticked; nothing saved
until Save. Refresh list submits an empty GET form (a same-URL #completeness
link would only scroll, not reload); groups/show_ignored come back from prefs.
confirmGapRefresh() asks first if any not-needed box differs from defaultChecked.
```
-->

**PROGRAM: DELETING A RECIPE WARNS WHEN MEALS OR RECIPES USE IT**

Before you delete a recipe, NuMa now tells you how many logged meals it's in (and between which dates) and which recipes use it as a sub-recipe, and suggests Archive instead, which breaks nothing. This happens on both Delete buttons, the Recipes list's and the recipe page's. [learn more...](#delete-recipe-elsewhere)

<!--
```
Recipes list (Delete) and recipe page (Delete recipe). Before: the recipe page
warned only about sub-recipe use, never meals; the Recipes list's button said
just "Delete X?" (and its &#39; escaping broke the confirm() for any name with
an apostrophe). Now both use web/backend.py _recipe_delete_warning(), fed by new
db.recipe_meal_use() (meal count + first/last date, per recipe or all at once)
and db.recipe_subrecipe_users() (whole-list sub-recipe users); the text goes
through |tojson inside a single-quoted onsubmit attribute. Test:
test_recipe_delete_warns_about_meals_and_sub_recipe_use.
```
-->

**MANUAL: WATER GOAL EXPLAINED, AND WHAT COUNTS AS WATER**

The water section now explains what its daily goal is: the typical intake of healthy people, not a measured need, with Europe's lower figures for comparison. It also says that coffee, tea and dilute alcohol count as water, and why eating a lot of protein is a reason not to run low on drinks. [learn more...](#water)

**PROGRAM: A SECOND GOAL, FOR WATER FROM DRINKS, A WARNING FROM 65, AND FOOD'S SHARE OF YOUR WATER**

Your total water, from drinks and food together, is still measured against its daily goal (3.7 liters for men, 2.7 for women). The drinks part of it now has a goal of its own as well (3.0 and 2.2 liters), both from the US Institute of Medicine. From age 65, a day's page also warns when its drinks come to less than the minimum the European clinical nutrition guideline recommends for older people (2.0 liters for men, 1.6 for women). That minimum is a floor, not a lower goal: older people's need for water doesn't fall. A new manual section explains why, with sources. Water from food now shows what share of the day's water it supplied. [learn more...](#water-older)

<!--

```
Scope: profile.compute_rda() always adds water_drinks_g (minimum) = IOM beverage part of the total-water AI (3000 male / 2200 female / 2600 other). New profile.drinks_floor(profile): ESPEN geriatric minimum (2000 / 1600 / 1800; Volkert et al. 2019) at age >= 65, else None. _nutrient_sections(drinks_floor=) appends a "below the N L ... (ESPEN)" warning to the Water from drinks label when the value is under it; passed only on whole-day pages (_meal_day_context, summary_date), from the day's pinned profile (or the active one), and only while water tracking is on. An earlier same-day version offered ESPEN as an alternative goal in Settings → 9; replaced by the floor before release (owner: older people need more protein, so they shouldn't get a lower water goal). _nutrient_sections() also appends "(N% of the total)" to the Water from food label. New manual subsection #water-older with footnotes 77-83.
```

-->

**PROGRAM: WET FOOD PICKED FOR A DRY ONE IS NOW FLAGGED**

When a food's name, or the name you gave it in a recipe or meal, says it's dry (a flour, powder, dried...) but its data says it's over 40% water, NuMa now marks it in the recipe's ingredient list and the meal's food list, and lists it on Foods → 9 with where it's used. Most likely the wet version was picked by mistake, and every value from it is several times too low. Every other food in those lists shows its water in gray, and food search now labels USDA's okara as the wet pulp. [learn more...](#water-wet-dry)

<!--

```
Scope: numa_app/services/water.py dry_word() / wet_dry_conflict() (dry words flour|powder|powdered|dried|dehydrated|freeze-dried|dry; wet-context words prepared|reconstituted|cooked|packed in|in oil|wine|... void them; WET_DRY_THRESHOLD_G 40, above dried fruit at ~31%); data_quality.wet_dry_in_use() (own name or recipe-ingredient / meal-item typed name, with where used); web/backend.py _mark_water() on recipe detail + edit ingredients and meal items (sets water_pct, wet_dry; a recipe ingredient's recipe_id is its parent, so only ref_recipe_id marks a sub-recipe); new _water_mark.html mark()/footnote(); Foods → 9 #wet-dry table. usda_api okara alias label "Okara (wet pulp, as pressed — about 82% water)" (deliberately no dry word, or the check would flag it), and search_foods() now applies an alias label to USDA's own matching result too. Checked against a copy of the owner's DB with water filled in: 28 dry-named foods, 0 flagged (highest 30.9%).
```

-->

**PROGRAM: WATER TRACKING CAN BE TURNED OFF**

Settings → 9 has a **Track my water intake** switch. Turned off, it hides every water row, the drink tick-boxes, the water fill-in and the wet/dry check; nothing is deleted, so turning it back on brings everything back. [learn more...](#settings)

<!--

```
Scope: web/backend.py _track_water() (prefs track_water, default True; Jinja global), _hidden_nutrients(), _shown_groups() applied to _nutrient_sections, Top Contributors options, Compare groups, Computed Daily Targets, Nutrient Targets rows, Meals & Log column picker, Nutrient Plot choices, What-if groups (whatif._row_keys never puts water keys in "Other"); POST /settings/water; templates settings.html (#water-tracking, access key w), _drink_toggle.html, analysis_food_use.html Drink column, food_cache_db_check.html backfill + wet/dry blocks. Water is still summed into meal snapshots while off, so switching back needs no recompute.
```

-->

**PROGRAM: OKARA SEARCH RESULT HELD CELERY DATA**

Searching for okara now offers USDA's own okara (SR Legacy, with amino acids). Before this fix, NuMa's built-in "Okara" result pointed to USDA's raw celery, so choosing it saved celery's nutrients. Your database had no such entry, so nothing needs correcting.

<!--

```
Scope: usda_api.py _SEARCH_ALIASES — okara alias fdc_id 2346405 ("Celery, raw", Foundation) -> 172452 ("Okara", SR Legacy; full AA profile, water 81.6 g). All five aliases checked against the live API 2026-10-11; the other four were right. New tests/test_usda.py TestSearchAliases pins each alias id to USDA's own description. Found while testing the water backfill's batch request.
```

-->

**PROGRAM: FILL IN WATER FOR ALL YOUR USDA FOODS AT ONCE**

Foods → 9, *Missing nutrient data*, now has a **Fill in water for N USDA foods from USDA** button. It fetches just the water value for every USDA food that lacks one, adds it only where the food has none, and changes nothing else about the food; meals and recipes using those foods update to match. If it stops partway, clicking it again carries on. [learn more...](#water)

<!--

```
Scope: new numa_app/services/water_backfill.py (candidates(), run(), start() on a background thread, status()/clear_status(); per-batch recipe recompute once per recipe + stale meals + meal_recalc_log), usda_api.get_water_values() (GET foods?fdcIds=..&format=abridged&nutrients=255, 20 ids per request), db.fill_source_nutrient() (blank-only write into nutrients_json and source_json, so not a user edit), POST /food/cache/water-backfill, food_cache_db_check.html progress/outcome block (#water-backfill, 3 s reload while running). Foods marked "Water not needed" skipped. A USDAError stops the run but keeps earlier batches; rerun resumes. Tests: tests/test_water.py TestBackfill.
```

-->

**PROGRAM: WATER INTAKE, FROM DRINKS AND FROM FOOD**

Meal, recipe and day pages now show how much water you took in, split into water from drinks and water from food, measured against a daily goal for total water (3.7 L men, 2.7 L women). Tick **This food is a drink** or **This recipe is a drink** on a food's or recipe's page, or on Analysis → Food use in meals; USDA beverages are ticked for you. Both halves can be chosen as columns and plotted. Foods saved before today have no water value until refreshed. [learn more...](#water)

<!--

```
Scope: usda_api.py (NUTRIENT_MAP 1051 water_g, abridged "255", _food_category(), DERIVED_NUTRIENTS), usda_nutrients.py (nutrient_label, COMPARE_GROUPS), cnf_api.py (H2O), profile.py (compute_rda water_g AI), db.py (foods.is_drink / recipes.is_drink migration with "Beverages, ..." name backfill; cache_food(category=) guesses on insert only; set_food_is_drink / set_recipe_is_drink), new numa_app/services/water.py (tag(), as_drink(), is_drink(), looks_like_drink()), recipe_nutrients.expand_recipe_ingredients (leaf tagging, recipe drink flag carried down as _drink), web/backend.py (_meal_expand_for_diaas tagging, Water group + subtype rows shown only when the split is present, POST /food/{id}/drink and /recipe/{id}/drink with local next, Food use in meals Drink column), whatif._Ctx.nutrients_100g, meal_list_columns (split keys as column/plot choices), data_completeness ("water" group, not checked by default), claude_fetch prompt key list, templates _drink_toggle.html / food_detail / recipe_detail / analysis_food_use. The split is never stored on a food: tag() adds water_drinks_g / water_food_g at the three points food nutrients enter a total, so meal snapshots, day totals, plots and What-if carry it unchanged. Not done: CoFID/AFCD/CIQUAL moisture columns (build scripts need the source spreadsheets), a quick "+ glass of water" button. Tests: tests/test_water.py.
```

-->

#### October 10 updates

**PROGRAM: PROTEIN QUALITY TABLE SHOWS SCORES AFTER DIGESTION**

A food's Protein Quality table now has two score columns: each amino acid in the food itself, and after digestion. Its Met / Short status follows the after-digestion column, the one that decides whether the protein is complete. So a food the page calls incomplete no longer shows every amino acid as met. When every amino acid is met in the food but the protein is still incomplete (buckwheat, for one), a note explains why. The figure that used to be labeled DIAAS is now correctly called digestibility, and the real DIAAS is shown beside it. [learn more...](#protein-quality)

<!-- 

```
Scope: food page Protein Summary + Protein Quality, and the food print view.
web/backend.py _protein_section: aa_rows gain dig_score (score x TID) and
"met" now follows it (as pc["complete"] already did); "diaas" was the TID
itself -- now "digestibility" = TID and "diaas" = min raw score x TID (the
real DIAAS; bar + color follow it); new limiting_dig_score,
digestion_limited (incomplete but every raw score >= 1.0),
short_after_digestion, digestibility_pct. DCP formula unchanged. Templates:
food_detail.html, print.html, new _protein_quality_note.html. Found on
USDA 170686 buckwheat: raw Leucine 1.028 / Lysine 1.060 all "Met", verdict
Incomplete at TID 0.79 (0.812 / 0.838 after digestion).
```

-->

**PROGRAM: COMPLEMENT "% INCREASE" MEASURED FROM THE REAL STARTING DCP**

Each complement suggestion's "% increase" now measures from your meal's (or day's, or recipe's) actual current DCP, and the line under the table says what that starting figure is. Small amounts no longer show a misleading negative increase. When a food is held to its per-meal limit, its last row and summary lines say "per-meal limit" rather than "full". [learn more...](#tier-1-gap-closers)

<!--

```
Scope: every Protein Complement Suggestions section. complements.py: new
base_dcp(ingredients) (diaas.meal_level_diaas on the base's own ingredients)
is build_complement_display's base_digestible; without ingredients,
protein x min(1, limiting score). It was protein x digestibility, which
ignores the limiting AA: meal 182 at TID 0.84 / Lysine 0.69 -> 76.8 g vs a
real 63.7 g, so 10 g soy (74.2 g) showed -3.3% instead of +16%. Feeds
pct_increase (gap-closer and booster rows), the two-step dcp_before/net_gain,
and the no-new_scores fallbacks. _fmt_pair's estimate now matches _total_dig
(protein x pooled limiting score, not x new/old ratio). Result carries
base_dcp; the "% increase" explanation line names it. "(full)" -> "(per-meal
limit)" and "at full serving" -> "at the per-meal limit" when capped.
```

-->

**PROGRAM: COMPLEMENT RANKING MATCHES THE NUMBERS SHOWN**

When complement suggestions are sorted by DCP achieved, the order now follows exactly the "total digestible complete protein" figure each option shows, so a higher number is never listed below a lower one. A note under the list explains how that figure is worked out. On single-food pages that figure is also corrected: it no longer counts all the protein as complete whenever an option helps at all. [learn more...](#tier-1-gap-closers)

<!--

```
Scope: every Protein Complement Suggestions section. complements.py:
_achieved_dcp() (memoized exact_dcp at the shown amount, else _total_dig) is
now both the "dcp" sort key and _fmt's total_dig; the sort used the
_total_dig estimate while the page showed exact_dcp (meal 182: soy 105.8 g
ranked below Tiger Soup 0607 at 102.8 g). _total_dig's estimate was
(protein) x min(1, new_limiting / old_limiting), which is 1.0 for any
improvement; now (protein) x min(1, new_limiting), matching _dcp_at_frac and
the README formula. New dcp_note footer before exhausted_msg in all six
templates; ranking note names the figure.
```

-->

**PROGRAM: COMPLEMENT SUGGESTIONS STAY WITHIN A SENSIBLE AMOUNT PER MEAL**

Protein complement suggestions no longer tell you to add impossible amounts, like four cups of nutritional yeast. Each food now has a most-per-meal amount: your own, if you save one right there under the suggestion, or else a sensible default for that kind of food. When closing a gap would take more, the suggestion shows what the limit gets you and how much full closure would take. You can lift the limit for that page only. [learn more...](#tier-1-gap-closers)

<!--

```
Scope: every Protein Complement Suggestions section; the food, meal and recipe
pages get the save-limit box and the one-time checkbox (they have the
#complements-form), day/summary/recipe-portion pages show the capped note only.
usda_nutrients.complement_meal_limit (user > 3x label serving / 2x recipe
serving > type default > 300 g), _score_one_complement(max_grams) -> capped
result at the limit with closing_grams, suggest_complements(uncap_names),
improver steps capped, pair legs must close within limits; gaps still tried
most-limiting first so a capped partial on the main gap wins over a token
amount closing a minor one. db: food_annotations.max_meal_g,
food_meal_limits() (tolerates a missing column, since the candidate builders'
catch-all would otherwise drop the whole pantry), set_food_meal_limit().
POST /complement-limit (button formaction inside the GET form; field
limit_g_<fdc_id>). New _complement_limit.html; complements.label_serving_g.
Not a user edit: has_user_annotation ignores max_meal_g.
```

-->

**PROGRAM: COMPLEMENT AMOUNTS COUNT EACH FOOD AT ITS OWN DIGESTIBILITY**

Protein complement suggestions now work out how much of a food to add by counting your meal and the added food each at its own digestibility. Well-digested foods like soy protein isolate now get a realistic amount for closing the main gap, rather than being sized against a different gap. When a suggestion's amount is for a gap other than the main one, it now says so. [learn more...](#tier-1-gap-closers)

<!--

```
Scope: every Protein Complement Suggestions section (food, recipe, meal, day,
daily summary, recipe-portion analysis). usda_nutrients._score_one_complement,
_build_pairs; numa_app/services/complements.py (two_step_combo, _fmt);
new web/templates/_complement_target_note.html.

Found on meal 182: soy isolate showed 106 g "full" with Lysine left at 0.87.
Root cause: the grams solve assumed the whole pool, candidate included, was at
the base's digestibility (R = ref / base_dig), so soy (TID 0.95) against a
meal at 0.84 "needed" 621 g for Lysine (> 300 g cap), was rejected for
Isoleucine by the reduction guard, and fell through to the Leucine gap. Fixes:
(1) solve (D_base + alpha*X*tid) / (P + beta*X) = ref per source; new_scores
are pooled scores / base_dig so callers' "x digestibility" rescale still holds;
uniform math kept when base_dig is the 1.0 no-data default. (2) The reduction
guard compared the new pooled DIAAS against the base's digestibility (0.84);
now against the base's own pooled DIAAS (0.69). (3) Result carries target_aa;
the page names the gap when it isn't the primary. Pairs: post-A pool is now
per-source too, and A is skipped only when it leaves no gaps (was: "opens no
new gap", which mis-skipped an A that leaves an original gap). Two-step step 2
also draws from the sub-call's gap-closers, since strong boosters now land
there. Meal 182: soy 165 g closes Lysine, yeast 181 g (was 256 g).
```

-->

**MANUAL: WHEN TO EAT PROTEIN**

A new section, Part 4, Z, sets out what research says about *when* to eat protein: why the daily total comes first, why spreading it across meals helps, what matters around resistance and endurance exercise (and why the "anabolic window" is wider than once thought), protein before sleep, and the emerging case for protein at breakfast — each point with its source and its limits. Day pages' protein-per-meal note links to it. [learn more...](#protein-timing)

**PROGRAM: PROTEIN PER MEAL**

A meal's page now says, under Protein Summary, whether the meal carries the per-meal protein amount research associates with keeping and building muscle — 0.25–0.4 g per kg of your weight, or 25–30 g if you're 65 or over — judged on digestible complete protein, with its leucine alongside. A day's pages list each meal and how many reached it. A big meal is never flagged as too much. [learn more...](#protein-per-meal)

<!--

```
Scope: meal page Protein Summary; day view and Daily Summary date page
(Protein Quality - Full Day). New numa_app/services/protein_per_meal.py
(per_meal_amount, meal_check); _protein_per_meal.html (meal_line,
day_table); backend _protein_per_meal_day() from stored bcp_g + nutrients
snapshot. Manual #protein-per-meal (Part 4, F) with footnotes [^65]-[^68]
(ISSN 2017, Schoenfeld & Aragon 2018, PROT-AGE 2013, Trommelen 2023);
glossary PROT-AGE. Tests: tests/test_protein_per_meal.py.
```

-->

**MANUAL: FAO REFERENCE VALUES, PART 9 TIDIED, CITATION CHECKLIST**

The nine FAO 2013 amino acid reference values every protein score in NuMa is measured against now have their own table, with how to read it, in Part 4, J. Part 9's finished items moved to its "implemented" list, its stale entries were updated, and its source-citation item is now a checklist of which areas are sourced, which still need sources, and which are NuMa's own design choices. DIAAS, complete protein and glycemic load gained citations. [learn more...](#citations-progress)

**PROGRAM: HELP CHOOSING A DAILY GLYCEMIC LOAD TARGET**

Under the daily glycemic load target box in Settings → Your Profile, **Help me choose a target** offers three starting points, each filled in with one click: 80 per 2,000 kcal scaled to your own calorie target (recommended), the commonly quoted 80, or 10–20% below your own average over the last 30 days. The manual explains who each suits, its limits, and its sources — and that no guideline sets an official number. [learn more...](#gl-target-choose)

<!--

```
Scope: Settings -> 1 (#gl-target-help details panel, js-gl-target-pick
buttons fill #gl_day_target). glycemic_load.gl_target_options(calories,
recent_avg, recent_days) + constants GL_MODERATE_PER_2000_KCAL,
GL_CONVENTIONAL_DAY_TARGET, GL_STEP_DOWN, GL_STEP_DOWN_MIN_DAYS (7).
settings_get: calories from compute_rda, recent average from
average_day_gl(day_gl_totals(last 30 days' meal dates)). Manual
#gl-target-choose with footnotes [^61]-[^64] (Barclay 2021 GI Foundation;
ASA 2025; Livesey et al. 2019 Nutrients; AND summary of ADA/NICE/Diabetes
Canada positions). Tests: TestGlTargetOptions, settings page test.
```

-->

**PROGRAM: GI NOTES TAILORED TO YOUR GLUCOSE TOLERANCE**

The note NuMa shows beside a GI value measured in people with diabetes now follows **Your glucose tolerance** in Settings → Your Profile (the setting formerly labeled "Glycemic index lookup default"). Set to impaired, it says the value fits you; set to normal, it says to treat it as an approximation and prefer a normal-tolerance value; not set, it gives both readings and a link to set it. [learn more...](#gi-impaired)

<!--

```
Scope: _gl_result.html gi_impaired_advice(links, plural) — the one place the
advice is worded; used by gi_population_note, _top_contributors gi_dagger_note,
compare footnote, food_detail, food_annotate. Jinja global
user_glucose_tolerance() (web/backend.py, active profile). Settings label and
help text reworded. Test: test_impaired_value_note_is_tailored_to_profile.
```

-->

**PROGRAM: OPTIONAL DAILY GLYCEMIC LOAD TARGET**

Settings → Your Profile has a new **Daily glycemic load target**. Set one and every day's glycemic load is checked against it: on the day's pages, colored in Recent Days' Day GL column, as "days over" in Nutrient averages across days, and in What-if: Meals as days over it before and after your changes — so an average under the target can't hide days that aren't. A day missing some GI values is called over only when it already is; otherwise NuMa says it can't tell yet. [learn more...](#gl-target)

**PROGRAM: SAVING YOUR PROFILE KEEPS ITS NAME**

Saving Settings → Your Profile now saves to the profile you're using. Before, a profile with any name other than "Default" had its changes written to a separate "Default" profile instead, so they seemed not to stick.

<!--

```
Scope: Settings -> 1 (profile.UserProfile.gl_day_target, _positive_or_none;
settings_post also passes name=existing.name — previously defaulted to
"Default", writing a second file when the active profile had another name).
glycemic_load.gl_target_status() (rda_status "limit"; "unknown" when an
incomplete day is still under). Day contexts (meal day, summary date, day
print) -> gl_target, _gl_result.html gl_target_line via gl_figure(target=).
Recent Days row day_gl_target (pinned profile per day). Trend: gl_days_over /
gl_target_days. whatif._gl_cell(targets=) -> days_over_target_before/after,
target_unknown_*. Speed check 2026-10-10 on a copy of the real DB: 90 days
(87 meals) 0.74 s total, GL cell 0.04 s; DB checksum unchanged. GI-USE-PLAN
item 7, step 5; WHATIF-PLAN Phase 5 complete.
```

-->

**MANUAL: WHAT YOU CAN DO WITH GI AND GL; WHAT "IMPAIRED GLUCOSE TOLERANCE" MEANS**

Two new sections. "What you can do with GI and GL" walks through using glycemic load — read it, see which foods drive it, change one, check the whole picture in What-if — with a worked example: 200 g of white rice versus pearled barley. "What 'impaired glucose tolerance' means here" explains that NuMa's label covers people with type 2 or type 1 diabetes, gestational diabetes and pre-diabetes, and how to use such a value if you don't have diabetes. Every place NuMa marks such a value now links to it. [learn more...](#gi-impaired)

**PROGRAM: GLYCEMIC LOAD IN COMPARE AND RECENT DAYS, AND HOW TO READ A BAND**

Compare has a new glycemic table: each food's GI and each item's glycemic load per 100 g, the lowest highlighted. Recent Days has a **Day GL** column with its band, and a link to plot it over time. Under every glycemic load band, one line now says which scale it's on and links to what you can do with it. [learn more...](#gl-uses)

<!--

```
Scope: Compare (_build_gl_compare_rows; entries carry gi, gi_impaired, gl via
food_gl / gl_for_leaves over expand_recipe_ingredients scaled to 100 g);
Recent Days (_build_day_rows -> day_gl via new glycemic_load.day_gl();
show_gl_col = not gi opt-out); _gl_result.html gl_band_help(scope) called in
gl_figure, food_detail, trend - replaces the separate gl_band_caveat lines on
meal_day, summary, print, trend. Impaired-mark links -> #gi-impaired on food,
Annotate (also beside the lookup's population chooser), GL figure,
Top Contributors/swaps, Compare. GI-USE-PLAN items 1-3, 6, 8.
```

-->

**PROGRAM: GI VALUES MEASURED IN PEOPLE WITH DIABETES ARE MARKED**

When a food's GI was picked from a reference-table row measured in people with impaired glucose tolerance or diabetes, NuMa now says so wherever that value is used: on the food's page and its Annotate page, with a † in Top Contributors ranked by glycemic load and in lower-GI swap suggestions, and in a line under any meal's, recipe's or day's glycemic load naming those foods. That's the right value if it describes you; if not, your own response may differ. [learn more...](#gi-populations)

<!--

```
Scope: food page, Annotate page, every GL figure (_gl_result.html), GL Top
Contributors and swap suggestions. glycemic_load.gi_measured_impaired(src)
looks for the "Impaired glucose tolerance" label the lookup JS writes into
gi_source; _food_share() tallies counted foods (>= 1 g carbs) into result
"impaired" (combine_gl merges, de-duplicated); accumulators now a dict
(_new_acc). rank_contributors_by_gl and gl_swaps items carry "impaired";
db.foods_with_gi() returns gi_source. Jinja filter gi_impaired. Annotate
JS toggles #gi-pop-note on pick. GI-USE-PLAN item 11. Tests:
TestImpairedPopulation (test_glycemic_load.py), test_gl_swaps.py.
```

-->

**PROGRAM: FOODS YOU USE WITH NO GI, AND WHERE SWAP SUGGESTIONS COME FROM**

Foods → 9 has a new folded-up list, **Foods you use with no GI**: foods in your recipes, meals or pantry with carbohydrate but no glycemic index, most-used first, each with a **look up a GI** link and a **not needed** box. Lower-GI swap suggestions now say they come only from the foods you've given a GI, and how many foods you use still have none, with a link to that list. [learn more...](#missing-gi)

<!--

```
Scope: Foods -> 9 (#missing-gi); meal/recipe Top Contributors ranked by GL.
data_quality.missing_gi_in_use() (carbs >= GI_LIST_MIN_CARBS = 5 g/100 g,
no gi_estimate; ignored = gi_no_prompt). Completeness save route: group "gi"
-> db.upsert_food_annotation(gi_no_prompt=0/1); back anchor "missing-gi".
List hidden when GI opted out. _build_contributors adds gl_pool_n
(db.foods_with_gi) and gl_missing_in_use_n for Medium/High GL;
_top_contributors.html gl_pool_note() under shown swaps and in the
no-suggestion message. Tests in tests/test_gl_swaps.py.
```

-->

**PROGRAM: SEE WHICH FOODS DRIVE GLYCEMIC LOAD, AND LOWER-GI SWAPS TO TRY**

On a meal or recipe page, Top Contributors can now rank the foods by glycemic load, showing each food's GI and amount; the rows add up to the meal's or recipe's glycemic load, and foods with no GI are named with a link to add one. When the load is Medium or High, NuMa suggests lower-GI foods from your Food Cache with similar carbohydrate, each with a link that opens What-if with the swap filled in, so you can see every nutrient's change first. A new link under each Glycemic Load figure takes you straight there. [learn more...](#gl-swaps)

<!--

```
Scope: meal and recipe pages -> Top Contributors (rank=gl); GL section link.
top_contributors.rank_contributors_by_gl(): leaf foods by GI x carbs/100,
merged per food, with gi/grams/carbs_100g, no-GI gaps and coverage. New
numa_app/services/gl_swaps.py suggest_swaps(): pool = db.foods_with_gi()
(non-archived); GI >= 5 lower, carbs/100 g within 1.5x, GL saving >= 0.5,
shared name words first. backend: _GL_RANK_KEY option after carbs_g,
_build_contributors(gl_scope=...) adds gl_gaps/gl_coverage/gl_band/gl_swaps
(swaps only for Medium/High), _gl_swap_whatif_url() (meal ids / last 30
days / recipe ids). Recipe page ranks GL over calorie_leaves (sub-recipes
opened). _top_contributors.html gl_contributor_notes(). GI-USE-PLAN step 2.
Tests: tests/test_gl_swaps.py.
```

-->

**PROGRAM: GLYCEMIC LOAD IN WHAT-IF, AND HOW MUCH A GL FIGURE COVERS**

What-if: Meals now shows your average daily glycemic load before and after your changes, with its band (Low, Moderate, High); What-if: Recipes shows glycemic load per serving for each recipe. When some carbohydrate comes from foods with no GI, NuMa says how much of it the figure covers, before and after, and names the foods with no GI so you can add one — otherwise swapping in such a food would look like an improvement. Every incomplete GL figure elsewhere (meal, recipe, day pages) now gets the same coverage line. [learn more...](#whatif-gl)

<!--

```
Scope: Analysis -> What-if: meals / recipes; every incomplete GL figure.
glycemic_load.py: _food_share() tallies carbohydrate with a GI vs carbohydrate
that counts (negligible and "don't prompt" excluded); _result() adds
carbs_with_gi_g, carbs_g, coverage_pct; combine_gl() sums them; new
gl_for_leaves() computes GL from already-expanded leaf foods, so what-if's
edits reach GL without a second expansion path. whatif.py: "gl" summary cell
(_gl_cell: average day GL over days with carbs, day bands, coverage before/
after, no-GI gaps after); recipes get a per-serving GL row at the end of the
carbohydrate section (_recipe_gl_row). gi_opt_out passed from backend.
_gl_result.html gl_coverage() macro. WHATIF-PLAN Phase 5 first item; GI-USE-PLAN
step 1. Tests: TestGlycemicLoad + page test in test_whatif.py, coverage and
gl_for_leaves tests in test_glycemic_load.py.
```

-->

**PROGRAM: TURN OFF THE MISSING-AMINO-ACID AND CALORIE WARNINGS FROM WHERE THEY APPEAR**

Beside each food in a meal's or recipe's **Missing Amino Acid Profiles** section there is now an **Amino acids not needed for this food — stop listing it** button, for a food whose protein doesn't matter, such as a supplement. The food stops being listed there and on Foods → 9, and a short line counts foods hidden this way. That section and the **Calories** note above the Nutritional Analysis table both link to the manual's instructions for turning their check off. [learn more...](#missing-aa-off)

<!--

```
Scope: meal and recipe pages -> Missing Amino Acid Profiles; Calories note.
web/backend.py _build_diaas_display(): drops missing-AA names whose food has
the "aa" group in food_data_ignores; adds missing_fdc_ids and
missing_aa_not_needed. POST /food/{fdc_id}/data-ignore takes an optional
local-path `next` (rejects // and backslashes) to return to the meal/recipe.
New partial web/templates/_aa_not_needed.html (button, footer, manual link);
_calorie_note.html links to new anchor #calorie-check-off. Manual anchors
#missing-aa-off, #calorie-check-off. Test:
test_missing_aa_not_needed_button_hides_food.
```

-->

#### Release v2026-10-09-1637 summary (dated details below)

- **21.** USDA foods now keep the zeros USDA measured (earlier versions dropped them); 17 starter foods are updated to match.
- **20.** Nutrient tables list every nutrient: "0" where the source measured none, "no data" where nothing was recorded; small amounts keep their decimals.
- **19.** When NuMa is updated while it's running, every page says so, with a **Restart NuMa now** button, instead of failing with an error.
- **18.** Food and recipe names in complement suggestions and DIAAS boosters are now links to their pages.
- **17.** MANUAL: Part 1 A now lists every file NuMa puts on your computer, and why.
- **16.** MANUAL: New section "Data entry: what you can type, and data errors to catch" (Part 6, J), with every accepted form and the common errors.
- **15.** Forms read what you type more forgivingly — `400 IU`, `12 mg`, `1,200`, `1½ c`, `2 eggs`, `2 tablets`, a pasted amino acid table — and anything NuMa can't read is named instead of silently dropped. Supplement mode now works.
- **14.** MANUAL: Weekly sweep and full manual audit — column guides, menu paths and portion formats brought up to date, three new Glossary entries, and the updates log trimmed to the last two weeks.
- **13.** A volume typed with its weight ("2 T 15 g") now records the weight you typed; before, the weight was ignored and an estimate used instead.
- **12.** In search results, your recipes now come first among your own matches, ahead of Pantry and Food Cache foods.
- **11.** Glycemic load now shows for every food (per 100 g and per portion), every recipe (per serving) and every meal and day — marked "incomplete, missing GI data" with the missing foods listed when some have no GI value.
- **10.** MANUAL: New quick-answer table on what each edit changes — editing recipes, the food cache, or the manual's source file.
- **9.** A meal's food search shows each food's or recipe's own note beside its "Add to meal" box.
- **8.** Compare, Convert, Edit Recipe and the "copy from another food" searches show your own matches at once while online results load; the copy-from searches now rank results and honor the result limit like every other search.
- **7.** Compare, Convert and Edit Recipe now search every source you tick, and a search result from any source opens and adds correctly.
- **6.** A red "Online search in progress…" note now shows wherever NuMa is waiting on an online search; Food Cache gains a **Search online** button.
- **5.** My Pantry's search now covers every source you tick (CNF, CoFID, AFCD and CIQUAL were being skipped), and shows your own matches at once while online results load.
- **4.** My Pantry: a new **Filter my pantry list** box narrows the pantry list itself, and search results now have Compare checkboxes.
- **3.** What-if pages: save a scenario by name, download the results as CSV, and apply a replace-only scenario to your meals or recipes for real, after a confirmation page.
- **2.** "Keep as entered" now rewrites an amount as your own weight ("2309.2 g (8 c)"), so it's never listed again; the "Kept as entered" lists are gone.
- **1.** On the Database check page (Foods → 9), any list longer than 6 entries now starts folded behind its count line; click it to show the list.

#### October 9 updates

**PROGRAM: USDA'S ZEROS ARE BACK**

Earlier versions of NuMa threw away every nutrient USDA had measured at zero, so a food with no vitamin C, say, looked the same as one never tested for it. New lookups now keep those zeros, and 17 of the [starter foods](#starter-data) are updated to include them: after updating NuMa, they're listed under **Improved in this version of NuMa** in Settings → 9, where you can take the update or keep your copy. A food you've already looked up gets its zeros back the next time you use **Refresh from USDA**. [learn more...](#nutrients)

<!--
```
Scope: new scripts/restore_usda_zeros.py (fetch each cached USDA food; add
only keys USDA reports as exactly 0 that the food lacks, to nutrients_json
and source_json; never touches an existing value; backs up the DB). Run on
the owner's DB 2026-10-09: 236 checked, 64 foods got zeros, 5 lookups failed
(4 ids USDA doesn't serve, 1 timeout), no food's user_edited changed, no
non-zero value changed. starter_data.json: 37 zero values added to 17 foods
(refresh_starter_data.py also pulled 4 unrelated live edits — Organic Diced
Tomatoes portions and 3 recipes — which were deliberately NOT included; run
the refresh yourself when you want them). Nutrients are part of
demo_data._item_hash, so prior-version users get the "improved" notice.
Tests: tests/test_restore_usda_zeros.py.
```
-->

**PROGRAM: "NO DATA" IS NOT ZERO**

Nutrient tables now show a row for every nutrient NuMa tracks. A nutrient the food's source measured at zero shows **0**; one that was never recorded shows **no data**, instead of being left out (which hid EPA, DHA and linoleic acid while showing ALA) or shown as 0. Small amounts keep their decimals, so 0.3 mg no longer reads as 0. Zeros from USDA and zeros you type on a custom food are now kept as real zeros. [learn more...](#nutrients)

<!--
```
Scope: food, recipe, recipe-portion, meal, day, Daily Summary, trend and print
nutrient tables. web/backend.py _nutrient_sections(): every key in
_NUTRIENT_GROUPS gets a row; value None + missing=True when absent;
_display_amount() (whole from 10, 1 dp from 0.1, then 2-4 dp) replaced
round(val), which showed 0.3 as 0. usda_api._parse_food(): `value or amount`
dropped measured zeros — now explicit None checks; a 0 kcal Energy row no
longer blocks the Atwater figure. Custom profile save keeps a typed 0 (was
dropped). Existing cached USDA foods still lack their zeros until
re-fetched (222 foods; one-time fill-zeros-only repair offered to owner).
Tests: TestNutrientTableNoData, test_usda_parse_keeps_measured_zeros.
```
-->

**PROGRAM: "PLEASE RESTART" INSTEAD OF AN ERROR**

When NuMa is updated while it's still running, a yellow bar at the top of every page now says so, with a **Restart NuMa now** button that restarts it behind the page and brings you back where you were. A page that would have failed with "Internal Server Error" because of the update shows the same message instead. [learn more...](#ts-crash)

<!--
```
Scope: web/backend.py — _disk_version() (version.py re-read on mtime
change; path from sys.modules["version"]), _restart_needed() (never when
frozen), _restart_needed_middleware (outermost; a crash while stale ->
503 restart page), _can_restart_in_place() (argv[0] is launcher.py, not
--reload), _schedule_restart() (Popen a fresh launcher with --no-browser,
start_new_session; the new launcher's port-in-use path stops this process;
os._exit backstop after 8 s), POST /restart-now (waiting page polls GET
/restart-status until a different VERSION answers, then location.replace),
base.html banner. Cause: 2026-10-09 the owner hit a 500 running a server
started before that day's code changes (templates are read from disk, code
isn't). Verified end to end on an isolated port. Tests: TestRestartNeeded.
```
-->

**PROGRAM: SUGGESTED FOODS AND RECIPES ARE LINKS**

In Complement Suggestions and DIAAS boosters, every food or recipe name — in a suggestion card, a two-food pair or a two-step combination — now links to that food's or recipe's own page, opened in a new tab so the analysis you're reading stays put. A generic estimate from the built-in list has no page, so it stays plain text. [learn more...](#comp)

<!--
```
Scope: food, meal, day, Daily Summary, recipe and recipe-portion analysis
pages (suggest_card macros, pairs, two_step_combos, diaas_improvers); new
Jinja global item_link() in web/backend.py (recipe_id -> /recipe/N, else
fdc_id -> /food/N, else escaped plain name). Printouts unchanged. Tests:
test_item_link_links_suggested_foods_and_recipes,
test_complement_cards_use_item_link_everywhere (no bare name left).
```
-->

**PROGRAM: NOTHING YOU TYPE IS SILENTLY DROPPED**

Forms now read the everyday ways people write values, and say so when they convert one. On a custom food: `400 IU` (vitamins A, D, E), `12 mg`, `2.4 µg`, `1046 kJ`, `1,200`, `2½`, `trace`, and a pasted amino acid table. In any amount box: `½ cup`, `1,000 g`, `2 tbsp.`, and counts of a food's own portions such as `2 eggs` or `2 tablets`. Anything NuMa can't read is named, and the form keeps everything you typed until it's fixed; before, such values vanished without a word. Supplement mode now works: a custom food with a serving of 1 tablet gets a "1 tablet" portion, so `2 tablets` logs twice the label amounts. [learn more...](#data-entry)

<!--
```
Scope: new numa_app/services/entry_parse.py (parse_number, parse_nutrient,
parse_aa_block, supplement_portion, EntryError). Edit Custom Profile: boxes
are now text inputs (type=number refused "400 IU" in the browser); the POST
reads every box through parse_nutrient, refuses the whole save on any error
with typed values kept (_custom_edit_response), notes conversions, adds the
supplement portion, takes a pasted AA table. web/backend.py
_parse_portion_str_raw: _normalize_amount_text (fraction characters,
thousands/decimal commas, unit periods and aliases), _match_count_portion
("2 eggs" -> "1 large egg"; ambiguous -> refused) and _portion_hint in the
not-recognized message. Settings -> 7 targets (parse_nutrient; error shown,
nothing saved) and a recipe's weight/volume on a meal (add_error) no longer
swallow unreadable values. Owner's earlier weight-in-amount / volume-in-note
entries (39 recipe lines) checked read-only: grams as typed, nothing wrong.
Tests: tests/test_entry_parse.py, TestParsePortionStrTolerant,
test_custom_profile_save_converts_units_and_refuses_unreadable,
test_settings_nutrient_target_reads_units_and_reports_errors.
```
-->

**MANUAL: DATA ENTRY, AND WHAT'S INSTALLED**

A new section, [Data entry: what you can type, and data errors to catch](#data-entry), lists every form NuMa accepts in amount and nutrient boxes, what it refuses and why, and the mistakes no form can catch (per-serving figures typed as per 100 g, the wrong unit, a slipped decimal point). Part 1 A has a new list, [What's on your computer, and why](#installed-files). Custom foods, supplement mode and the portion-formats appendix now describe what actually works.

<!--
```
Scope: user-manual.md Part 6 E (custom foods, supplements), new Part 6 J
(#data-entry), Part 1 A (#installed-files), Appendix E counts, Part 8
ts-no-piece-portion. Also removed export.py (unused CLI report export) and
scripts/run_numa.sh (launched the deleted numa.py); docs references updated.
README sweep item 8 now requires every non-200 link to be reported in full,
and names the fdc.nal.usda.gov food-details curl 404 as a known false alarm
(owner confirmed both Appendix F links work, 2026-10-09).
tests/test_packaging_spec.py::test_readme_test_count_matches_the_suite now
enforces the README test count, which nothing had checked.
```
-->

**MANUAL: WEEKLY SWEEP AND FULL MANUAL AUDIT**

The manual's column guides now match what each table actually shows (Codes instead of IDs, the Pantry, Recipes, Meals & Log and import tables), menu paths and cross-references are corrected, the portion-formats appendix now says how to enter counts like "2 eggs", leftover instructions from the old command-line version are gone, and the Glossary has new entries for what-if, user-edited and generic density. The updates log is trimmed to the last two weeks. [learn more...](#portion-formats)

<!--
```
Scope: user-manual.md Parts 1, 3-8, Appendix E, Glossary; README.md key
features (what-if, data checks, food-use replace); README-numa-documentation.md
monthly deep check (Project Structure: 6 modules, ~40 templates, 20 scripts;
schema table +9 tables; Data Storage rewritten; Setup now Python 3.12 +
cryptography/matplotlib/pdfminer.six/playwright; dead state.py/prefs.py,
_search_relevance_key, export.py, update-notify-frequency references fixed);
CLAUDE.md (data_quality.py, energy_check.py added; export.py marked unused);
scripts/setup_venv.sh message (python numa.py -> web/launcher.py).
New test: db-check list folding (>6 folds). Findings NOT fixed, for the
owner: custom-food supplement mode, IU entry and AA paste-block exist only
in the manual (CLI-era); count units ("2 eggs") unsupported; export.py and
scripts/run_numa.sh dead; two fdc.nal.usda.gov food-details links 404 to
curl (SPA? unverified).
```
-->

**PROGRAM: A WEIGHT TYPED WITH A VOLUME IS NOW USED**

Typing a volume with its weight, like `2 T 15 g` or `1/4 c 60`, now records the weight you typed and shows it as "15 g (2 T)". Before, NuMa ignored the weight and worked the grams out from the volume instead. Check any amount you entered this way in a recipe or meal: re-enter it to get the weight you meant. [learn more...](#portion-formats)

<!--
```
Scope: every amount box using web/backend.py _parse_portion_str_raw() (meal
add/edit, recipe ingredients, food page, analyze, convert). Found in the
2026-10-09 full manual audit: Appendix E documented "2 T 30g" -> 30 g, which
numa_app/services/portions.py handles, but the web's own parser stopped at
the volume unit, so the typed weight was dropped and density used. Worse,
data_quality treats "2 T 15 g" as a typed own weight and never lists it
under Amounts that no longer match, so the wrong grams were invisible. The
volume branch now reads a trailing number (+ weight unit) as the weight,
label "15 g (2 T)" (own_weight_text's form); anything else after the
volume is an error. Tests: TestParsePortionStrExplicitWeight.
```
-->

**PROGRAM: RECIPES FIRST IN SEARCH RESULTS**

Wherever a search can return recipes as well as foods, your recipes are now listed first among your own matches, ahead of Pantry and Food Cache foods. Online results still follow below the divider. The "Pantry, Cache, then Other" sort is now "Recipes, Pantry, Cache, then Other". [learn more...](#search-ranking)

<!--
```
Scope: every _run_food_search() screen (Food Search, a meal's Add panel,
Edit Recipe, Compare, Convert) and Food Use's substitute picker.
web/backend.py _cap_results_preserving_local() now orders the local block
recipe, then pantry/cache (each keeping relevance order); _SEARCH_CATEGORY_RANK
and search_ranking.SOURCE_RANK tie-breaks recipe 0, pantry 1, cache 2; the
substitute search sorts recipes first. Divider and sort-mode labels renamed
(search.html, meal.html, _search_api_rows.html). Manual: Part 6 C and the
Sort order note corrected -- they said local and online results could
interleave, but local results have always been grouped first.
```
-->

**PROGRAM: GLYCEMIC LOAD FOR EVERY FOOD, RECIPE AND MEAL**

Glycemic load now shows on every food's page (per 100 g, and for the portion you're analyzing), every recipe's page (per serving) and every meal and day. When some foods have carbohydrate but no GI value, the figure reads "at least 14.2 — incomplete, missing GI data", with each missing food listed and a link to add its GI. Foods marked "don't prompt me" are listed as such. Foods with under 1 g of carbohydrate in the amount used no longer need a GI at all. [learn more...](#glycemic)

<!--
```
Scope: food, recipe, recipe-portion, meal, day, Daily Summary and print pages;
numa_app/services/glycemic_load.py (rewritten core: gl_for_items, food_gl,
recipe_gl, meal_gl, combine_gl; result dict {total, complete, gaps}),
web/backend.py (_recipe_gl_web, _compute_gl, day pools, _food_detail_context
gl_100g/gl_portion, food print), new web/templates/_gl_result.html macro
replacing six copies of the GL block; food_detail.html GI/GL line; db.py
recipe_set_gl removed. Root cause: recipe items read recipes.gl_g, which
nothing in production ever wrote (only tests), so every recipe -- and every
meal or day containing one -- showed "Not available". Recipe GL is now
worked out live from ingredients through sub-recipes (cycle guard; deleted
sub-recipe = gap). A missing GI no longer hides the total: the counted part
is a lower bound, banded only when complete or already High. gi_no_prompt
(and the global GI opt-out) mark a gap "not_wanted" rather than "no_gi".
NEGLIGIBLE_CARBS_G = 1.0 in the amount eaten, mirroring DCP's 1 g protein
floor. Trends/plots still skip incomplete days (day_gl_total -> None).
```
-->

**MANUAL: WHAT AN EDIT CHANGES, AT A GLANCE**

The section on data editing now opens with a short answer and a table: for each kind of change (a food's nutrients, its portions, a recipe's ingredients or servings, a rename, a delete, a substitution, a what-if, your profile), what happens to the recipes and meals that use it. In short, nutrient changes cascade everywhere automatically; amounts you have already typed keep their grams. A new subsection explains how an edit to the manual's own source file reaches your browser. [learn more...](#editing-consequences)

<!--
```
Scope: user-manual.md Part 6 D (#editing-consequences) -- heading renamed to
"Data editing: what changes when editing recipes, meals, or the food cache"
so sidebar searches for "data editing", "editing recipes" and "editing food
cache" rank it first (title words score 3x idf in scoreOf()). Quick-answer
table synthesized from the existing D subsections, #data-effects,
#stale-amounts, #fooduse-substitute, #whatif-apply, #day-profile; cascade
claims checked against recipe_dcp.cascade_food_change/recompute_recipe_dcp
and backend _stale_meals_middleware. New #manual-source-edits subsection:
/manual and / both run manual_build.rebuild_manual_if_stale() (mtime check),
and manual_update.get_active_manual() serves a downloaded manual instead
when its stamp is newer than the baked header stamp.
```
-->

#### October 8 updates

**PROGRAM: NOTES IN A MEAL'S FOOD SEARCH**

When you search for something to add to a meal, any note you've saved on a food or recipe now shows to the right of its **Add to meal** box. Long notes show their first few lines; click the note to read all of it, and click again to fold it back.

<!--
```
Scope: Meals -> a meal -> Add food search (_add_food_row.html, meal.html,
style.css). _search_local_results() rows now carry `notes` (foods.notes;
recipes.notes, now selected by db.recipe_list()). The add-food table widens
(76rem cap instead of 46rem) only when a result has a note; the note is a
flex item beside the form that wraps below it on narrow windows, clamped to
4 lines with CSS line-clamp, toggled open on click.
```
-->

**PROGRAM: YOUR OWN MATCHES FIRST, ON EVERY SEARCH**

The searches on Compare, Convert and Edit Recipe (Add ingredient), and the "copy from another food" searches (a custom food's **Estimate amino acids** and **Copy nutrient values**, and **Fill in nutrients from another food**), now show matches from your pantry, Food Cache and recipes straight away. The online results fill in a moment later, with the red **Online search in progress…** note showing until they do; anything you type or tick meanwhile is kept. The "copy from another food" searches now also rank results by how well they match, follow your "Show up to" result limit, and include your pantry foods. The amino acid search still lists foods with amino acid data first. [learn more...](#food-search)

<!--
```
Scope: web/backend.py (_SEARCH_SCREENS, /search-rows/{screen}, _run_food_search
options exclude_fdc_id / aa_first, _picker_sources), base.html
[data-search-results] script, _search_results_block.html, new rows partials
(_compare_search_rows, _convert_search_rows, _recipe_search_rows,
_source_picker_rows; _pantry_search_rows reused), README "Searching for a
food". _search_food_sources() removed: the pickers had no ranking, no limit,
fetched USDA twice per search, and ran their online searches with a database
connection open. My Pantry moved off its own script and
/pantry/search-api-results onto the shared mechanism. Compare's entry loader
now fetches uncached foods before opening its connection (CLAUDE.md DB rule).
Rows carry data-row-key so typed amounts / ticks survive the swap; the
unsaved-changes guard is re-pointed at the new rows.
```
-->

**PROGRAM: EVERY SEARCH BOX SEARCHES EVERY SOURCE YOU TICK**

The searches on Compare, Convert and Edit Recipe (Add ingredient) now look in every source ticked in their Source list, just like Foods → Search; they had been skipping Open Food Facts, the Canadian Nutrient File, and, on Convert and Edit Recipe, CoFID, AFCD and CIQUAL too. Clicking a result's name, converting it, adding it to a recipe, or comparing it now works whichever source it came from; a result not yet in your Food Cache from one of those sources used to end at "Could not load food". [learn more...](#food-search)

<!--
```
Scope: web/backend.py search + fetch paths; README "Searching for a food".
One pipeline, _run_food_search() (local -> online -> sort -> Source filter ->
cap), now used by Foods -> Search, Analyze a Food Portion, meal add-food panel,
My Pantry, Compare, Convert and Edit Recipe; options external / foods_only /
exclude_recipe_id / clean_query. _meal_add_food_local_results() merged into
_search_local_results() (superset row shape; GI/DIAAS as strings, matching
online rows; aa_indicator everywhere, so a cached food with no nutrient data
shows the warning sign on the meal panel too). Compare/Convert/Edit Recipe
dropped their own cache+USDA loops; search_error dropped from Compare/Convert
search (per-source failures are skipped silently, as elsewhere).
Fetch-on-pick: food page (_food_detail_context), Convert detail, recipe
ingredient add and Compare "Add to food cache" use _get_or_cache_source_food();
Compare's uncached-entry loader uses _fetch_uncached_food_detail(). Open Food
Facts ids are a one-way hash of the barcode number, so it travels as off_code:
food_url() template global for result links, hidden field on Add to recipe,
off_code_<id> beside Compare checkboxes (add-multiple caches those foods).
```
-->

**PROGRAM: "ONLINE SEARCH IN PROGRESS…" WHEREVER YOU'RE WAITING ON ONE**

Whenever NuMa is searching USDA, Open Food Facts or the Canadian Nutrient File, a red **Online search in progress…** note now shows where you'll see it: next to the result count, or beside the Search button on pages that wait for the online results before showing anything. It goes away when the results arrive. Food Cache also has a **Search online** button beside **Filter this list**, which takes the same words to Foods → Search. [learn more...](#food-search)

<!--
```
Scope: all online-search screens. Async pages (Foods -> Search, Analyze a Food
Portion, meal add-food panel, My Pantry): the gray "Searching ..." row at the
bottom of the results table is replaced by a red note near the count / search
box (_online_search_notice.html macro; same element ids, so the JS gate and the
e2e "removed after fetch" checks still hold); the JS now removes it on success
and rewrites it on failure. Pages that wait server-side (Compare's add panel,
Convert, Fill in from another food, custom-food AA/nutrient source pickers,
Edit Recipe ingredient search; also Foods -> Search's barcode path): search
forms carry data-online-search, and a base.html submit listener adds the note
beside the button when the query is non-empty and a live source is ticked (or
none is). Live keys come from _LIVE_SOURCES via the live_source_keys template
global. Notes it adds are cleared on a back-button (bfcache) restore. Food
Cache: "Filter" renamed "Filter this list", plus a "Search online" button.
```
-->

**PROGRAM: MY PANTRY SEARCHES EVERY SOURCE YOU TICK, AND SHOWS YOUR OWN MATCHES AT ONCE**

My Pantry's search now looks in every source ticked in its Source list, the same as Foods → Search: Canadian Nutrient File, CoFID, AFCD and CIQUAL included, which it had been skipping. Matches from your pantry and Food Cache show straight away, and the online results fill in a few seconds later. Ticks you make in the meantime are kept. [learn more...](#pantry)

<!--
```
Scope: Foods -> My Pantry (web/backend.py, pantry.html, new
_pantry_search_rows.html). pantry_get had its own cache+USDA+OFF search that
ignored cnf and the static sources despite offering their checkboxes. Replaced
by the shared _search_local_results() and
_external_food_search_results() (recipe rows dropped: a pantry holds foods).
First render is local-only; new GET /pantry/search-api-results returns the
full merged, re-sorted, capped rows, which replace the tbody (Compare ticks
carried across), mirroring /food/search-api-results. search_error dropped:
the shared helpers swallow per-source failures, as on Foods -> Search.
Compare-button coloring now uses a delegated change listener.
```
-->

**PROGRAM: MY PANTRY CAN FILTER ITS OWN LIST, AND COMPARE SEARCH RESULTS**

My Pantry has a new **Filter my pantry list** box just above the list. Type a word or two to show only the pantry items whose name or notes contain them all. The search box at the top of the page still looks for new foods to add, and its results now have Compare checkboxes of their own. Each Compare button turns blue once two or more items are ticked. On Food Cache, a filter now also offers a **Not here? Search online** link to Foods → Search. [learn more...](#pantry)

<!--
```
Scope: Foods -> My Pantry (web/backend.py pantry_get, pantry.html). New GET param
"filter": every lower-cased word must appear in food_name + notes; applied after
the items are built, so search's in-pantry detection and the link_id lookup
still use the full list (all_items). Result count reads "N of M pantry items
matching X"; an empty filter result says so rather than "Your pantry is empty".
The Add search form carries the filter forward as a hidden field. Search
results get an external compare-search-form (rows hold their own add/remove
forms); a shared data-compare-btn script colors each button by the ticks for
its own form only.
```
-->

**PROGRAM: WHAT-IF SCENARIOS CAN BE SAVED, DOWNLOADED, AND APPLIED FOR REAL**

Both What-if pages now let you save a scenario under a name and open it again later, and download the results as a CSV file. When every change is a straight swap (a food for a food at the same weight, or a recipe for a recipe at the same servings), **Apply these replacements for real…** makes the swap in your meals or recipes. A confirmation page first lists exactly which ones will change and which won't. [learn more...](#whatif-apply)

<!--
```
Scope: Analysis -> What-if: meals / recipes (WHATIF-PLAN.md Phase 4). New table
saved_whatif_scenarios (name, page, query) storing the page's own query string,
minus "applied"; db.saved_whatif_*; routes /analysis/whatif/save, /load/{id},
/saved/rename, /saved/delete; macros saved_panel / result_actions /
applied_banner in _whatif_changes.html. CSV: /analysis/whatif/export.csv and
/analysis/whatif-recipes/export.csv via whatif.meals_csv()/recipes_csv();
evaluate_recipes(max_columns=None) for an uncapped recipe CSV. Route bodies
split into _whatif_meals_compute()/_whatif_recipes_compute() so page, CSV and
apply share one computation. Apply: whatif.real_substitution_problems() (pure)
allows only replace food->food "grams" or recipe->recipe "servings", since
db.substitute_item_in_meals/_recipes keep the stored amount as a number; chains
and duplicate items refused. GET /analysis/whatif/apply = confirmation
(analysis_whatif_apply.html) listing direct targets via new
db.meals_with_direct_item / recipes_with_direct_ingredient and the nested-only
count (what-if hits minus direct); POST re-plans from the query, substitutes in
one transaction, recomputes DCP for changed recipes, redirects with applied=N.
whatif.py itself still never writes.
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

[^8]: Atkinson, Brand-Miller, Foster-Powell, Buyken & Goletzke, "International tables of glycemic index and glycemic load values 2021: a systematic review," *The American Journal of Clinical Nutrition* 114(5):1625–1632 (doi:10.1093/ajcn/nqab233). The newer of the two editions involved. NuMa does not ship it — its license forbids that — but it can read it into your own copy in a few minutes; see [Upgrading to the 2021 tables](#gi-editions). The published table is actually two online supplemental tables, and the thing to understand about them is that they are split by **how well the study was run, not by who it was run on**: **Supplemental Table 1** holds values from studies whose method was consistent with ISO 26642:2010 (food numbers 1–2091), and **Supplemental Table 2** holds values from studies that deviated from that standard — fewer than ten subjects, an unusual carbohydrate portion, an unrepeated reference food — or whose results varied widely (2092–4018). Most of Table 2 was still measured in normal-glucose-tolerance subjects, so NuMa takes each row's subject group from that row's own "Subjects (type & number)" column and carries ISO compliance as a separate flag; see [Method quality](#gi-method-quality). This is a change from the 2008 edition, whose two appendix tables genuinely were split by population. Values are taken from the glucose-referenced GI column (GI, Glucose=100), matching the scale NuMa uses everywhere else. Glycemic load is not imported from the table at all: the published GL is a *nominal* figure computed from a standardized carbohydrate portion for the whole food category, and the source itself calls it "intended as a guide only", so NuMa computes GL live from a food's own cached carbohydrate content and the amount consumed instead (see [Glycemic Load](#gl)). Each row also publishes its **year of test** and country of food production, which NuMa shows in the lookup — see [How to read a lookup result](#gi-result-row). Licensing: published under the Elsevier user license, which expressly permits "access, download, copy, translate, text and data mine" for non-commercial purposes but forbids redistribution, reposting and adaptation. That is precisely why NuMa ships the parser and the Creative Commons 2008 edition[^8a] rather than this table: extracting the data for your own use is something the license allows *you* to do, and the resulting file stays on your machine. Copyright is held by the American Society for Nutrition; permission to distribute would have to come from them via the publisher. (For technically skilled users: table ingestion is `scripts/build_gi_data.py`, producing the local-only `gi_data_local.json`, which `gi_lookup.py` prefers over the bundled `gi_data.json` whenever it exists; lookup/matching logic is `gi_lookup.py`. The 2008 ingest script is kept as `scripts/build_gi_data_2008.py` but is not part of a normal build. A separate, older helper, `import_gi_seed.py`, bulk-applies exact name matches from a small 62-item starter set for automation/demo-data purposes.) Every entry cites its source study by number, listed in the supplemental tables' own footnotes and reference list; a code beginning **UO** means "unpublished observations", for which there is no paper to trace.

[^8a]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2008," *Diabetes Care* 31(12):2281–3. **The edition built into NuMa**, and the one every install has. A Creative Commons–licensed table, which is exactly why it can ship with the program at all. If you add the 2021 edition[^8] yourself, NuMa keeps the few hundred of this edition's foods that 2021 does not appear to cover, labeled **2008 edition** in lookup results — see [Upgrading to the 2021 tables](#gi-editions). Those rows have no year of test, no standard error and no country, because this edition did not publish them in a form NuMa captured; "2008" on such a row is the edition it came from, never the year the food was tested.

[^8b]: Foster-Powell, Holt & Brand-Miller, "International table of glycemic index and glycemic load values: 2002," *The American Journal of Clinical Nutrition* 76(1):5–56. Deliberately **not** used. It is the direct predecessor of the 2008 table above, which revised and absorbed it, so adding it would mainly contribute duplicate food names carrying older values for the same studies — actively worse than not having them, since the lookup shows you every plausible match to choose between. Listed here only to record that it was considered and why it was rejected.

[^9]: US National Institutes of Health. (2026, July 31). Office of Dietary Supplements—Nutrient Recommendations and Databases. https://ods.od.nih.gov/HealthInformation/nutrientrecommendations.aspx

[^10]: NuMa's own curated table of amino-acid profiles for common protein-complement foods — beans, grains, seeds, and a few animal foods included for comparison (`_COMPLEMENT_TABLE` in `usda_nutrients.py`). 23 of the 25 entries cite a specific [USDA](#gloss-usda) FoodData Central SR Legacy record by FDC ID, sourced the same way as the rest of NuMa's nutrient data[^2]; the remaining two (nutritional yeast, pea protein powder) use published amino-acid-composition literature values because no matching USDA record exists for those specific products. NuMa always checks your own food cache for a real match to each entry's food name before falling back to these built-in figures — see [amino acid estimates in complement suggestions](#comp-estimate).

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

