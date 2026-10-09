"""
entry_parse.py — tolerant reading of what people type into NuMa's forms.

One rule throughout: anything NuMa can read, it reads (and says when it
converted something); anything it can't, it says so. Nothing typed is ever
silently dropped. Before this module, the custom-food form threw away any
value that wasn't a bare number — "400 IU", "1,200", "12 mg" all vanished
without a word, and the browser's number boxes wouldn't take them anyway.

- parse_number(): "1,200", "12,5", "1 1/2", "½", "1½", ".5"
- parse_nutrient(): a number, optionally with a unit, converted to the
  field's own unit — g / mg / mcg (µg, ug), IU for vitamins A, D and E,
  kJ for calories; "trace" counts as 0, "n/a" / "-" as blank.
- parse_aa_block(): a pasted amino acid table ("Lysine 5.2" per line, any
  common separator), converted to g per 100 g food.
- COUNT_UNITS / supplement_portion(): the per-tablet "supplement mode".

Docs: README-numa-documentation.md, Architecture: "numa_app/services/entry_parse.py";
user-manual.md #data-entry
"""
from __future__ import annotations

import re

_UNICODE_FRACTIONS = {
    "½": "1/2", "⅓": "1/3", "⅔": "2/3", "¼": "1/4", "¾": "3/4", "⅕": "1/5",
    "⅖": "2/5", "⅗": "3/5", "⅘": "4/5", "⅙": "1/6", "⅚": "5/6", "⅛": "1/8",
    "⅜": "3/8", "⅝": "5/8", "⅞": "7/8",
}
_BLANK_WORDS = {"", "-", "—", "–", "n/a", "na", "nd", "none", "?"}
_TRACE_WORDS = {"trace", "tr", "traces"}

# Mass units, in grams.
_MASS_G = {"g": 1.0, "gr": 1.0, "gram": 1.0, "grams": 1.0,
           "mg": 1e-3, "milligram": 1e-3, "milligrams": 1e-3,
           "mcg": 1e-6, "µg": 1e-6, "μg": 1e-6, "ug": 1e-6, "microgram": 1e-6, "micrograms": 1e-6}
_FIELD_UNIT_G = {"g": 1.0, "mg": 1e-3, "mcg": 1e-6}

# IU -> the field's own unit. Vitamin A as retinol (RAE), D as D3/D2, E as
# natural d-alpha-tocopherol — the forms supplement labels almost always mean.
IU_FACTORS = {
    "vitamin_a_mcg": 0.3,
    "vitamin_d_mcg": 0.025,
    "vitamin_e_mg":  0.67,
}

# Units a supplement is counted in. A food whose serving is "1 <one of these>"
# is in supplement mode: its per-100 g values are the label's per-unit values.
COUNT_UNITS = {"tablet", "capsule", "softgel", "pill", "gummy", "lozenge", "chew",
               "scoop", "packet", "sachet", "drop", "wafer", "caplet", "vegcap"}


class EntryError(ValueError):
    """A value that can't be read. str(err) is a sentence for the person."""


def normalize(raw) -> str:
    """Unicode fractions spelled out ("1½" -> "1 1/2"), odd spaces made plain."""
    s = str(raw if raw is not None else "").replace(" ", " ").replace(" ", " ").strip()
    for ch, frac in _UNICODE_FRACTIONS.items():
        s = re.sub(rf"(\d){ch}", rf"\1 {frac}", s)
        s = s.replace(ch, frac)
    s = s.replace("⁄", "/")
    return re.sub(r"\s+", " ", s)


def parse_number(raw) -> float:
    """A typed number. Accepts thousands commas ("1,200"), a decimal comma
    ("12,5"), fractions and mixed numbers ("1/2", "1 1/2"), "½"."""
    s = normalize(raw)
    if not s:
        raise EntryError("Nothing was entered.")
    if re.fullmatch(r"\d{1,3}(,\d{3})+(\.\d+)?", s):
        s = s.replace(",", "")
    elif re.fullmatch(r"\d+,\d+", s):
        s = s.replace(",", ".")
    m = re.fullmatch(r"(\d+) (\d+)/(\d+)", s)
    if m:
        den = float(m.group(3))
        if den == 0:
            raise EntryError(f'"{raw}" divides by zero.')
        return float(m.group(1)) + float(m.group(2)) / den
    m = re.fullmatch(r"(\d+(?:\.\d+)?)/(\d+(?:\.\d+)?)", s)
    if m:
        den = float(m.group(2))
        if den == 0:
            raise EntryError(f'"{raw}" divides by zero.')
        return float(m.group(1)) / den
    try:
        return float(s)
    except ValueError:
        raise EntryError(f'"{raw}" isn\'t a number NuMa can read.') from None


