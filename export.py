"""
export.py — Render numa nutrient reports to plain text, markdown, or HTML fragment.

Each report is a list of typed section dicts:
  {"type": "nutrient_table",          "title": str, "nutrients": dict, "per_label": str}
  {"type": "protein_completeness",    "nutrients": dict}
  {"type": "bioavailability",         "food_name": str, "nutrients": dict}
  {"type": "ingredient_list",         "title": str, "items": list[dict]}
    item keys: food_name, amount, unit
  {"type": "recipe_bioavailability",  "ingredient_stats": list[dict], "total_protein": float}
    stat keys: name, amount_g, protein_g, diaas, has_aa, limiting_aa
  {"type": "complement_suggestions",  "nutrients": dict, "base_diaas": float|None}

Formats: "txt", "md", "html"
Docs: README-numa-documentation.md, Project Structure
"""

import pathlib
import re
from datetime import date

import usda as _usda

# Nutrient groups — mirrors _print_nutrient_table in numa.py
_GROUPS: list[tuple[str, list[str]]] = [
    ("Macronutrients", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    ]),
    ("Minerals", [
        "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "zinc_mg",
    ]),
    ("Vitamins", [
        "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
        "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
        "b6_mg", "folate_mcg", "b12_mcg",
    ]),
    ("Phytonutrients", [
        "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
        "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg",
        "isoflavones_mg",
    ]),
]


# ---------------------------------------------------------------------------
# Low-level table builders
# ---------------------------------------------------------------------------

def _txt_table(rows: list[tuple[str, str, str]], col_widths: tuple[int, int, int]) -> str:
    """Return fixed-width text table rows (no header, no border)."""
    lines = []
    for label, amount, unit in rows:
        lines.append(f"  {label:<{col_widths[0]}} {amount:>{col_widths[1]}}  {unit:<{col_widths[2]}}")
    return "\n".join(lines)


def _md_table(header: tuple[str, str, str],
              rows: list[tuple[str, str, str]]) -> str:
    """Return a GitHub-flavored markdown pipe table."""
    lines = [
        f"| {header[0]} | {header[1]} | {header[2]} |",
        f"|:{'─' * len(header[0])}|{'─' * len(header[1])}:|:{'─' * len(header[2])}|",
    ]
    for label, amount, unit in rows:
        lines.append(f"| {label} | {amount} | {unit} |")
    return "\n".join(lines)


def _html_table(header: tuple[str, str, str],
                rows: list[tuple[str, str, str]],
                css_class: str = "numa-table") -> str:
    """Return a bare HTML table fragment (no inline styles)."""
    th = "".join(f"<th>{h}</th>" for h in header)
    body_rows = []
    for label, amount, unit in rows:
        body_rows.append(
            f"    <tr><td>{label}</td><td>{amount}</td><td>{unit}</td></tr>"
        )
    return (
        f'<table class="{css_class}">\n'
        f"  <thead><tr>{th}</tr></thead>\n"
        f"  <tbody>\n"
        + "\n".join(body_rows) +
        "\n  </tbody>\n</table>"
    )


# ---------------------------------------------------------------------------
# Section renderers — nutrient table
# ---------------------------------------------------------------------------

def _nutrient_rows(nutrients: dict[str, float]) -> list[tuple[str, list[tuple[str, str, str]]]]:
    """Return [(group_name, [(label, amount_str, unit), ...]), ...] for present nutrients."""
    result = []
    for group, keys in _GROUPS:
        rows = []
        for k in keys:
            if k in nutrients:
                label, unit = _usda.nutrient_label(k)
                rows.append((label, f"{nutrients[k]:.2f}", unit))
        if rows:
            result.append((group, rows))
    return result


def _render_nutrient_table_txt(title: str, nutrients: dict[str, float],
                               per_label: str = "") -> str:
    heading = title if not per_label else f"{title}  ({per_label})"
    lines = [heading.upper(), "=" * min(len(heading), 60)]
    for group, rows in _nutrient_rows(nutrients):
        lines.append(f"\n{group.upper()}")
        col_w = (max(len(r[0]) for r in rows) + 2, 10, 8)
        lines.append(_txt_table(rows, col_w))
    return "\n".join(lines)


