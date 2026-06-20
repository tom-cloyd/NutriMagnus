"""
drafted_foods.py — user-drafted food profile management for numa.

Handles editing any cached food's nutrients, and the full drafted-profile
workflow (create, edit, delete, bulk AA import).  Called from foods.py.
Docs: README-numa-documentation.md, Architecture: "numa_app/workflows/drafted_foods.py — cache editing and drafted profiles"
"""
import json
import re

from rich.table import Table

import db as _db
import usda as _usda
from .. import state
from ..services.search import _search_and_pick_food
from ..ui.common import _id_cell, ID_KEY, _prompt_with_options, _show_menu, dot_cell, table_title, table_footer, help_footer
from ..ui.prompts import Cancelled, ReturnToMain, _ask_int, _prompt
from ..ui.render import _print_nutrient_table

def _edit_portions(portions: list) -> list:
    """Interactively add / remove portion entries. Returns updated list."""
    state.console.print(f"\n  [{state.T['hi']}]Portion and weight[/{state.T['hi']}]  [grey62]— maps serving descriptions to grams (e.g. '2 tablespoons = 18 g')[/grey62]")
    if portions:
        for i, p in enumerate(portions, 1):
            state.console.print(f"    {i}.  {p['description']}  —  {p['gram_weight']:.1f} g")
    else:
        state.console.print("  [grey62]  None on file.[/grey62]")

    first = True
    while True:
        state.console.print()
        if first:
            prompt_label = "Portion description  [grey62](e.g. '2 tablespoons', '1 cup' · Enter alone = done · r#=remove entry)[/grey62]"
        else:
            prompt_label = "Additional portion description (optional)  [grey62](Enter alone = done · r#=remove entry)[/grey62]"
        try:
            desc = _prompt(prompt_label, free_text=True).strip()
        except Cancelled:
            break

        if not desc or desc.lower() == "b":
            break
        if desc.lower() == "m":
            raise ReturnToMain()
        if desc.lower() == "q":
            raise SystemExit(0)

        # r1, r2 … — remove by index
        if desc.lower().startswith("r") and desc[1:].isdigit():
            idx = int(desc[1:])
            if 1 <= idx <= len(portions):
                removed = portions[idx - 1]
                portions = [p for i, p in enumerate(portions, 1) if i != idx]
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Removed: {removed['description']}")
                for i, p in enumerate(portions, 1):
                    state.console.print(f"    {i}.  {p['description']}  —  {p['gram_weight']:.1f} g")
            else:
                state.console.print(f"  [{state.T['warning']}]No portion #{idx}.[/{state.T['warning']}]")
            first = False
            continue

        while True:
            try:
                gw_raw = _prompt(f"Weight of '{desc}' in grams  [grey62](b=back)[/grey62]", free_text=True).strip()
            except Cancelled:
                break
            if not gw_raw or gw_raw.lower() == "b":
                break
            try:
                gw = float(gw_raw)
                portions = portions + [{"description": desc, "gram_weight": gw}]
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Added: {desc} = {gw:.1f} g")
                first = False
                break
            except ValueError:
                state.console.print(f"  [{state.T['warning']}]Enter a number.[/{state.T['warning']}]")

    return portions


