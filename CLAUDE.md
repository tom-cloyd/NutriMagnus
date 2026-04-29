# NutriMagnus (numa) — AI Coding Guide

Nutritional analysis CLI. USDA FoodData Central + Open Food Facts. Python 3.13, stdlib only (no requests, no typer). Rich for terminal output.

Full architecture docs: `README-numa-documentation.md`

---

## Run / Test

```bash
./numa.py                        # launch interactive app
pytest                           # run full test suite
pytest tests/test_cli.py -k foo  # run one test
```

Tests use `NumaTestRunner` (see `tests/conftest.py`) — never call `numa.py` as a subprocess in tests.

---

## Package Layout

```
numa.py              — 5-line CLI entry point (argparse only)
db.py                — all SQLite access (get_db context manager + query functions)
usda.py              — thin re-export shim; edit usda_api.py / usda_nutrients.py instead
usda_api.py          — USDA HTTP client, NUTRIENT_MAP, amino acid constants
usda_nutrients.py    — nutrient math, AA analysis, DIAAS, complement suggestions
diaas.py             — meal-level DIAAS pooled calculation
profile.py           — UserProfile dataclass, RDA computation
export.py            — report rendering (txt / md / html)
openfoodfacts.py     — Open Food Facts API client

numa_app/
  main.py            — initialize_app(), _run_menu(), run_app()
  state.py           — AppContext (Console + theme dict T + dietary flag)
  config/
    prefs.py         — dietary preference load/save
    theme.py         — theme load/save/switch
  ui/
    common.py        — _show_menu, _safe_call, _id_cell, _prompt_with_options,
                       dot_cell, section_title, table_title, table_footer, ID_KEY
    prompts.py       — _prompt(), Cancelled, ReturnToMain, _ask_float/int/date
    render.py        — _print_nutrient_table, _print_protein_completeness, _print_bioavailability,
                       _print_recipe_bioavailability, _print_rda_comparison
  services/
    portions.py      — _parse_portion_input(), _pick_portion()
    search.py        — _search_and_pick_food()
    reports.py       — auto-save + user-export offer
  workflows/
    foods.py         — Foods menu
    drafted_foods.py — drafted food profile CRUD
    pantry.py        — My Pantry menu
    meals.py         — Meals & Log menu
    recipes.py       — Recipes menu dispatch + shared helpers + create/browse/develop
    recipe_analysis.py — _do_recipe_view (full nutrition analysis)
    recipe_edit.py   — _do_recipe_edit
    settings.py      — Settings menu
    summary.py       — Daily Summary menu
```

---

## Navigation Contract

Every interactive function obeys this protocol:

| Signal | Meaning | How raised |
|--------|---------|-----------|
| `Cancelled` | cancel this action, back to menu | Ctrl+C / Escape / `b` at prompt |
| `ReturnToMain` | jump straight back to main menu | user types `m` at any prompt |
| `SystemExit(0)` | quit program | user types `q` at any prompt |

**`_safe_call(fn, *args)`** — wrap every menu-action dispatch with this. It catches `Cancelled` (prints "Cancelled.") and lets `ReturnToMain` and `SystemExit` propagate.

**`_prompt(prompt_text, *, default, choices, free_text, prefill)`** — the only way to get user input. Never use bare `input()`. `choices=["y","n"]` enables single-keypress mode (only listed chars accepted). `free_text=True` uses readline with backspace. `prefill=True` pre-populates the line with `default` for in-place editing.

**`_prompt_with_options(label, options, *, default)`** — displays a numbered/lettered options block above the prompt, then collects free-text input. Use this (not raw `state.console.print` + `_prompt`) when presenting explicit choices with descriptions. `options` is `list[tuple[str, str]]` — `[("1", "Search USDA"), ("2", "Enter name only")]`.

Workflow functions that present a sub-loop should catch `Cancelled` and `break`/`return`, not `except Exception`.

---

## Database Pattern