def _render_nutrient_table_md(title: str, nutrients: dict[str, float],
                              per_label: str = "") -> str:
    heading = title if not per_label else f"{title}  *({per_label})*"
    lines = [f"## {heading}"]
    for group, rows in _nutrient_rows(nutrients):
        lines.append(f"\n### {group}")
        lines.append(_md_table(("Nutrient", "Amount", "Unit"), rows))
    return "\n".join(lines)


def _render_nutrient_table_html(title: str, nutrients: dict[str, float],
                                per_label: str = "") -> str:
    sub = f" <em>({per_label})</em>" if per_label else ""
    lines = [f"<h2>{title}{sub}</h2>"]
    for group, rows in _nutrient_rows(nutrients):
        lines.append(f"<h3>{group}</h3>")
        lines.append(_html_table(("Nutrient", "Amount", "Unit"), rows))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section renderers — protein completeness
# ---------------------------------------------------------------------------

def _pc_rows(nutrients: dict[str, float]) -> tuple[dict | None, list[tuple[str, str, str]]]:
    """Return (result_dict_or_None, [(aa_label, score_str, status), ...])."""
    pc = _usda.protein_completeness(nutrients)
    if not pc["has_data"]:
        return None, []
    rows = []
    for aa_key, score in pc["scores"].items():
        label, _ = _usda.nutrient_label(aa_key)
        status = "✓" if score >= 1.0 else "✗"
        rows.append((label, f"{score:.2f}", status))
    return pc, rows


def _render_protein_completeness_txt(nutrients: dict[str, float]) -> str:
    pc, rows = _pc_rows(nutrients)
    if pc is None:
        return "(No amino acid data available.)"
    status = "Complete protein" if pc["complete"] else "Incomplete protein"
    lines = ["PROTEIN QUALITY", "=" * 20, f"  Status: {status}"]
    if not pc["complete"] and pc.get("limiting_aa"):
        lbl, _ = _usda.nutrient_label(pc["limiting_aa"])
        lines.append(f"  Most limiting: {lbl}")
    lines.append(f"\n  {'Amino Acid':<22} {'Score':>6}  {'vs. ref':>7}")
    lines.append(f"  {'-' * 38}")
    for label, score, status_ch in rows:
        lines.append(f"  {label:<22} {score:>6}  {status_ch:>7}")
    return "\n".join(lines)


def _render_protein_completeness_md(nutrients: dict[str, float]) -> str:
    pc, rows = _pc_rows(nutrients)
    if pc is None:
        return "_No amino acid data available._"
    status = "✅ Complete protein" if pc["complete"] else "⚠️ Incomplete protein"
    lines = [f"## Protein Quality\n\n**Status:** {status}"]
    if not pc["complete"] and pc.get("limiting_aa"):
        lbl, _ = _usda.nutrient_label(pc["limiting_aa"])
        lines.append(f"\n**Most limiting amino acid:** {lbl}")
    lines.append("")
    lines.append(_md_table(("Amino Acid", "Score", "vs. reference"), rows))
    return "\n".join(lines)


def _render_protein_completeness_html(nutrients: dict[str, float]) -> str:
    pc, rows = _pc_rows(nutrients)
    if pc is None:
        return "<p><em>No amino acid data available.</em></p>"
    status = "Complete protein" if pc["complete"] else "Incomplete protein"
    cls = "complete" if pc["complete"] else "incomplete"
    lines = [
        "<h2>Protein Quality</h2>",
        f'<p><strong>Status:</strong> <span class="protein-{cls}">{status}</span></p>',
    ]
    if not pc["complete"] and pc.get("limiting_aa"):
        lbl, _ = _usda.nutrient_label(pc["limiting_aa"])
        lines.append(f"<p><strong>Most limiting amino acid:</strong> {lbl}</p>")
    lines.append(_html_table(("Amino Acid", "Score", "vs. reference"), rows,
                             css_class="numa-table aa-scores"))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section renderers — bioavailability