def _do_edit_cached_food(fdc_id: int, cached) -> None:
    """
    Edit any cached food's profile — name, serving metadata, nutrients, note.
    After saving, marks the entry user_drafted=True so automatic re-fetches
    will not overwrite the changes.
    """
    existing_nutrients: dict = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    existing_portions: list = []
    pj = cached["portions_json"]
    if pj and pj != "null":
        existing_portions = json.loads(pj)

    # Detect supplement mode: single portion with gram_weight == 100
    is_supplement = (
        len(existing_portions) == 1
        and existing_portions[0].get("gram_weight") == 100.0
    )
    unit_name = "tablet"
    if is_supplement:
        desc = existing_portions[0].get("description", "1 tablet")
        unit_name = re.sub(r"^1\s*", "", desc).strip() or "tablet"

    # For user-drafted foods not already in supplement mode, ask if they should be
    if not is_supplement and cached["user_drafted"]:
        try:
            supp_q = _prompt(
                "Is this a supplement?  [grey62](tablet, capsule, softgel, scoop… — y/N)[/grey62]",
                choices=["y", "n"], default="n"
            )
        except Cancelled:
            supp_q = "n"
        if supp_q == "y":
            is_supplement = True
            try:
                unit_name = _prompt(
                    "Unit name  [grey62](Enter for 'tablet' — or: capsule / softgel / pill / scoop)[/grey62]",
                    default="tablet"
                ).strip() or "tablet"
            except Cancelled:
                unit_name = "tablet"
            existing_portions = [{"description": f"1 {unit_name}", "gram_weight": 100.0}]

    state.console.print(
        f"\n[{state.T['hi']}]Editing:[/{state.T['hi']}] [bold]{cached['name']}[/bold]\n"
        f"[grey62]Press Enter to keep the current value for each field.[/grey62]"
    )
    if not cached["user_drafted"]:
        state.console.print(
            f"\n[grey62]This is a cached {cached['data_type'] or 'external'} food. "
            f"Saving will mark it as user-modified — automatic re-fetches "
            f"will not overwrite your changes.[/grey62]"
        )
    state.console.print()

    # Name
    try:
        name = _prompt(
            "Food name (edit or press Enter to keep)",
            default=cached["name"], prefill=True, free_text=True, two_line=True,
        ).strip()
    except Cancelled:
        return
    if not name:
        name = cached["name"]
    elif name.lower() == "b":
        return
    elif name.lower() == "m":
        raise ReturnToMain()
    elif name.lower() == "q":
        raise SystemExit(0)

    # Serving size / unit — kept silently from existing data; not prompted
    if is_supplement:
        serving_size = 1.0
        serving_unit = unit_name
    else:
        serving_size = cached["serving_size"]
        serving_unit = cached["serving_unit"]

    # Portions  (supplements have a fixed single-portion structure — skip)
    if not is_supplement:
        existing_portions = _edit_portions(existing_portions)

    # Nutrients
    if is_supplement:
        state.console.print(
            f"\n  [{state.T['hi']}]Supplement mode:[/{state.T['hi']}]"
            f" enter values per [bold]{unit_name}[/bold] (as shown on the label)."
        )
    nutrients = _prompt_nutrients(
        existing_nutrients,
        unit_label=unit_name if is_supplement else "100g",
    )

    # Note
    try:
        notes = _prompt(
            "Note  [grey62](Enter to keep, '-' to clear)[/grey62]",
            default=cached["notes"] or ""
        ).strip()
    except Cancelled:
        notes = cached["notes"] or ""
    if notes == "-":
        notes = ""

    with _db.get_db() as conn:
        _db.update_cached_food_profile(
            conn, fdc_id, name, nutrients,
            data_type="User Drafted",
            serving_size=serving_size,
            serving_unit=serving_unit,
            portions=existing_portions,
            notes=notes or None,
            user_drafted=True,
        )

    per_label = f"per {unit_name}" if is_supplement else "per 100g"
    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Profile updated: [bold]{name}[/bold]"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label=per_label)


# ---------------------------------------------------------------------------
# Drafted food profiles
# ---------------------------------------------------------------------------

# Ordered lists of (nutrient_key, display_label, unit) for user prompting.
_DRAFT_MACROS = [
    ("calories",         "Calories",            "kcal"),
    ("protein_g",        "Protein",             "g"),
    ("fat_g",            "Total fat",           "g"),
    ("carbs_g",          "Carbohydrates",       "g"),
    ("fiber_g",          "Fiber",               "g"),
    ("sugar_g",          "Sugars",              "g"),
    ("saturated_fat_g",  "Saturated fat",       "g"),
    ("mono_fat_g",       "Monounsaturated fat", "g"),
    ("poly_fat_g",       "Polyunsaturated fat", "g"),
    ("omega3_ala_mg",    "ALA (omega-3)",       "mg"),
    ("omega3_epa_mg",    "EPA (omega-3)",       "mg"),
    ("omega3_dha_mg",    "DHA (omega-3)",       "mg"),
    ("omega6_la_mg",     "Linoleic (omega-6)",  "mg"),
    ("sodium_mg",        "Sodium",              "mg"),
]

_DRAFT_MINERALS = [
    ("calcium_mg",       "Calcium",             "mg"),
    ("iron_mg",          "Iron",                "mg"),
    ("magnesium_mg",     "Magnesium",           "mg"),
    ("phosphorus_mg",    "Phosphorus",          "mg"),
    ("potassium_mg",     "Potassium",           "mg"),
    ("zinc_mg",          "Zinc",                "mg"),
]

_DRAFT_VITAMINS = [
    ("vitamin_a_mcg",    "Vitamin A",           "mcg RAE"),
    ("vitamin_c_mg",     "Vitamin C",           "mg"),
    ("vitamin_d_mcg",    "Vitamin D",           "mcg"),
    ("vitamin_e_mg",     "Vitamin E",           "mg"),
    ("vitamin_k_mcg",    "Vitamin K",           "mcg"),
    ("thiamin_mg",       "Thiamin (B1)",         "mg"),
    ("riboflavin_mg",    "Riboflavin (B2)",      "mg"),
    ("niacin_mg",        "Niacin (B3)",          "mg"),
    ("b6_mg",            "Vitamin B6",           "mg"),
    ("folate_mcg",       "Folate (B9)",          "mcg"),
    ("b12_mcg",          "Vitamin B12",          "mcg"),
]

_DRAFT_PHYTO = [
    ("beta_carotene_mcg",     "Beta-carotene",        "mcg"),
    ("alpha_carotene_mcg",    "Alpha-carotene",       "mcg"),
    ("lycopene_mcg",          "Lycopene",             "mcg"),
    ("lutein_zeaxanthin_mcg", "Lutein + zeaxanthin",  "mcg"),
    ("choline_mg",            "Choline",              "mg"),
    ("beta_sitosterol_mg",    "Beta-sitosterol",      "mg"),
    ("isoflavones_mg",        "Isoflavones",          "mg"),
]

