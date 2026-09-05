# Disclaimer

*Last reviewed: 2026-09-03*

## Not medical advice

NutriMagnus ("NuMa") is a personal food-record and nutrient-calculation tool. It reports estimated nutrient content, amino acid balance, and related figures computed from third-party food composition databases (USDA FoodData Central, Open Food Facts, the Canadian Nutrient File, UK CoFID, Australian AFCD, and French CIQUAL) and from the formulas described in the [User Manual](/manual).

NuMa does not diagnose, treat, cure, or prevent any disease, and nothing it displays — figures, percentages, "complete"/"incomplete" labels, RDA comparisons, or any other output — is medical, dietary, or health advice. It does not know your medical history, lab results, medications, allergies, or the advice your clinician has given you, and it makes no claim that following any pattern of use will produce any particular health outcome, including weight change, symptom relief, or improved lab values.

If you have a medical condition, are pregnant or breastfeeding, are managing a chronic illness, or are considering a significant change to your diet, talk to a physician, registered dietitian, or other qualified health professional before acting on anything you see here. If you think you may be experiencing a medical emergency, contact emergency services immediately — do not rely on this program.

## Data accuracy

NuMa pools nutrient data from multiple public food databases and, for some entries, from values you or a third party (including an AI assistant, for foods fetched via the Food Cache's Claude-assisted lookup) that have been entered by hand. These sources vary in accuracy, completeness, and how recently they were updated, and a food's real nutrient content varies by brand, growing conditions, preparation method, and portion measured in ways no database fully captures.

We routinely check NuMa's calculations for internal correctness — the automated test suite (767 tests as of this writing) runs before every release, and a monthly maintenance sweep includes an accuracy check of sample values against their source databases (see [Data, testing, and validation](/manual#data-testing-validation) in the User Manual for the current test count and [Appendix A](/manual#a-recent-program-updates-log) for the sweep log). These checks confirm that NuMa computes what it claims to compute from the data it's given; they cannot confirm that the underlying third-party data is itself free of errors, nor that any specific food record matches the actual product you ate.

Treat every figure NuMa shows as an informed estimate, not a laboratory measurement. Use your own judgment, and verify anything important (e.g., for a diagnosed allergy or a medically prescribed nutrient limit) against a product label or another authoritative source.

## Your responsibility

You are solely responsible for the food choices, dietary decisions, and any health-related actions you take, whether or not you used NuMa to inform them. NuMa is a calculation and record-keeping aid, not a substitute for professional medical or nutritional judgment, and its author accepts no liability for outcomes arising from its use.

## Questions or corrections

If you find a figure that looks wrong, or have a suggestion for this disclaimer, see [Part 8 — Troubleshooting and feedback](/manual#feedback) in the User Manual.