# ---------------------------------------------------------------------------

def _render_bioavailability_txt(food_name: str, nutrients: dict[str, float]) -> str:
    diaas = _usda.get_diaas(food_name)
    flags = _usda.get_antinutrient_flags(food_name)
    if diaas is None and not flags:
        return ""
    lines = ["BIOAVAILABILITY", "=" * 18]
    if diaas is not None:
        raw = nutrients.get("protein_g", 0.0)
        adj = raw * diaas
        lines.append(f"  Protein digestibility (DIAAS): {diaas:.2f}")
        if raw > 0:
            lines.append(f"  Digestible protein: {adj:.1f}g  (from {raw:.1f}g raw)")
    for flag in flags:
        lines.append(f"  Note: {flag['problem']} — {flag['cause']}")
        for label, sol in flag["solutions"]:
            lines.append(f"    * {label}: {sol}")
    return "\n".join(lines)


def _render_bioavailability_md(food_name: str, nutrients: dict[str, float]) -> str:
    diaas = _usda.get_diaas(food_name)
    flags = _usda.get_antinutrient_flags(food_name)
    if diaas is None and not flags:
        return ""
    lines = ["## Bioavailability"]
    if diaas is not None:
        raw = nutrients.get("protein_g", 0.0)
        adj = raw * diaas
        lines.append(f"\n**Protein digestibility (DIAAS):** {diaas:.2f}")
        if raw > 0:
            lines.append(f"**Digestible protein:** {adj:.1f}g  *(from {raw:.1f}g raw)*")
    for flag in flags:
        lines.append(f"\n> ⚠️ **{flag['problem']}** — {flag['cause']}")
        for label, sol in flag["solutions"]:
            lines.append(f"> - *{label}:* {sol}")
    return "\n".join(lines)


def _render_bioavailability_html(food_name: str, nutrients: dict[str, float]) -> str:
    diaas = _usda.get_diaas(food_name)
    flags = _usda.get_antinutrient_flags(food_name)
    if diaas is None and not flags:
        return ""
    lines = ["<h2>Bioavailability</h2>"]
    if diaas is not None:
        raw = nutrients.get("protein_g", 0.0)
        adj = raw * diaas
        lines.append(f"<p><strong>Protein digestibility (DIAAS):</strong> {diaas:.2f}</p>")
        if raw > 0:
            lines.append(
                f"<p><strong>Digestible protein:</strong> {adj:.1f}g "
                f"<em>(from {raw:.1f}g raw)</em></p>"
            )
    for flag in flags:
        lines.append(f'<p class="antinutrient-note">⚠️ <strong>{flag["problem"]}</strong>'
                     f' — {flag["cause"]}</p>')
        if flag["solutions"]:
            items = "".join(f"<li><em>{l}:</em> {s}</li>" for l, s in flag["solutions"])
            lines.append(f'<ul class="antinutrient-solutions">{items}</ul>')
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Section renderers — ingredient list
# ---------------------------------------------------------------------------

def _render_ingredient_list_txt(title: str, items: list[dict]) -> str:
    lines = [f"{title.upper()}", "=" * min(len(title), 60)]
    for item in items:
        lines.append(f"  • {item['food_name']}  {item['amount']} {item['unit']}")
    return "\n".join(lines)


def _render_ingredient_list_md(title: str, items: list[dict]) -> str:
    lines = [f"## {title}"]
    for item in items:
        lines.append(f"- {item['food_name']}  —  {item['amount']} {item['unit']}")
    return "\n".join(lines)


def _render_ingredient_list_html(title: str, items: list[dict]) -> str:
    rows = [(item["food_name"], str(item["amount"]), item["unit"]) for item in items]
    return (
        f"<h2>{title}</h2>\n"
        + _html_table(("Ingredient", "Amount", "Unit"), rows)
    )


# ---------------------------------------------------------------------------
# Section renderers — recipe per-ingredient bioavailability
# ---------------------------------------------------------------------------