```python
# ALWAYS use the context manager — it commits on clean exit, rolls back on exception
with _db.get_db() as conn:
    row = _db.recipe_get(conn, rid)

# NEVER hold a connection across a prompt — user input can take seconds/minutes
with _db.get_db() as conn:
    data = _db.some_query(conn)
# ... prompt the user ...
with _db.get_db() as conn:
    _db.some_write(conn, data)
```

`get_db()` is a `@contextmanager`; the connection is `sqlite3.connect(..., check_same_thread=False)` with `row_factory = sqlite3.Row`.

**Row column names** (key tables):

`recipe_list()` / `recipe_get()` rows:
`id, name, description, servings, dcp_g, dcp_computed_at, created_at, complete, last_accessed_at, total_weight, total_weight_unit`
(`recipe_get` also returns `total_volume`, `total_volume_unit`, `instructions`)

`recipe_get_ingredients()` rows:
`id, recipe_id, fdc_id, food_name, amount, unit, notes, ref_recipe_id`

`meal_get_items()` rows:
`id, meal_id, item_type ('food'|'recipe'), fdc_id, recipe_id, food_name, amount, unit, notes`

`pantry_list()` rows:
`id, food_name, fdc_id, notes`

`get_cached_food()` rows:
`fdc_id, name, data_type, brand, serving_size, serving_unit, nutrients_json, portions_json, user_drafted, notes`

---

## `_search_and_pick_food()` Return Value

Returns `None` if the user cancels, or one of two dict shapes depending on what was selected:

**Food selected** (USDA or OFF):
```python
{
    "fdcId":            int,         # USDA FDC ID (positive) or OFF synthetic ID (negative)
    "name":             str,
    "dataType":         str,         # "Foundation", "SR Legacy", "Branded", "Survey (FNDDS)",
                                     # "Experimental", "User Drafted", or "OFF"
    "brand":            str | None,
    "servingSize":      float | None,
    "servingUnit":      str | None,
    "householdServing": str | None,
    "nutrients":        dict[str, float],   # per 100 g, keys from NUTRIENT_MAP
    "portions":         list[dict] | None,  # USDA portion list
}
```

**Recipe selected** (when `prepend_recipes` list was passed):
```python
{
    "_type":        "recipe",
    "id":           int,
    "name":         str,
    "servings":     float,
    "dcp_g":        float | None,
    "total_weight": float | None,
}
```

Callers must check `food.get("_type") == "recipe"` before accessing recipe-only keys.

**`_id_cell(fdc_id)`** (from `ui/common.py`) — renders the ID column value for any food table: positive int → `"123456"` (dim), negative OFF ID → `"OFF"` (dim), `None` → `""`. Always use this for ID columns; never format IDs manually. `ID_KEY` is the matching legend string for `table_footer()`.

---

## Nutrients Dict

All nutrient values are **per 100 g**. The dict is stored as JSON in `foods.nutrients_json` and passed around as `dict[str, float]`.

Valid keys (from `usda_api.NUTRIENT_MAP`):

```
# Macros
calories, protein_g, carbs_g, fat_g, fiber_g, sugar_g,
saturated_fat_g, mono_fat_g, poly_fat_g

# Minerals (mg)
calcium_mg, iron_mg, magnesium_mg, phosphorus_mg,
potassium_mg, sodium_mg, zinc_mg

# Vitamins
vitamin_a_mcg, vitamin_c_mg, vitamin_d_mcg, vitamin_e_mg,
vitamin_k_mcg, thiamin_mg, riboflavin_mg, niacin_mg,
b6_mg, folate_mcg, b12_mcg

# Phytonutrients
beta_carotene_mcg, alpha_carotene_mcg, lycopene_mcg,
lutein_zeaxanthin_mcg, choline_mg, beta_sitosterol_mg, isoflavones_mg

# Amino acids (g) — all prefixed aa_
aa_tryptophan_g, aa_threonine_g, aa_isoleucine_g, aa_leucine_g,
aa_lysine_g, aa_methionine_g, aa_cystine_g, aa_phenylalanine_g,
aa_tyrosine_g, aa_valine_g, aa_histidine_g
```

Essential AAs: all `aa_` keys except `aa_cystine_g` and `aa_tyrosine_g`.
`usda.has_amino_acid_data(nutrients)` → True if 5+ non-zero AA values present.