def field_unit(key: str) -> str:
    """The unit a nutrient key is stored in: "g", "mg", "mcg" or "kcal"."""
    if key == "calories":
        return "kcal"
    for suffix in ("_mcg", "_mg", "_g"):
        if key.endswith(suffix):
            return suffix[1:]
    return ""


def parse_nutrient(key: str, raw, label: str = "") -> tuple[float | None, str | None]:
    """Read one nutrient field. Returns (value in the field's unit, or None
    for blank; a note when something was converted, else None). Raises
    EntryError with a plain-language reason when it can't be read."""
    name = label or key
    s = normalize(raw)
    low = s.lower()
    if low in _BLANK_WORDS:
        return None, None
    if low in _TRACE_WORDS:
        return 0.0, f"{name}: \"{s}\" counted as 0"
    if s.startswith("<"):
        raise EntryError(f"{name}: \"{s}\" is a limit, not an amount. Enter 0, or the figure itself.")
    if "%" in s:
        raise EntryError(f"{name}: \"{s}\" is a percent of daily value, which can't be turned into an "
                         f"amount reliably. Enter the amount from the label instead.")
    if not re.search(r"\d", s):
        raise EntryError(f'{name}: "{s}" has no number.')
    m = re.fullmatch(r"(.+?)\s*([a-zA-Zµμ]+(?:\s*RAE)?)\.?", s)
    number_text, unit_text = (m.group(1), m.group(2)) if m and re.search(r"\d", m.group(1)) else (s, "")
    try:
        value = parse_number(number_text)
    except EntryError:
        raise EntryError(f'{name}: "{s}" isn\'t an amount NuMa can read.') from None
    if value < 0:
        raise EntryError(f"{name}: {s} is negative.")
    unit = unit_text.strip().replace(" RAE", "").replace("RAE", "").strip()
    unit_low = unit.lower()
    target = field_unit(key)
    if not unit:
        return value, None
    if unit_low == "iu":
        factor = IU_FACTORS.get(key)
        if factor is None:
            raise EntryError(f"{name}: IU can only be converted for vitamins A, D and E. "
                             f"Enter {name.lower()} in {target}.")
        out = round(value * factor, 4)
        return out, f"{name}: {value:g} IU = {out:g} {target}"
    if target == "kcal":
        if unit_low in ("kcal", "cal", "calories", "calorie"):
            return value, None
        if unit_low == "kj":
            out = round(value / 4.184, 1)
            return out, f"{name}: {value:g} kJ = {out:g} kcal"
        raise EntryError(f'{name}: "{unit}" isn\'t an energy unit. Use kcal or kJ.')
    if unit_low in _MASS_G and target in _FIELD_UNIT_G:
        if _MASS_G[unit_low] == _FIELD_UNIT_G[target]:
            return value, None
        out = round(value * _MASS_G[unit_low] / _FIELD_UNIT_G[target], 6)
        return out, f"{name}: {value:g} {unit} = {out:g} {target}"
    raise EntryError(f'{name}: "{unit}" isn\'t a unit NuMa knows here. Enter it in {target}.')


# ── Pasted amino acid tables ──────────────────────────────────────────────

AA_NAMES = {
    "tryptophan": "aa_tryptophan_g", "trp": "aa_tryptophan_g",
    "threonine": "aa_threonine_g", "thr": "aa_threonine_g",
    "isoleucine": "aa_isoleucine_g", "ile": "aa_isoleucine_g",
    "leucine": "aa_leucine_g", "leu": "aa_leucine_g",
    "lysine": "aa_lysine_g", "lys": "aa_lysine_g",
    "methionine": "aa_methionine_g", "met": "aa_methionine_g",
    "cystine": "aa_cystine_g", "cysteine": "aa_cystine_g", "cys": "aa_cystine_g",
    "phenylalanine": "aa_phenylalanine_g", "phe": "aa_phenylalanine_g",
    "tyrosine": "aa_tyrosine_g", "tyr": "aa_tyrosine_g",
    "valine": "aa_valine_g", "val": "aa_valine_g",
    "histidine": "aa_histidine_g", "his": "aa_histidine_g",
}
# Amino acids NuMa doesn't track — named as skipped, not as errors.
AA_UNTRACKED = {"arginine", "arg", "alanine", "ala", "aspartic acid", "asp", "glutamic acid",
                "glu", "glycine", "gly", "proline", "pro", "serine", "ser", "hydroxyproline",
                "asparagine", "glutamine", "aspartate", "glutamate"}