# Vitamins that supplement labels often express in IU instead of mg/mcg.
# Value is the conversion factor: stored_unit = IU × factor.
_IU_VITAMINS: dict[str, float] = {
    "vitamin_a_mcg": 0.3,    # 1 IU retinol/retinyl ester = 0.3 mcg RAE
    "vitamin_d_mcg": 0.025,  # 1 IU = 0.025 mcg  (= 1/40 mcg)
    "vitamin_e_mg":  0.67,   # 1 IU natural d-alpha-tocopherol = 0.67 mg
}

_DRAFT_AMINO_ACIDS = [
    ("aa_tryptophan_g",   "Tryptophan",    "g"),
    ("aa_threonine_g",    "Threonine",     "g"),
    ("aa_isoleucine_g",   "Isoleucine",    "g"),
    ("aa_leucine_g",      "Leucine",       "g"),
    ("aa_lysine_g",       "Lysine",        "g"),
    ("aa_methionine_g",   "Methionine",    "g"),
    ("aa_cystine_g",      "Cystine",       "g"),
    ("aa_phenylalanine_g","Phenylalanine", "g"),
    ("aa_tyrosine_g",     "Tyrosine",      "g"),
    ("aa_valine_g",       "Valine",        "g"),
    ("aa_histidine_g",    "Histidine",     "g"),
]

# Maps every name/abbreviation a literature source might use to the program's
# internal nutrient key.  Keys are lowercase; matching is case-insensitive.
_AA_NAME_LOOKUP: dict[str, str] = {
    # Tryptophan
    "tryptophan": "aa_tryptophan_g",  "trp": "aa_tryptophan_g",  "w": "aa_tryptophan_g",
    # Threonine
    "threonine":  "aa_threonine_g",   "thr": "aa_threonine_g",   "t": "aa_threonine_g",
    # Isoleucine
    "isoleucine": "aa_isoleucine_g",  "ile": "aa_isoleucine_g",  "i": "aa_isoleucine_g",
    # Leucine
    "leucine":    "aa_leucine_g",     "leu": "aa_leucine_g",     "l": "aa_leucine_g",
    # Lysine
    "lysine":     "aa_lysine_g",      "lys": "aa_lysine_g",      "k": "aa_lysine_g",
    # Methionine
    "methionine": "aa_methionine_g",  "met": "aa_methionine_g",  "m": "aa_methionine_g",
    # Cystine — accept cysteine too (they differ by one hydrogen; literature uses both)
    "cystine":    "aa_cystine_g",     "cysteine": "aa_cystine_g",
    "cys":        "aa_cystine_g",     "c": "aa_cystine_g",
    # Phenylalanine
    "phenylalanine": "aa_phenylalanine_g", "phe": "aa_phenylalanine_g", "f": "aa_phenylalanine_g",
    # Tyrosine
    "tyrosine":   "aa_tyrosine_g",    "tyr": "aa_tyrosine_g",    "y": "aa_tyrosine_g",
    # Valine
    "valine":     "aa_valine_g",      "val": "aa_valine_g",      "v": "aa_valine_g",
    # Histidine
    "histidine":  "aa_histidine_g",   "his": "aa_histidine_g",   "h": "aa_histidine_g",
}

# Non-essential AAs we recognize by name but do not store.
_AA_NON_ESSENTIAL: set[str] = {
    "arginine", "arg", "r",
    "alanine", "ala", "a",
    "aspartate", "aspartic", "aspartic acid", "asparagine", "asp", "asn", "d", "n",
    "glutamate", "glutamic", "glutamic acid", "glutamine", "glu", "gln", "e", "q",
    "glycine", "gly", "g",
    "proline", "pro", "p",
    "serine", "ser", "s",
    "hydroxyproline", "hyp",
    "selenocysteine", "sec", "u",
}