def _bio_rows(ingredient_stats: list[dict]) -> tuple[list[tuple], float, float, int]:
    """
    Return (rows, total_protein, total_digestible, unknown_count).
    Each row is (name, amount_str, protein_str, diaas_str, lim_label, dig_str).
    """
    rows = []
    total_protein = 0.0
    total_digestible = 0.0
    unknown_count = 0
    for s in ingredient_stats:
        p = s.get("protein_g", 0.0)
        total_protein += p
        diaas = s.get("diaas")
        amount_g = s.get("amount_g")
        limiting_aa = s.get("limiting_aa")

        if diaas is not None:
            dig = p * diaas
            diaas_str = f"{diaas:.2f}"
        else:
            dig = p
            diaas_str = "?"
            unknown_count += 1
        total_digestible += dig

        amount_str = f"{amount_g:.4g}g" if amount_g else "—"
        if limiting_aa:
            lim_label, _ = _usda.nutrient_label(limiting_aa)
        else:
            lim_label = "— (complete)" if s.get("has_aa") else "—"

        rows.append((s["name"][:30], amount_str, f"{p:.1f}g", diaas_str, lim_label, f"{dig:.1f}g"))
    return rows, total_protein, total_digestible, unknown_count


def _render_recipe_bioavailability_txt(ingredient_stats: list[dict], total_protein: float) -> str:
    if total_protein <= 0:
        return ""
    rows, tp, td, unk = _bio_rows(ingredient_stats)
    lines = ["BIOAVAILABILITY — PER SERVING", "=" * 34]
    lines.append(f"  {'Ingredient':<30}  {'Serving':>8}  {'Crude protein':>13}  {'DIAAS':>6}  {'Limiting IAA':<18}  {'Bioavailable':>12}")
    lines.append(f"  {'-' * 90}")
    for name, amt, prot, diaas, lim, dig in rows:
        lines.append(f"  {name:<30}  {amt:>8}  {prot:>8}  {diaas:>6}  {lim:<18}  {dig:>9}")
    eff = td / tp if tp > 0 else 0.0
    lines.append(f"\n  Total bioavailable protein: {td:.1f}g  (from {tp:.1f}g, effective DIAAS {eff:.2f})")
    if unk:
        lines.append(f"  ({unk} ingredient(s) had no DIAAS data — assumed fully bioavailable)")
    return "\n".join(lines)


def _render_recipe_bioavailability_md(ingredient_stats: list[dict], total_protein: float) -> str:
    if total_protein <= 0:
        return ""
    rows, tp, td, unk = _bio_rows(ingredient_stats)
    lines = ["## Bioavailability — per serving", ""]
    lines.append("| Ingredient | Amount | Protein | DIAAS | Limiting IAA | Bioavailable |")
    lines.append("|:-----------|-------:|--------:|------:|:-------------|-------------:|")
    for name, amt, prot, diaas, lim, dig in rows:
        lines.append(f"| {name} | {amt} | {prot} | {diaas} | {lim} | {dig} |")
    eff = td / tp if tp > 0 else 0.0
    lines.append("")
    lines.append(f"**Total bioavailable protein:** {td:.1f}g  *(from {tp:.1f}g, effective DIAAS {eff:.2f})*")
    if unk:
        lines.append(f"\n*({unk} ingredient(s) had no DIAAS data — assumed fully bioavailable)*")
    return "\n".join(lines)


def _render_recipe_bioavailability_html(ingredient_stats: list[dict], total_protein: float) -> str:
    if total_protein <= 0:
        return ""
    rows, tp, td, unk = _bio_rows(ingredient_stats)
    header = ("Ingredient", "Amount", "Protein", "DIAAS", "Limiting IAA", "Bioavailable")
    th = "".join(f"<th>{h}</th>" for h in header)
    body_rows = []
    for name, amt, prot, diaas, lim, dig in rows:
        body_rows.append(
            f"    <tr><td>{name}</td><td>{amt}</td><td>{prot}</td>"
            f"<td>{diaas}</td><td>{lim}</td><td>{dig}</td></tr>"
        )
    eff = td / tp if tp > 0 else 0.0
    unk_note = (
        f'<p class="diaas-note"><em>({unk} ingredient(s) had no DIAAS data — '
        f'assumed fully bioavailable)</em></p>'
    ) if unk else ""
    return (
        '<h2>Bioavailability — per serving</h2>\n'
        f'<table class="numa-table bioavailability">\n'
        f'  <thead><tr>{th}</tr></thead>\n'
        f'  <tbody>\n'
        + "\n".join(body_rows) +
        '\n  </tbody>\n</table>\n'
        f'<p><strong>Total bioavailable protein:</strong> {td:.1f}g '
        f'<em>(from {tp:.1f}g, effective DIAAS {eff:.2f})</em></p>'
        + unk_note
    )


