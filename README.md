# NutriMagnus — Nutritional Analysis for Individuals and Families

**NutriMagnus ("nutrition wizard")** is a free, open-source nutritional analysis program for individuals and families — with particular depth for people eating plant-based diets.

It analyzes individual foods, recipes, and full daily meals using data from the USDA FoodData Central database (300,000+ foods) and Open Food Facts (millions of packaged products worldwide). No subscription, no account, no internet connection required after first use.

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
- **Personal pantry** — keep a list of protein sources on hand; the complement advisor draws from it first
- **Extensive built-in help** — type `?topic` at any prompt for inline reference panels covering every feature; a full User Manual is included and accessible without leaving the app

---

## Download

**Linux (Ubuntu):** Download the latest release from the [Releases page](https://codeberg.org/Tom_Cloyd/NutriMagnus/releases).

*(Windows version coming.)*

A User Manual is built into the app — type `?` followed by any topic name at any prompt to read it inline.

---

## For developers

Built with Python 3.12, Rich, and SQLite. No external services or API keys required for basic use.

```bash
git clone https://codeberg.org/Tom_Cloyd/NutriMagnus
cd NutriMagnus
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
./numa.py
```

Full architecture documentation: [README-numa-documentation.md](README-numa-documentation.md)

---

## License

Copyright © 2026 Tom Cloyd. Released under the [PolyForm Noncommercial License 1.0.0](LICENSE) — free to use and modify; commercial use prohibited.