def _bulk_import_aa(protein_g: float | None) -> dict:
    """
    Accept amino acid values entered as 'name: value' pairs, one per prompt.
    If protein_g is provided, treats input as g per 100g protein and converts
    to g per 100g food.  If protein_g is None or 0, treats input as g per 100g
    food directly.  Returns a dict of {aa_key: value_per_100g_food}.
    """
    from_protein = (protein_g is not None and protein_g > 0)

    state.console.print(
        f"\n  [{state.T['accent']}]— Bulk amino acid import —[/{state.T['accent']}]"
    )
    if from_protein:
        state.console.print(
            f"  [grey62]Input unit: [bold]g per 100g protein[/bold]  "
            f"(protein content: {protein_g:.2g} g/100g food)\n"
            f"  Values will be converted automatically: "
            f"aa_food = aa_protein × {protein_g:.2g} / 100[/grey62]\n"
            f"  [grey62]Accepted names: full name, 3-letter code, or 1-letter code "
            f"(e.g. tryptophan, trp, W)[/grey62]\n"
            f"  [grey62]Enter one amino acid per line as   name: value   "
            f"— press Enter on a blank line when done.[/grey62]"
        )
    else:
        state.console.print(
            f"  [grey62]Input unit: [bold]g per 100g food[/bold]\n"
            f"  Accepted names: full name, 3-letter code, or 1-letter code "
            f"(e.g. tryptophan, trp, W)\n"
            f"  Enter one amino acid per line as   name: value   "
            f"— press Enter on a blank line when done.[/grey62]"
        )

    raw_entries: list[tuple[str, float]] = []   # (raw_name, raw_value)

    while True:
        try:
            line = _prompt("  AA").strip()
        except Cancelled:
            break
        if not line or line.lower() == "b":
            break
        if line.lower() == "q":
            raise SystemExit(0)

        # Accept "name: value", "name = value", or "name value"
        import re as _re
        m = _re.match(r"^([a-zA-Z][\w\s-]*)[\s:=]+([0-9.]+)\s*$", line)
        if not m:
            state.console.print(
                f"    [{state.T['warning']}]Format not recognised — "
                f"enter as  name: value  (e.g. lysine: 4.8)[/{state.T['warning']}]"
            )
            continue
        name_raw = m.group(1).strip()
        try:
            value = float(m.group(2))
        except ValueError:
            state.console.print(f"    [{state.T['warning']}]Value must be a number.[/{state.T['warning']}]")
            continue
        raw_entries.append((name_raw, value))

    if not raw_entries:
        return {}

    # Classify each entry
    stored:       list[tuple[str, str, float, float]] = []  # (raw_name, key, raw_val, stored_val)
    non_essential: list[tuple[str, float]] = []             # (raw_name, raw_val)
    unrecognized:  list[tuple[str, float]] = []             # (raw_name, raw_val)

    for name_raw, value in raw_entries:
        key_lookup = name_raw.lower().strip()
        if key_lookup in _AA_NAME_LOOKUP:
            aa_key = _AA_NAME_LOOKUP[key_lookup]
            stored_val = value * protein_g / 100.0 if from_protein else value
            stored.append((name_raw, aa_key, value, stored_val))
        elif key_lookup in _AA_NON_ESSENTIAL:
            non_essential.append((name_raw, value))
        else:
            unrecognized.append((name_raw, value))

    # Summary display
    state.console.print()
    if stored:
        state.console.print(f"  [{state.T['success']}]Recognized and stored:[/{state.T['success']}]")
        label_map = {key: label for key, label, _ in _DRAFT_AMINO_ACIDS}
        for name_raw, aa_key, raw_val, stored_val in stored:
            label = label_map.get(aa_key, aa_key)
            if from_protein:
                state.console.print(
                    f"    [{state.T['hi']}]{label:<16}[/{state.T['hi']}]"
                    f"  {raw_val:.4g} g/100g protein  →  {stored_val:.5g} g/100g food  "
                    f"[{state.T['success']}]✓[/{state.T['success']}]"
                )
            else:
                state.console.print(
                    f"    [{state.T['hi']}]{label:<16}[/{state.T['hi']}]"
                    f"  {stored_val:.5g} g/100g food  [{state.T['success']}]✓[/{state.T['success']}]"
                )
    if non_essential:
        state.console.print(f"  [grey62]Not stored (non-essential, not tracked by this program):[/grey62]")
        for name_raw, val in non_essential:
            state.console.print(f"    [grey62]{name_raw}: {val:.4g}[/grey62]")
    if unrecognized:
        state.console.print(f"  [{state.T['warning']}]Unrecognized names — not stored:[/{state.T['warning']}]")
        for name_raw, val in unrecognized:
            state.console.print(
                f"    [{state.T['warning']}]{name_raw}: {val:.4g}[/{state.T['warning']}]  "
                f"[grey62](check spelling; accepted: full name, 3-letter, or 1-letter code)[/grey62]"
            )

    return {aa_key: stored_val for _, aa_key, _, stored_val in stored}


def _list_drafted_foods() -> list:
    """Print a table of all user-drafted foods and return the rows."""
    with _db.get_db() as conn:
        rows = _db.list_user_drafted_foods(conn)
    if not rows:
        state.console.print("[grey62]No drafted food profiles yet.[/grey62]")
        return []
    table_title("DRAFTED FOOD PROFILES")
    _NAME_W = 36
    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("#",    justify="right", min_width=3)
    tbl.add_column("Name", min_width=_NAME_W, max_width=_NAME_W, no_wrap=True)
    tbl.add_column("Note", min_width=24)
    for i, r in enumerate(rows, 1):
        tbl.add_row(str(i), dot_cell(r["name"], _NAME_W), r["notes"] or "")
    state.console.print(tbl)
    help_footer("drafted-foods")
    return list(rows)


