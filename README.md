# NutriMagnus — Nutritional Analysis for Individuals and Families

**NutriMagnus ("nutrition wizard")** is a free, open-source nutritional analysis program for individuals and families — with particular depth for people eating plant-based diets.

It analyzes individual foods, recipes, and full daily meals using data from the USDA FoodData Central database (300,000+ foods) and Open Food Facts (millions of packaged products worldwide), as well as 4 other international data sources, plus several more that are internal to the program. No subscription or account is needed for any of this access. An internet connection is needed to look up a food for the first time; anything already looked up is cached locally and works offline from then on.

---

## Disclaimer

NutriMagnus is an informational tool only. It is not a substitute for advice from a qualified dietitian, physician, or other healthcare professional. Nutritional needs vary by individual — always consult a professional before making significant dietary changes. Use of this software is entirely at your own risk.

---

## Who it's for

Anyone who wants to understand what they're actually eating — especially people on plant-based diets, where standard nutrition tools fall short on protein quality analysis.

---

## Key features

- **Food search** — search the USDA database and Open Food Facts; view detailed macro and micronutrient profiles
- **Portion analysis** — analyze any quantity of any food against your personal RDA targets
- **Recipes** — build, save, and fully analyze recipes; develop them interactively with live nutritional feedback
- **Meal logging** — log meals by date; view and analyze what you ate; daily nutrition summary
- **Protein completeness (DIAAS)** — see not just how much protein a food contains, but how much your body can actually use, adjusted for digestibility and amino acid balance
- **Complement suggestions** — NutriMagnus identifies which essential amino acids are missing and suggests specific foods — drawn from your personal pantry first — to fill the gap
- **Oxalate tracking** — flags high-oxalate foods with practical notes (relevant for kidney stone risk and calcium absorption)
- **Multiple user profiles** — different RDA targets for different household members (age, sex, weight, activity level)
- **Personalized nutrient targets** — set a custom "optimal" target above the standard RDA for any nutrient (e.g. higher Vitamin D for older adults), and custom max limits that warn you as you approach them
- **Personal pantry** — keep a list of protein sources on hand; the complement advisor draws from it first
- **Glycemic load tracking** — see the glycemic load of foods, recipes, and full meals
- **Nutrient trends over time** — average your intake over 7, 14, or 30 days, or plot any nutrient across your logged days, to catch a chronic shortfall a single day's numbers would hide
- **CSV export/import** — move foods and recipes between installs, or edit them in a spreadsheet
- **Archive** — hide a food, pantry entry, or recipe you're not currently using without deleting it
- **Printable reports** — generate a print/PDF-ready report for any food, meal, or full day, with a checkbox choice of which sections to include
- **Extensive built-in help** — "Learn more" links throughout the app jump straight to the relevant section of the full User Manual, built in and readable without leaving the app

---

## Download

**Linux (Ubuntu):** Download the latest release from the [Releases page](https://github.com/tom-cloyd/NutriMagnus/releases). Built and tested on Ubuntu 24.04 LTS; it should run on most other modern Linux distros too, but only Ubuntu is verified. If the prebuilt binary doesn't run on yours, see [For developers](#for-developers) below to run it from source instead.

*(Windows version coming.)*

A User Manual is built into the app — open it anytime from the nav bar, or follow a "Learn more" link from the relevant page.

**Want to know when a new version ships?** Click **Watch → Custom → Releases** at the top of this page — GitHub will notify you directly, and it's the only way to hear about updates without checking back yourself.

---

## For developers

Built with Python 3.12, FastAPI, and SQLite. No external services or API keys required for basic use — food search works out of the box on a shared USDA demo key; add your own free key in Settings for higher rate limits.

```bash
git clone https://github.com/tom-cloyd/NutriMagnus
cd NutriMagnus
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python web/launcher.py
```

Full architecture documentation: [README-numa-documentation.md](README-numa-documentation.md)

---

## License

Copyright © 2026 Tom Cloyd. Released under the [PolyForm Noncommercial License 1.0.0](LICENSE) — free to use and modify; commercial use prohibited.