# ---------------------------------------------------------------------------
# Section renderers — complement suggestions
# ---------------------------------------------------------------------------

def _render_complement_suggestions_txt(nutrients: dict[str, float],
                                       base_diaas: float | None) -> str:
    gaps = _usda.get_aa_gaps(nutrients)
    if not gaps:
        return "PROTEIN COMPLEMENT SUGGESTIONS\n" + "=" * 30 + "\n  No complement suggestions needed."

    suggestions = _usda.suggest_complements(nutrients, pantry_candidates=[], exclude_animal=False)
    general_suggs = sorted(suggestions.get("general", []),
                           key=lambda s: (0.0 if s.get("new_complete") else 1.0,
                                         float(s.get("grams", 10**9) or 10**9)))

    base_protein = nutrients.get("protein_g", 0.0)
    base_digestible = base_protein * base_diaas if base_diaas else base_protein

    gap_labels = ", ".join(
        _usda.nutrient_label(aa)[0] + f" ({score:.2f})"
        for aa, score, _ in gaps
    )
    lines = ["PROTEIN COMPLEMENT SUGGESTIONS", "=" * 30,
             f"  Gaps: {gap_labels}", ""]

    for i, s in enumerate(general_suggs[:5], 1):
        diaas_str = f"  (DIAAS {s['diaas']:.2f})" if s.get("diaas") else ""
        lines.append(f"  Option {i}: {s['name']}{diaas_str}")
        lines.append(f"    Add: {s['grams']}g")
        score_parts = []
        for aa, orig_score, _ in gaps[:3]:
            new_score = s["new_scores"].get(aa, orig_score)
            lbl, _ = _usda.nutrient_label(aa)
            score_parts.append(f"{lbl}: {orig_score:.2f}→{new_score:.2f}")
        lines.append(f"    Effect: {' · '.join(score_parts)}")
        dig = s["digestible_protein_added"]
        raw = s["protein_added"]
        total_dig = base_digestible + dig
        lines.append(f"    Adds: {dig:.1f}g digestible protein (from {raw:.1f}g raw)")
        lines.append(f"    Total bioavailable complete protein = {total_dig:.1f}g")
        lines.append("")

    if not general_suggs:
        lines.append("  No qualifying complement options found.")
    return "\n".join(lines).rstrip()