def _prompt_nutrients(existing: dict | None = None, unit_label: str = "100g") -> dict:
    """
    Interactively prompt for nutrient values (per 100 g, or per serving if unit_label set).
    existing: pre-fill from this dict if provided (e.g. loaded from USDA cache).
    unit_label: display label for the denominator — "100g" for foods, "tablet" etc. for supplements.
    Returns a nutrients dict (may be partial if user exits early via Ctrl+C or 'b').
    Raises ReturnToMain if user types 'm'. Raises SystemExit on 'q'.
    """
    if unit_label == "100g":
        state.console.print(
            f"\n  [grey62]Enter nutrient values per [bold]100 g[/bold]. "
            f"Press Enter to keep the current value, or enter a number to override. "
            f"Ctrl+C or [bold]b[/bold] to stop and save what you have so far.[/grey62]"
        )
    else:
        state.console.print(
            f"\n  [grey62]Enter the values shown on the label for [bold]1 {unit_label}[/bold]. "
            f"Vitamins A, D, and E may be entered in IU (e.g. [bold]400 IU[/bold]). "
            f"Press Enter to keep the current value, or Ctrl+C / [bold]b[/bold] to stop.[/grey62]"
        )
    nutrients: dict = dict(existing) if existing else {}

    def _prompt_field(key: str, label: str, unit: str, precision: str = ".4g") -> bool:
        """Prompt for one field. Returns False if user bailed (Ctrl+C or b)."""
        iu_factor = _IU_VITAMINS.get(key)
        prompt_unit = f"{unit} or IU" if iu_factor else unit
        current = existing.get(key) if existing else None
        default_str = f"{current:{precision}}" if current is not None else None
        while True:
            try:
                raw = _prompt(
                    f"  {label} ({prompt_unit} per {unit_label})",
                    default=default_str or ""
                ).strip()
            except Cancelled:
                return False
            lower = raw.lower()
            if lower == "q":
                raise SystemExit(0)
            if lower == "m":
                raise ReturnToMain()
            if lower == "b":
                return False
            if not raw:
                if current is not None:
                    nutrients[key] = current
                return True
            # IU input: "2000 IU" or "2000iu"
            if iu_factor and lower.endswith("iu"):
                val_str = raw[:lower.rfind("iu")].strip()
                try:
                    iu_val = float(val_str)
                    converted = iu_val * iu_factor
                    state.console.print(
                        f"    [grey62]→ {converted:.4g} {unit}  "
                        f"({iu_val:g} IU × {iu_factor} = {converted:.4g} {unit})[/grey62]"
                    )
                    nutrients[key] = converted
                    return True
                except ValueError:
                    pass
            # Native unit — strip optional "mg"/"mcg" suffix then parse
            val_str = re.sub(r"\s*(mg|mcg)\s*$", "", lower).strip()
            try:
                nutrients[key] = float(val_str if val_str else raw)
                return True
            except ValueError:
                if iu_factor:
                    state.console.print(
                        f"    [{state.T['warning']}]Enter a number in {unit} "
                        f"or append IU  (e.g. 50  or  2000 IU)[/{state.T['warning']}]"
                    )
                else:
                    state.console.print(f"    [{state.T['warning']}]Enter a number (or press Enter to skip).[/{state.T['warning']}]")

    def _prompt_section(fields: list) -> bool:
        """Prompt for a list of fields. Returns False if user bailed."""
        for key, label, unit in fields:
            if not _prompt_field(key, label, unit):
                return False
        return True

    def _ask_section(title: str, hint: str, fields: list) -> bool:
        """Ask whether to enter an optional section, prompt if yes. Returns False if bailed."""
        has_data = existing and any(existing.get(k) for k, _, _ in fields)
        state.console.print()
        state.console.print(
            f"  [{state.T['accent']}]{title}[/{state.T['accent']}]  [grey62]{hint}[/grey62]"
        )
        try:
            ans = _prompt("  Enter values?", choices=["y", "n"],
                          default="y" if has_data else "n")
        except Cancelled:
            return False
        if ans == "y":
            return _prompt_section(fields)
        return True

    # --- Basic macros (always prompted) ---
    state.console.print(f"\n  [{state.T['accent']}]— Basic nutrients —[/{state.T['accent']}]")
    if not _prompt_section(_DRAFT_MACROS):
        return nutrients

    # --- Minerals (optional) ---
    if not _ask_section(
        "Minerals",
        "Calcium · Iron · Magnesium · Phosphorus · Potassium · Zinc",
        _DRAFT_MINERALS,
    ):
        return nutrients

    # --- Vitamins (optional) ---
    if not _ask_section(
        "Vitamins",
        "A · C · D · E · K · B1 (Thiamin) · B2 · B3 · B6 · B9 (Folate) · B12",
        _DRAFT_VITAMINS,
    ):
        return nutrients

    # --- Amino acids (optional — three-way choice) ---
    state.console.print()
    state.console.print(
        f"  [{state.T['accent']}]Amino acid profile[/{state.T['accent']}]"
        f"  [grey62](enables protein completeness analysis)[/grey62]"
    )
    state.console.print("  [grey62]1[/grey62]  Enter values one-by-one (g per 100g food)")
    state.console.print("  [grey62]2[/grey62]  Bulk import from literature (g per 100g protein — auto-converted)")
    state.console.print("  [grey62]n[/grey62]  Skip")
    while True:
        try:
            aa_choice = _prompt("  Choice", choices=["1", "2", "n"], default="n").strip().lower()
        except Cancelled:
            aa_choice = "n"
        if aa_choice in ("1", "2", "n"):
            break
    if aa_choice == "1":
        state.console.print(f"\n  [{state.T['accent']}]— Amino acids (g per 100g food) —[/{state.T['accent']}]")
        state.console.print("  [grey62]All are optional. Press Enter to skip, Ctrl+C or 'b' to stop.[/grey62]")
        for key, label, unit in _DRAFT_AMINO_ACIDS:
            if not _prompt_field(key, label, unit, precision=".5g"):
                return nutrients
    elif aa_choice == "2":
        bulk_result = _bulk_import_aa(nutrients.get("protein_g"))
        nutrients.update(bulk_result)

    # --- Phytonutrients (optional) ---
    if not _ask_section(
        "Phytonutrients",
        "Beta-carotene · Alpha-carotene · Lycopene · Lutein+zeaxanthin · Choline · Beta-sitosterol · Isoflavones",
        _DRAFT_PHYTO,
    ):
        return nutrients

    return nutrients