---

## Theme / Styling

Use `state.T["key"]` for all colors — never hardcode Rich color names.

| Key | Use |
|-----|-----|
| `accent` | bold section headings, numbered menu items |
| `accent_plain` | table header style |
| `success` | ✓, green bars, "met" status |
| `warning` | ⚠, yellow, "approaching" |
| `error` | ✗, red, "over limit" |
| `hi` | bold white — sub-section titles within an analysis |
| `default_hint` | blue — pre-filled defaults in prompts |

**Table/heading helpers** (always use these — don't call `state.console.print` for section structure directly):

```python
from ..ui.common import section_title, table_title, table_footer, dot_cell

section_title("Title", "optional subtitle")   # full-width accent + rule
table_title("Title", "optional Rich markup")  # indented hi-colour title
table_footer("  [dim]legend text[/dim]")      # blank line + footer lines
dot_cell(text, width)                          # truncate + dim dot leaders
```

---

## ? Help System

Users type `?topic` at any prompt to display an inline help panel. The lookup chain is:

1. `_prompt()` in `numa_app/ui/prompts.py` detects a `?`-prefixed input and calls `manual.show(ref)`.
2. `manual.show()` resolves aliases via `_ALIASES`, then looks up `(title, body)` in the parsed section dict.
3. The section is rendered as a Rich `Panel` and the prompt repeats.

**Adding a new help topic:**

1. Add a section to `user-manual.md` with an anchored heading:
   ```
   ## My New Topic [mytopic]

   Plain text body. No markdown tables — Rich renders this as-is inside a Panel.
   ```
   The anchor is the text inside `[…]`, lower-cased. It must be unique.

2. If you want shortcut aliases, add entries to `_ALIASES` in `manual.py`:
   ```python
   "my-topic": "mytopic",
   "my topic": "mytopic",
   ```

3. Surface it from the relevant output block using `help_footer()` in `ui/common.py`:
   ```python
   from ..ui.common import help_footer
   help_footer("mytopic")                  # one topic
   help_footer("mytopic", "diaas")         # two topics — joined with "or"
   ```
   This prints: `At any prompt, type ?mytopic or ?diaas for help with these columns.`

4. Update the topic list in the `## Using the ? Help System [help]` section of `user-manual.md`.

**Format rules for manual sections:**
- Plain text only — no Markdown tables, no bold/italic markup (Rich won't render it).
- Indented preformatted blocks (4-space indent) are preserved as-is.
- `---` separator lines are stripped from section bodies automatically.

---

## Circular Import Pattern

`recipes.py` imports from `recipe_analysis.py` and `recipe_edit.py` at call time (not at module top) to break circular dependencies:

```python
def _do_something():
    from .recipe_analysis import _do_recipe_view   # lazy — inside function body
    from .recipe_edit import _do_recipe_edit
```

Follow this pattern for any new cross-imports between workflow modules.

---

## Key Invariants

- **Never `import usda_api` or `import usda_nutrients` directly** — always `import usda as _usda`. `usda.py` is the stable public surface.
- **Never use `requests`** — HTTP via stdlib `urllib` only (`usda_api.py`).
- **Never use `typer`** — CLI is stdlib `argparse` in `numa.py`.
- **Never open the DB outside `get_db()`** — no raw `sqlite3.connect()` calls in workflow code.
- **Never hold a DB connection across a `_prompt()` call.**
- **Never hardcode Rich color strings** — always `state.T["key"]`.
- **`_prompt()` only** for user input — never bare `input()`.
- **Add `Docs:` line** to any new module's docstring pointing to the relevant README section.

---

## Test Conventions

- `NumaTestRunner.invoke(input="...")` — newline-separated inputs, one per prompt.
- `_mock_api(monkeypatch)` — stubs USDA API; use for any test that touches food search.
- Autouse fixtures handle DB, profile, prefs, export no-op, and OFF stub — don't set these up manually.
- When adding a test for a new recipe flow, map out the full prompt sequence in a comment first (the input string is fragile).
