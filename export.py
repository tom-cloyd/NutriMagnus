"""
export.py — Render numa nutrient reports to plain text, markdown, or HTML fragment.

Each report is a list of typed section dicts:
  {"type": "nutrient_table",       "title": str, "nutrients": dict, "per_label": str}
  {"type": "protein_completeness", "nutrients": dict}
  {"type": "bioavailability",      "food_name": str, "nutrients": dict}
  {"type": "ingredient_list",      "title": str, "items": list[dict]}
    item keys: food_name, amount, unit

Formats: "txt", "md", "html"
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
# Top-level: build_report / write_report
# ---------------------------------------------------------------------------

_RENDERERS = {
    "txt": {
        "nutrient_table":       lambda s: _render_nutrient_table_txt(
                                    s["title"], s["nutrients"], s.get("per_label", "")),
        "protein_completeness": lambda s: _render_protein_completeness_txt(s["nutrients"]),
        "bioavailability":      lambda s: _render_bioavailability_txt(
                                    s["food_name"], s["nutrients"]),
        "ingredient_list":      lambda s: _render_ingredient_list_txt(
                                    s["title"], s["items"]),
    },
    "md": {
        "nutrient_table":       lambda s: _render_nutrient_table_md(
                                    s["title"], s["nutrients"], s.get("per_label", "")),
        "protein_completeness": lambda s: _render_protein_completeness_md(s["nutrients"]),
        "bioavailability":      lambda s: _render_bioavailability_md(
                                    s["food_name"], s["nutrients"]),
        "ingredient_list":      lambda s: _render_ingredient_list_md(
                                    s["title"], s["items"]),
    },
    "html": {
        "nutrient_table":       lambda s: _render_nutrient_table_html(
                                    s["title"], s["nutrients"], s.get("per_label", "")),
        "protein_completeness": lambda s: _render_protein_completeness_html(s["nutrients"]),
        "bioavailability":      lambda s: _render_bioavailability_html(
                                    s["food_name"], s["nutrients"]),
        "ingredient_list":      lambda s: _render_ingredient_list_html(
                                    s["title"], s["items"]),
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