def _render_complement_suggestions_md(nutrients: dict[str, float],
                                      base_diaas: float | None) -> str:
    gaps = _usda.get_aa_gaps(nutrients)
    if not gaps:
        return "## Protein Complement Suggestions\n\nNo complement suggestions needed."

    suggestions = _usda.suggest_complements(nutrients, pantry_candidates=[], exclude_animal=False)
    general_suggs = sorted(suggestions.get("general", []),
                           key=lambda s: (0.0 if s.get("new_complete") else 1.0,
                                         float(s.get("grams", 10**9) or 10**9)))

    base_protein = nutrients.get("protein_g", 0.0)
    base_digestible = base_protein * base_diaas if base_diaas else base_protein

    gap_labels = ", ".join(
        _usda.nutrient_label(aa)[0] + f" ({score:.2f})"
        for aa, score, _ in gaps
    )
    lines = [f"## Protein Complement Suggestions\n", f"**Gaps:** {gap_labels}", ""]

    for i, s in enumerate(general_suggs[:5], 1):
        diaas_str = f"  *(DIAAS {s['diaas']:.2f})*" if s.get("diaas") else ""
        lines.append(f"### Option {i}: {s['name']}{diaas_str}")
        lines.append(f"- **Add:** {s['grams']}g")
        score_parts = []
        for aa, orig_score, _ in gaps[:3]:
            new_score = s["new_scores"].get(aa, orig_score)
            lbl, _ = _usda.nutrient_label(aa)
            score_parts.append(f"{lbl}: {orig_score:.2f}→{new_score:.2f}")
        lines.append(f"- **Effect:** {' · '.join(score_parts)}")
        dig = s["digestible_protein_added"]
        raw = s["protein_added"]
        total_dig = base_digestible + dig
        lines.append(f"- **Adds:** {dig:.1f}g digestible protein *(from {raw:.1f}g raw)*")
        lines.append(f"- **Total bioavailable complete protein:** {total_dig:.1f}g")
        lines.append("")

    if not general_suggs:
        lines.append("_No qualifying complement options found._")
    return "\n".join(lines).rstrip()


def _render_complement_suggestions_html(nutrients: dict[str, float],
                                        base_diaas: float | None) -> str:
    gaps = _usda.get_aa_gaps(nutrients)
    if not gaps:
        return "<h2>Protein Complement Suggestions</h2>\n<p>No complement suggestions needed.</p>"

    suggestions = _usda.suggest_complements(nutrients, pantry_candidates=[], exclude_animal=False)
    general_suggs = sorted(suggestions.get("general", []),
                           key=lambda s: (0.0 if s.get("new_complete") else 1.0,
                                         float(s.get("grams", 10**9) or 10**9)))

    base_protein = nutrients.get("protein_g", 0.0)
    base_digestible = base_protein * base_diaas if base_diaas else base_protein

    gap_labels = ", ".join(
        _usda.nutrient_label(aa)[0] + f" ({score:.2f})"
        for aa, score, _ in gaps
    )
    lines = [
        "<h2>Protein Complement Suggestions</h2>",
        f"<p><strong>Gaps:</strong> {gap_labels}</p>",
    ]

    for i, s in enumerate(general_suggs[:5], 1):
        diaas_str = f" <em>(DIAAS {s['diaas']:.2f})</em>" if s.get("diaas") else ""
        score_parts = []
        for aa, orig_score, _ in gaps[:3]:
            new_score = s["new_scores"].get(aa, orig_score)
            lbl, _ = _usda.nutrient_label(aa)
            score_parts.append(f"{lbl}: {orig_score:.2f}→{new_score:.2f}")
        dig = s["digestible_protein_added"]
        raw = s["protein_added"]
        total_dig = base_digestible + dig
        lines.append(
            f'<div class="complement-option">'
            f"<h3>Option {i}: {s['name']}{diaas_str}</h3>"
            f"<ul>"
            f"<li><strong>Add:</strong> {s['grams']}g</li>"
            f"<li><strong>Effect:</strong> {' · '.join(score_parts)}</li>"
            f"<li><strong>Adds:</strong> {dig:.1f}g digestible protein <em>(from {raw:.1f}g raw)</em></li>"
            f"<li><strong>Total bioavailable complete protein:</strong> {total_dig:.1f}g</li>"
            f"</ul></div>"
        )

    if not general_suggs:
        lines.append("<p><em>No qualifying complement options found.</em></p>")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Top-level: build_report / write_report
# ---------------------------------------------------------------------------