def _do_copy_cached_food() -> None:
    """Search the cache, pick any food, copy its data into a new user-drafted entry."""
    state.console.print(
        f"\n  [{state.T['hi']}]Copy a cached food as a draft[/{state.T['hi']}]\n"
        f"  [grey62]Copies nutrient data from any cached food into a new editable draft.[/grey62]"
    )
    try:
        query = _prompt("Search cached foods", free_text=True).strip()
    except Cancelled:
        return
    if not query or query.lower() in ("b", ""):
        return

    with _db.get_db() as conn:
        rows = _db.search_cached_foods(conn, query)
    if not rows:
        state.console.print(f"[{state.T['warning']}]No cached foods matching '{query}'.[/{state.T['warning']}]")
        return

    _CNAME_W = 36
    _CBRAND_W = 24

    with _db.get_db() as _ann_conn:
        _anns = _db.annotations_for_fdcids(
            _ann_conn, [r["fdc_id"] for r in rows if isinstance(r["fdc_id"], int)]
        )

    tbl = Table(show_header=True, header_style=state.T["accent_plain"], box=None, padding=(0, 1))
    tbl.add_column("#",             justify="right", min_width=3)
    tbl.add_column("Type",          min_width=12)
    tbl.add_column("ID",            justify="right", min_width=7)
    tbl.add_column("Food / Recipe", min_width=_CNAME_W, max_width=_CNAME_W, no_wrap=True)
    tbl.add_column("Brand",         min_width=_CBRAND_W, max_width=_CBRAND_W, no_wrap=True)
    tbl.add_column("Ann",           min_width=5)
    tbl.add_column("AA data",       min_width=8)

    for _ci, r in enumerate(rows, 1):
        ann = _anns.get(r["fdc_id"])
        has_gi    = ann is not None and ann["gi_estimate"]    is not None
        has_diaas = ann is not None and ann["diaas_estimate"] is not None
        s = state.T["success"]
        if has_gi and has_diaas:
            ann_cell = f"[{s}]GI DI[/{s}]"
        elif has_gi:
            ann_cell = f"[{s}]GI[/{s}][grey62] ··[/grey62]"
        elif has_diaas:
            ann_cell = f"[grey62]·· [/grey62][{s}]DI[/{s}]"
        else:
            ann_cell = "[grey62]·····[/grey62]"

        nutrients = json.loads(r["nutrients_json"]) if r["nutrients_json"] else {}
        if _usda.has_amino_acid_data(nutrients):
            aa_cell = f"[{s}]✓[/{s}]"
        else:
            aa_cell = f"[{state.T['error']}]✗[/{state.T['error']}]"

        brand = r["brand"] or ""
        type_str = f"[{s}]★[/{s}] {r['data_type'] or ''}"
        if not brand:
            brand_cell = f"[grey62]{'·' * _CBRAND_W}[/grey62]"
        else:
            _bt = brand[:_CBRAND_W - 1]
            _bp = _CBRAND_W - len(_bt) - 1
            brand_cell = f"{_bt} [grey62]{'·' * _bp}[/grey62]" if _bp > 0 else _bt

        tbl.add_row(
            str(_ci), type_str, _id_cell(r["fdc_id"]),
            dot_cell(r["name"], _CNAME_W), brand_cell,
            ann_cell, aa_cell,
        )

    state.console.print()
    table_title("Food cache")
    state.console.print(tbl)
    table_footer(f"  {ID_KEY}")
    help_footer("food-cache")

    pick = _ask_int("Pick #")
    if pick is None:
        return
    if pick < 1 or pick > len(rows):
        state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
        return

    with _db.get_db() as conn:
        cached = _db.get_cached_food(conn, rows[pick - 1]["fdc_id"])
    fdc_id = rows[pick - 1]["fdc_id"]
    if cached is None:
        state.console.print(f"[{state.T['warning']}]Food not found in cache.[/{state.T['warning']}]")
        return

    existing_nutrients: dict = json.loads(cached["nutrients_json"]) if cached["nutrients_json"] else {}
    existing_portions: list = []
    pj = cached["portions_json"]
    if pj and pj != "null":
        existing_portions = json.loads(pj)

    state.console.print(
        f"\n  [grey62]Copying: [bold]{cached['name']}[/bold] — press Enter to keep each value.[/grey62]\n"
    )

    try:
        name = _prompt(
            "Food name (edit or press Enter to keep)",
            default=f"Copy of {cached['name']}", prefill=True, free_text=True, two_line=True,
        ).strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return
    if name.lower() == "m":
        raise ReturnToMain()
    if name.lower() == "q":
        raise SystemExit(0)

    try:
        srv_raw = _prompt(
            "Serving size",
            default=f"{cached['serving_size']:.0f}" if cached["serving_size"] else ""
        ).strip()
    except Cancelled:
        srv_raw = ""
    serving_size: float | None = cached["serving_size"]
    if srv_raw:
        try:
            serving_size = float(srv_raw)
        except ValueError:
            pass

    try:
        serving_unit = _prompt(
            "Serving unit  [grey62](e.g. g, oz, cup, tablet)[/grey62]",
            default=cached["serving_unit"] or ""
        ).strip() or cached["serving_unit"]
    except Cancelled:
        serving_unit = cached["serving_unit"]

    nutrients = _prompt_nutrients(existing_nutrients)

    try:
        notes = _prompt(
            "Note  [grey62](Enter to keep, '-' to clear)[/grey62]",
            default=cached["notes"] or ""
        ).strip()
    except Cancelled:
        notes = cached["notes"] or ""
    if notes == "-":
        notes = ""

    with _db.get_db() as conn:
        new_fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn, new_fdc_id, name, "User Drafted",
            brand=cached["brand"],
            serving_size=serving_size,
            serving_unit=serving_unit,
            nutrients=nutrients,
            portions=existing_portions,
            user_drafted=True,
            notes=notes or None,
        )

    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Draft saved: [bold]{name}[/bold]  (ID {new_fdc_id})"
    )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label="per 100g")