# How the pasted figures are expressed -> label.
AA_BLOCK_UNITS = {
    "g_per_100g_food":    "g per 100 g of food",
    "mg_per_100g_food":   "mg per 100 g of food",
    "g_per_100g_protein": "g per 100 g of protein (same as % of protein)",
    "mg_per_g_protein":   "mg per g of protein",
}


def parse_aa_block(text: str, unit: str, protein_g: float | None) -> tuple[dict, list[str], list[str]]:
    """Read a pasted amino acid table: one amino acid per line, its name then
    its figure ("Lysine 5.2", "Lysine: 5.2", "Lysine\t5.2 g"). Returns
    (values in g per 100 g food, notes, errors). Per-protein figures need the
    food's protein per 100 g; without it they're an error, not a guess."""
    values: dict[str, float] = {}
    notes: list[str] = []
    errors: list[str] = []
    if unit not in AA_BLOCK_UNITS:
        return {}, [], ["Choose what the pasted figures are measured in."]
    per_protein = unit in ("g_per_100g_protein", "mg_per_g_protein")
    if per_protein and not protein_g:
        return {}, [], ["Per-protein amino acid figures need the food's protein per 100 g. "
                        "Enter Protein first, then paste again."]
    skipped: list[str] = []
    for line_no, line in enumerate(normalize_lines(text), 1):
        m = re.match(r"([A-Za-z][A-Za-z +\-]*?)\s*[:=\t,;]?\s*(\d[\d.,/ ]*)\s*([a-zA-Z%]*)\s*$", line)
        if not m:
            errors.append(f'Line {line_no}, "{line}": expected a name and a number.')
            continue
        name = m.group(1).strip().lower().rstrip(" -")
        name = re.sub(r"^l-", "", name)
        key = AA_NAMES.get(name)
        if key is None:
            if name in AA_UNTRACKED:
                skipped.append(m.group(1).strip())
            else:
                errors.append(f'Line {line_no}, "{line}": "{m.group(1).strip()}" isn\'t an amino acid NuMa knows.')
            continue
        try:
            v = parse_number(m.group(2).strip())
        except EntryError as e:
            errors.append(f"Line {line_no}: {e}")
            continue
        if unit == "g_per_100g_food":
            g = v
        elif unit == "mg_per_100g_food":
            g = v / 1000.0
        elif unit == "g_per_100g_protein":
            g = v * protein_g / 100.0
        else:  # mg per g protein
            g = v * protein_g / 1000.0
        if key in values:
            errors.append(f'Line {line_no}: {m.group(1).strip()} appears twice.')
            continue
        values[key] = round(g, 4)
    if per_protein and values:
        notes.append(f"Amino acids converted from {AA_BLOCK_UNITS[unit]} using "
                     f"{protein_g:g} g protein per 100 g.")
    if skipped:
        notes.append("Not tracked by NuMa, so left out: " + ", ".join(skipped) + ".")
    return values, notes, errors


def normalize_lines(text: str) -> list[str]:
    return [normalize(l) for l in str(text or "").splitlines() if normalize(l)]


def supplement_portion(serving_size, serving_unit) -> dict | None:
    """The portion that makes "1 tablet" (etc.) work: for a food whose serving
    is exactly 1 of a count unit, {"description": "1 tablet", "gram_weight":
    100.0} — the food's per-100 g values are the label's per-tablet values."""
    unit = (serving_unit or "").strip().lower()
    unit = unit[:-1] if unit.endswith("s") and unit[:-1] in COUNT_UNITS else unit
    if unit in COUNT_UNITS and serving_size is not None and float(serving_size) == 1.0:
        return {"description": f"1 {unit}", "gram_weight": 100.0}
    return None