_RENDERERS = {
    "txt": {
        "nutrient_table":          lambda s: _render_nutrient_table_txt(
                                       s["title"], s["nutrients"], s.get("per_label", "")),
        "protein_completeness":    lambda s: _render_protein_completeness_txt(s["nutrients"]),
        "bioavailability":         lambda s: _render_bioavailability_txt(
                                       s["food_name"], s["nutrients"]),
        "ingredient_list":         lambda s: _render_ingredient_list_txt(
                                       s["title"], s["items"]),
        "recipe_bioavailability":  lambda s: _render_recipe_bioavailability_txt(
                                       s["ingredient_stats"], s["total_protein"]),
        "complement_suggestions":  lambda s: _render_complement_suggestions_txt(
                                       s["nutrients"], s.get("base_diaas")),
    },
    "md": {
        "nutrient_table":          lambda s: _render_nutrient_table_md(
                                       s["title"], s["nutrients"], s.get("per_label", "")),
        "protein_completeness":    lambda s: _render_protein_completeness_md(s["nutrients"]),
        "bioavailability":         lambda s: _render_bioavailability_md(
                                       s["food_name"], s["nutrients"]),
        "ingredient_list":         lambda s: _render_ingredient_list_md(
                                       s["title"], s["items"]),
        "recipe_bioavailability":  lambda s: _render_recipe_bioavailability_md(
                                       s["ingredient_stats"], s["total_protein"]),
        "complement_suggestions":  lambda s: _render_complement_suggestions_md(
                                       s["nutrients"], s.get("base_diaas")),
    },
    "html": {
        "nutrient_table":          lambda s: _render_nutrient_table_html(
                                       s["title"], s["nutrients"], s.get("per_label", "")),
        "protein_completeness":    lambda s: _render_protein_completeness_html(s["nutrients"]),
        "bioavailability":         lambda s: _render_bioavailability_html(
                                       s["food_name"], s["nutrients"]),
        "ingredient_list":         lambda s: _render_ingredient_list_html(
                                       s["title"], s["items"]),
        "recipe_bioavailability":  lambda s: _render_recipe_bioavailability_html(
                                       s["ingredient_stats"], s["total_protein"]),
        "complement_suggestions":  lambda s: _render_complement_suggestions_html(
                                       s["nutrients"], s.get("base_diaas")),
    },
}


def build_report(report_title: str, sections: list[dict], fmt: str) -> str:
    """
    Render a report to the given format ("txt", "md", "html").

    report_title: appears as the document header
    sections:     list of typed section dicts (see module docstring)
    fmt:          "txt", "md", or "html"
    """
    if fmt not in _RENDERERS:
        raise ValueError(f"Unknown format: {fmt!r}. Choose txt, md, or html.")

    today = date.today().isoformat()
    renderers = _RENDERERS[fmt]

    rendered_sections = []
    for section in sections:
        stype = section.get("type")
        if not isinstance(stype, str):
            continue
        renderer = renderers.get(stype)
        if renderer is None:
            continue
        content = renderer(section)
        if content:
            rendered_sections.append(content)

    if fmt == "txt":
        sep = "\n\n"
        header = (
            f"NUMA — Nutritional Analysis\n"
            f"{'=' * 40}\n"
            f"Report: {report_title}\n"
            f"Generated: {today}\n"
            f"{'=' * 40}"
        )
        return header + "\n\n" + sep.join(rendered_sections) + "\n"

    if fmt == "md":
        sep = "\n\n"
        header = (
            f"# Numa — Nutritional Analysis\n\n"
            f"**Report:** {report_title}  \n"
            f"**Generated:** {today}"
        )
        return header + "\n\n" + sep.join(rendered_sections) + "\n"

    # html
    sep = "\n\n"
    header = (
        f"<!-- Numa nutritional analysis — generated {today} -->\n"
        f'<section class="numa-report">\n'
        f"<h1>{report_title}</h1>\n"
        f"<p><em>Generated: {today}</em></p>"
    )
    body = sep.join(rendered_sections)
    return header + "\n\n" + body + "\n\n</section>\n"


def safe_title(report_title: str) -> str:
    """Return the sanitized title prefix used in filenames (no date, no extension)."""
    safe = re.sub(r"[^\w\s-]", "", report_title).strip()
    safe = re.sub(r"[\s]+", "_", safe)
    return safe[:60]


def default_filename(report_title: str, fmt: str) -> str:
    """Suggest a filename for the report."""
    today = date.today().isoformat()
    return f"{safe_title(report_title)}_{today}.{fmt}"


def write_report(path: pathlib.Path, content: str) -> None:
    """Write content to path, creating parent directories as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
