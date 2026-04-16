# NutriMagnus ("nourishment wizard") - a 21st century nutritional analysis program for individuals and families

UPDATED: 2026-04-01 - 14:36

## About the program name - NutriMagnus

## The problem that NutriMagnus (NM) addresses

Opensource (i.e., free software, with publicly available code) nutrition analysis programs are available, but I wanted one that I could tweak, addresses the problem of variable nutrition needs relative to age, sex, and other special considerations, and particularly addresses the special needs of those eating a mostly or entirely plant-based diet.

Plant-based proteins are far less ecologically damaging to produce than animal protein, and also much less likely to acquire agricultural chemical accumulations, which are then ingested along with the nutrients they contain. They also do not involve the industrialized abuse of vast numbers of animals who live only long enough to produce edible protein and then are treated like an mere object to be processed as we might a fallen tree. 

But, almost all plant proteins come to us with a built-in problem. There are 9 protein building blocks (amino acids) which human bodies cannot make and must therefore ingest. Additionally, they must be ingested in specific proportions. When a food, or meal, or diet lacks or is insufficient in one or more of these "essential" amino acids this has a limiting effect on the utilization of the other 8. This is the "incomplete protein" problem which almost all plant proteins present.

Consider someone building a brick wall. Suppose they order a bag of cement and 500 bricks. It is likely that they will run out of cement before they run out of bricks. This is the limitation problem that is inherent in plant-based diets. While the needed amino acids do not need to all be present in a single food, or recipe, or meal, they do need to be present in approximately any given 24 hour period, if the amino acid limitation problem is to be avoided. So, one way or another one needs to tend to the issue of what is missing and where are you to find it so you can add it to your diet in time.

There are two other related dietary protein problems to be addressed:

* different protein sources in plant-based diets are metabolized in differing degrees of efficiency. Protein in a food, however balanced or not, does no good if our bodies do not access it.

* age differences in protein needs do exist and they are not minor. Older people require substantially more protein than do younger people. Almost all common discussion of dietary protein utterly fails to address this problem.

(The foregoing is a rapidly written summary and needs documentation; this will be added in the future.)

This is a technical problem that is beyond the ability of ordinary people to solve well. An easy-to-use, freely available computer program will go far in solving this problem. This is what the NM project is about.

## Developmental approach

NM is being developed using Claude Code, in the VSCodium programming editor, which allows for rapid progress and excellent human/AI pairing.

Development is focusing at present on coding and validating core features in a command line environment. Progress to a graphic user interface (GUI) is planned, but will not occur until core features are in place. Command and menu-driven operation of NM will always be available after the GUI is working.

## Developmental Plan

#### Phase 1 — Complete ✓

- Search the USDA food database and view detailed nutrient information for any food
- Analyze the nutritional content of a specific portion of a food
- Build and save recipes; view and analyze their nutritional content
- Log meals by date; view what you ate and analyze its nutritional content
- Daily nutrition summary
- Protein completeness analysis: see whether a food, recipe, or meal provides all nine essential amino acids in adequate proportions
- **Automated test suite** *(development tool)*: a set of automated checks that verify every key function of the program still works correctly after any code change. Running the tests after a change immediately reveals what, if anything, has broken — catching errors before they can reach users.

#### Phase 2 — Features coded and in use; two items still planned

**What you can do now:**

- **Richer nutrient information**: In addition to the standard macronutrients and micronutrients, NM tracks several plant bioactive compounds (carotenoids, choline, isoflavones, and others) where USDA data is available. Foods that contain substances known to reduce nutrient absorption are flagged with practical notes on how cooking or preparation reduces their effect.

- **Protein quality score (DIAAS)**: For any food or recipe, NM shows not just how much protein is present but how much your body can realistically use — adjusted for both digestibility and amino acid completeness. This matters especially on a plant-based diet, where raw protein figures routinely overstate what the body actually absorbs.

- **Protein complement suggestions**: After analyzing any food, recipe, meal, or daily summary, NM can suggest specific foods — drawing from your personal pantry list first — that would fill in your amino acid gaps. It calculates the minimum amount needed to close the gap, so you know exactly what to add to your meal.

- **My Pantry**: Keep a personal list of protein sources you currently have on hand. The complement advisor draws from this list first when making suggestions.

- **Meal-level protein quality**: When you analyze a full meal, NM computes a composite protein quality score across all the meal's ingredients combined, capturing how different foods complement each other.

- **Personalized nutrition targets**: Enter your age, sex, weight, height, and activity level, and NM computes calorie, protein, and micronutrient targets calibrated to you. After viewing a daily summary, you can compare your intake against these personal targets, with color-coded results for each nutrient.

- **Dietary preferences**: Tell NM whether to include animal-based foods (eggs, dairy, fish, poultry) in its complement suggestions, or to limit suggestions to plant-based sources only.

- **Recipe portion analysis**: Analyze the nutrients in a specific portion of any saved recipe — for example, how much protein and calcium you get from one serving of your chickpea stew.

- **Flexible portion entry**: Portions can be entered by weight (grams, ounces, pounds), or by volume (cups, tablespoons, teaspoons) for foods where a density is known.

**Still planned for Phase 2:**

- Development of a slightly modified version that will run on Windows operating systems. (The developmental version is Linux-only.)
- Nutrient trend charts or tables: see how your intake of key nutrients has varied over days or weeks
- Meal planning and dietary pattern analysis
- Transition to a graphical user interface (GUI); menu-driven operation will remain available

#### Phase 3 — Planned

- Barcode scanning for packaged foods
- Machine learning components for dietary recommendations

## Output samples

(to be developed)

### Launching program from command line => main menu displayed

![program launch - main menu](26-04-08-status-main-menu.png)

The main menu is simple. There are 4 main functions, each numbered. There are 3 support functions, one of which simply ends the program. Above, I have selected function 2. I want to make sure the recipe I want to enter is not already partially entered. 

**Main menu** function 2 brings up the **Recipes** menu, and again I enter 2, to get a list of the recipes NM knows about. The one I want to enter is not in the list. The **Recipes** menu comes up again, and this time I enter `1` to enter a recipe

### Entering a recipe

![entering a recipe](26-04-08-status-recipe-entry.png)