def _do_drafted_foods_menu() -> None:
    while True:
        _show_menu("Drafted Food Profiles", [
            ("1", "List drafted profiles"),
            ("2", "Create new drafted profile"),
            ("3", "Edit a drafted profile"),
            ("4", "Delete a drafted profile"),
            ("5", "Copy a cached food as draft"),
            ("b", "Back to Foods menu"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            return

        if choice == "1":
            _list_drafted_foods()

        elif choice == "2":
            _do_create_drafted_food()

        elif choice == "3":
            rows = _list_drafted_foods()
            if not rows:
                continue
            pick = _ask_int("Pick #")
            if pick is None:
                continue
            if pick < 1 or pick > len(rows):
                state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
                continue
            row = rows[pick - 1]
            with _db.get_db() as conn:
                cached = _db.get_cached_food(conn, row["fdc_id"])
            if cached is None:
                state.console.print(f"[{state.T['warning']}]Food not found.[/{state.T['warning']}]")
                continue
            _do_edit_cached_food(row["fdc_id"], cached)

        elif choice == "4":
            rows = _list_drafted_foods()
            if not rows:
                continue
            pick = _ask_int("Pick #")
            if pick is None:
                continue
            if pick < 1 or pick > len(rows):
                state.console.print(f"[{state.T['warning']}]Invalid selection.[/{state.T['warning']}]")
                continue
            row = rows[pick - 1]
            fdc_id = row["fdc_id"]
            try:
                confirm = _prompt(
                    f"Delete [{state.T['hi']}]{row['name']}[/{state.T['hi']}]?",
                    choices=["y", "n"], default="n"
                )
            except Cancelled:
                continue
            if confirm.lower() == "y":
                with _db.get_db() as conn:
                    conn.execute("DELETE FROM foods WHERE fdc_id = ? AND user_drafted = 1", (fdc_id,))
                state.console.print(f"[{state.T['success']}]✓[/{state.T['success']}] Deleted.")

        elif choice == "5":
            _do_copy_cached_food()

        elif choice == "b":
            return
        elif choice == "m":
            raise ReturnToMain()
        elif choice == "q":
            raise SystemExit(0)
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")


def _do_create_drafted_food() -> None:
    state.console.print(
        f"\n  [{state.T['hi']}]Create a drafted food profile[/{state.T['hi']}]\n"
        f"  [grey62]Drafted profiles let you build a best-guess nutrient profile for foods\n"
        f"  lacking complete official data.[/grey62]\n"
    )
    try:
        start = _prompt(
            "Start from a USDA food (pre-fill values) or from scratch?",
            choices=["u", "s"], default="s"
        ).strip().lower()
    except Cancelled:
        return

    existing_nutrients: dict = {}
    default_name = ""
    default_serving_size: float | None = None
    default_serving_unit: str | None = None

    if start == "u":
        food = _search_and_pick_food()
        if food is None:
            return
        existing_nutrients = dict(food.get("nutrients") or {})
        default_name = food.get("name", "")
        default_serving_size = food.get("servingSize")
        default_serving_unit = food.get("servingUnit")
        state.console.print(
            f"\n  [grey62]Loaded: [bold]{default_name}[/bold] — "
            f"you can override any value below.[/grey62]"
        )

    # Name
    try:
        if default_name:
            name = _prompt(
                "Food name (edit or press Enter to keep)",
                default=default_name, prefill=True, free_text=True, two_line=True,
            ).strip()
        else:
            name = _prompt("Food name", free_text=True).strip()
    except Cancelled:
        return
    if not name or name.lower() == "b":
        return
    if name.lower() == "m":
        raise ReturnToMain()
    if name.lower() == "q":
        raise SystemExit(0)

    # Supplement / unit-based mode
    try:
        supp_ans = _prompt(
            "Is this a supplement?  [grey62](tablet, capsule, softgel, scoop… — y/N)[/grey62]",
            choices=["y", "n"], default="n"
        )
    except Cancelled:
        return
    is_supplement = (supp_ans == "y")
    unit_name = "tablet"
    serving_size: float | None = default_serving_size
    serving_unit: str | None = default_serving_unit
    supplement_portions: list = []

    if is_supplement:
        try:
            unit_name = _prompt(
                "Unit name  [grey62](Enter for 'tablet' — or: capsule / softgel / pill / scoop)[/grey62]",
                default="tablet"
            ).strip() or "tablet"
        except Cancelled:
            unit_name = "tablet"
        serving_size = 1.0
        serving_unit = unit_name
        supplement_portions = [{"description": f"1 {unit_name}", "gram_weight": 100.0}]
        state.console.print(
            f"\n  [{state.T['hi']}]Supplement mode:[/{state.T['hi']}]"
            f" enter each value as the amount in one [bold]{unit_name}[/bold],"
            f" exactly as shown on the label."
        )
    else:
        # Serving size (optional metadata)
        try:
            _srv_unit_hint = f" ({default_serving_unit})" if (default_serving_size and default_serving_unit) else ""
            srv_raw = _prompt(
                f"Serving size{_srv_unit_hint}" if default_serving_size else "Serving size  [grey62](e.g. 30, or Enter to skip)[/grey62]",
                default=f"{default_serving_size:.0f}" if default_serving_size else ""
            ).strip()
        except Cancelled:
            srv_raw = ""
        serving_size = None
        if srv_raw:
            try:
                serving_size = float(srv_raw)
            except ValueError:
                pass
        try:
            serving_unit = _prompt(
                "Serving unit  [grey62](e.g. g, oz, cup, tablet — or Enter to skip)[/grey62]" if not default_serving_unit else "Serving unit  [grey62](e.g. g, oz, cup, tablet)[/grey62]",
                default=default_serving_unit or ""
            ).strip() or None
        except Cancelled:
            serving_unit = None

    # Nutrients
    nutrients = _prompt_nutrients(
        existing_nutrients if existing_nutrients else None,
        unit_label=unit_name if is_supplement else "100g",
    )

    # Note
    try:
        notes = _prompt(
            "Note  [grey62](document your sources/assumptions — optional)[/grey62]",
            default=""
        ).strip() or None
    except Cancelled:
        notes = None

    # Confirm before saving
    state.console.print(
        f"\n  [grey62]s[/grey62]  Save draft"
        f"\n  [grey62]d[/grey62]  Discard"
        f"\n  [grey62]m[/grey62]  Discard and return to main menu"
    )
    try:
        action = _prompt("Action", choices=["s", "d", "m"], default="s")
    except Cancelled:
        action = "d"
    if action == "d":
        state.console.print(f"\n  [grey62]Draft discarded.[/grey62]")
        return
    if action == "m":
        state.console.print(f"\n  [grey62]Draft discarded.[/grey62]")
        raise ReturnToMain()

    # Assign a negative fdc_id and save
    with _db.get_db() as conn:
        fdc_id = _db.next_user_drafted_fdc_id(conn)
        _db.cache_food(
            conn, fdc_id, name, "User Drafted",
            brand=None,
            serving_size=serving_size,
            serving_unit=serving_unit,
            nutrients=nutrients,
            portions=supplement_portions,
            user_drafted=True,
            notes=notes,
        )

    per_label = f"per {unit_name}" if is_supplement else "per 100g"
    state.console.print(
        f"\n  [{state.T['success']}]✓[/{state.T['success']}]  Drafted profile saved: "
        f"[bold]{name}[/bold]  (ID {fdc_id})"
    )
    if is_supplement:
        state.console.print(
            f"  [grey62]Portion: 1 {unit_name}  ·  "
            f"When logged in a meal, contributes exactly the values you entered.[/grey62]"
        )
    if nutrients:
        _print_nutrient_table(nutrients, title=name, per_label=per_label)


