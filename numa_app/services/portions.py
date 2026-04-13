import json
import re

import usda as _usda
from .. import state
from ..ui.prompts import Cancelled, ReturnToMain, _prompt

_UNIT_TO_GRAMS: dict[str, float] = {
    "g": 1.0, "gr": 1.0, "gram": 1.0, "grams": 1.0,
    "oz": 28.3495, "ounce": 28.3495, "ounces": 28.3495,
    "lb": 453.592, "lbs": 453.592, "pound": 453.592, "pounds": 453.592,
    "kg": 1000.0, "kilogram": 1000.0, "kilograms": 1000.0,
}

_VOLUME_TO_ML: dict[str, float] = {
    "c": 236.6, "cup": 236.6, "cups": 236.6,
    "T": 14.8, "tbsp": 14.8, "tablespoon": 14.8, "tablespoons": 14.8,
    "t": 4.9, "tsp": 4.9, "teaspoon": 4.9, "teaspoons": 4.9,
    "ml": 1.0, "milliliter": 1.0, "milliliters": 1.0, "cc": 1.0,
    "floz": 29.6,
    "l": 1000.0, "liter": 1000.0, "liters": 1000.0,
}


def _parse_number_tokens(parts: list[str]) -> tuple[float, int] | None:
    """
    Parse a number (plain float, fraction, or mixed number) from the front of a
    token list.  Returns (value, tokens_consumed) or None on failure.
    Examples: ["150"] → (150.0, 1), ["1/8"] → (0.125, 1),
              ["1", "1/2"] → (1.5, 2).
    """
    if not parts:
        return None
    p0 = parts[0]
    if "/" in p0:
        try:
            num, den = p0.split("/", 1)
            return float(num) / float(den), 1
        except (ValueError, ZeroDivisionError):
            return None
    try:
        whole = float(p0)
    except ValueError:
        return None
    # Mixed number: whole part followed by a fraction token (e.g. "1" "1/2")
    if len(parts) > 1 and "/" in parts[1] and not parts[1].startswith("p"):
        try:
            num, den = parts[1].split("/", 1)
            frac = float(num) / float(den)
            return whole + frac, 2
        except (ValueError, ZeroDivisionError):
            pass
    return whole, 1


_FRAC_MAP: list[tuple[float, str]] = [
    (1/8, "1/8"), (1/6, "1/6"), (1/5, "1/5"), (1/4, "1/4"),
    (1/3, "1/3"), (3/8, "3/8"), (2/5, "2/5"), (1/2, "1/2"),
    (3/5, "3/5"), (5/8, "5/8"), (2/3, "2/3"), (3/4, "3/4"),
    (4/5, "4/5"), (7/8, "7/8"),
]


def _nice_fraction(val: float) -> str:
    """Format a positive float as a nice fraction, whole number, or g-format."""
    whole = int(val)
    frac = val - whole
    if abs(frac) < 0.02:
        return str(whole)
    for f_val, f_label in _FRAC_MAP:
        if abs(frac - f_val) < 0.02:
            return f"{whole} {f_label}" if whole > 0 else f_label
    return f"{val:g}"


def _normalize_unit_display(label: str) -> str:
    """Normalize stored labels: convert decimal volume measures to compound units,
    and replace other bare decimal fractions with nice fraction strings."""
    _ML_PER = {"c": 236.588, "T": 14.787, "t": 4.929}

    def _replace_vol(m: re.Match) -> str:
        num = float(m.group(1))
        unit = m.group(2)
        return _volume_label(num * _ML_PER[unit])

    def _replace_bare(m: re.Match) -> str:
        return _nice_fraction(float(m.group(0)))

    # First pass: replace decimal+unit combos (e.g. "1.56147 c") with compound labels
    result = re.sub(r'(\d+\.\d+)\s*(c|T|t)\b', _replace_vol, label)
    # Second pass: replace any remaining bare decimals with nice fractions
    return re.sub(r'\d+\.\d+', _replace_bare, result)


def _volume_label(ml: float) -> str:
    """Return a human-friendly volume string, using compound units where helpful.

    Examples: 78.8 ml → "1/3 c", 34.5 ml → "2 T + 1 t", 4.9 ml → "1 t"
    """
    def _nice(s: str) -> bool:
        return '.' not in s

    # cups territory (>= 1/4 cup)
    if ml >= 59.15:
        s = _nice_fraction(ml / 236.6)
        if _nice(s):
            return f"{s} c"
        # try whole cups + tablespoon remainder
        whole_c = int(ml / 236.6)
        rem = ml - whole_c * 236.6
        prefix = f"{whole_c} c + " if whole_c else ""
        if rem >= 7.4:
            ts = _nice_fraction(rem / 14.8)
            if _nice(ts):
                return f"{prefix}{ts} T"
            # try whole T + teaspoon compound
            whole_t = int(rem / 14.8)
            t_rem = rem - whole_t * 14.8
            if whole_t > 0 and t_rem >= 2.45:
                ts2 = _nice_fraction(t_rem / 4.9)
                if _nice(ts2):
                    return f"{prefix}{whole_t} T + {ts2} t"
            # fallback: round to nearest tablespoon
            rounded_t = round(rem / 14.8)
            if rounded_t > 0:
                return f"{prefix}{rounded_t} T"
        if whole_c > 0:
            return f"{whole_c} c"
        # sub-cup but no nice tablespoon split — express as tablespoons
        return f"{round(ml / 14.8)} T"

    # tablespoon territory (>= half tablespoon)
    if ml >= 7.4:
        whole_t = int(ml / 14.8)
        rem = ml - whole_t * 14.8
        # prefer compound (e.g. "2 T + 1 t") over mixed fractions (e.g. "2 1/3 T")
        if whole_t > 0 and rem >= 2.45:
            ts = _nice_fraction(rem / 4.9)
            if _nice(ts):
                return f"{whole_t} T + {ts} t"
        s = _nice_fraction(ml / 14.8)
        if _nice(s):
            return f"{s} T"
        return f"{round(ml / 14.8)} T"

    # teaspoons
    s = _nice_fraction(ml / 4.9)
    return f"{s} t" if _nice(s) else f"{round(ml / 4.9)} t"


def _tokenize_portion(raw: str) -> list[str]:
    """Split raw input into tokens, separating any attached number+unit pairs."""
    result = []
    for p in raw.split():
        if not p.lower().startswith("p"):
            m = re.match(r'^(\d[\d./]*)\s*([A-Za-z].*)$', p)
            if m:
                result.extend([m.group(1), m.group(2)])
                continue
        result.append(p)
    return result


def _parse_portion_input(
    raw: str,
    portions: list[dict],
    food_name: str = "",
) -> tuple[float | None, str] | None:
    """
    Parse portion input.

    Returns:
      (grams, display_label)   on success — grams is the weight
      (None, vol_display)      volume recognized but density unknown; caller should ask for weight
      None                     unrecognized / bad input format

    Accepts:
      - plain number                    → grams         e.g. "150"
      - number + weight unit            → grams         e.g. "3 oz", "0.5 lb"
      - number + volume unit            → grams via density  e.g. "2 T", "1/4 cup"
      - number + vol unit + number + weight unit → explicit weight  e.g. "2 T 30g"
      - "pN"                            → USDA portion gram weight
      - "NUMBER pN"                     → multiple of USDA portion  e.g. "1.5 p1"
    """
    raw = raw.strip()
    raw_lower = raw.lower()

    # pN shortcut (bare) — case-insensitive
    if raw_lower.startswith("p") and raw_lower[1:].isdigit():
        idx = int(raw_lower[1:]) - 1
        if 0 <= idx < len(portions):
            p = portions[idx]
            return p["gram_weight"], p["description"]
        return None

    parts = _tokenize_portion(raw)
    if not parts:
        return None

    parsed = _parse_number_tokens(parts)
    if parsed is None:
        return None
    number, consumed = parsed
    remaining = parts[consumed:]

    if not remaining:
        # plain number → grams; annotate with volume if density known
        density = _usda.get_density_g_per_ml(food_name, portions)
        vol = _volume_label(number / density) if density else None
        label = f"{number:g} g ({vol})" if vol else f"{number:g} g"
        return number, label

    unit_token = remaining[0]          # original case — needed to distinguish T vs t
    unit_lower = unit_token.lower()

    # NUMBER pN  (e.g. "1.5 p1")
    if unit_lower.startswith("p") and unit_lower[1:].isdigit():
        idx = int(unit_lower[1:]) - 1
        if 0 <= idx < len(portions):
            p = portions[idx]
            grams = number * p["gram_weight"]
            return grams, f"{number:g} × {p['description']}"
        return None

    # Weight unit → grams; annotate with volume if density known
    factor = _UNIT_TO_GRAMS.get(unit_lower)
    if factor is not None:
        grams = number * factor
        density = _usda.get_density_g_per_ml(food_name, portions)
        vol = _volume_label(grams / density) if density else None
        label = f"{number:g} {unit_token} ({vol})" if vol else f"{number:g} {unit_token}"
        return grams, label

    # Volume unit — original case checked first so T≠t; fall back to lowercase
    ml_per_unit = _VOLUME_TO_ML.get(unit_token) or _VOLUME_TO_ML.get(unit_lower)
    if ml_per_unit is not None:
        # Preserve original tokens (e.g. "1/3 c" not "0.333333 c")
        vol_display = " ".join(parts[:consumed + 1])
        after_vol = remaining[1:]

        # Check for explicit weight following the volume: "2 T 30g" or "2 T 30 g"
        if after_vol:
            w_parsed = _parse_number_tokens(after_vol)
            if w_parsed is not None:
                w_number, w_consumed = w_parsed
                w_remaining = after_vol[w_consumed:]
                if not w_remaining:
                    # plain number after volume → treat as grams
                    return w_number, f"{vol_display} ({w_number:g} gr)"
                w_unit = w_remaining[0]
                w_factor = _UNIT_TO_GRAMS.get(w_unit.lower())
                if w_factor is not None:
                    grams = w_number * w_factor
                    return grams, f"{vol_display} ({w_number:g} {w_unit})"

        # No explicit weight — calculate via density if known
        density = _usda.get_density_g_per_ml(food_name, portions)
        if density is None:
            return None, vol_display
        grams = number * ml_per_unit * density
        return grams, f"{vol_display} ({grams:.0f} gr)"

    return None


def _pick_portion(food: dict, *, current: str | None = None) -> tuple[float, str, dict[str, float]] | None:
    """
    Ask the user for a portion size and return (grams, display_label, scaled_nutrients).
    USDA data is per 100g; we scale accordingly.
    current: optional display string for the existing portion (shown as a hint when editing).
    Returns None if cancelled.
    """
    portions = food.get("portions") or []

    brand = food.get("brand") or ""
    brand_str = f" ({brand})" if brand else ""
    state.console.print(f"\n  Food: [{state.T['hi']}]{food['name']}{brand_str}[/{state.T['hi']}]")

    state.console.print("  [dim]Enter an amount: 150 (g/gr), 3 oz, 0.5 lb, 1/4 c (cup), 2 T (tbsp), 1 t (tsp) — or skip[/dim]")
    if current:
        state.console.print(
            f"  Current: [{state.T['default_hint']}]{current}[/{state.T['default_hint']}]"
        )

    food_name = food.get("name", "")
    while True:
        try:
            raw = _prompt("Portion amount  (Enter=skip, b=back, m=main, q=quit)", free_text=True).strip()
        except Cancelled:
            return None
        if raw.lower() == "m":
            raise ReturnToMain()
        if raw.lower() == "b":
            return None
        if raw.lower() == "q":
            raise SystemExit(0)
        if not raw:
            return 0.0, "—", {}

        result = _parse_portion_input(raw, portions, food_name=food_name)
        if result is None:
            state.console.print(f"[{state.T['warning']}]Unrecognized input. "
                          f"Try: 150, 65 gr, 3 oz, 1/4 cup, 2 T, or p1.[/{state.T['warning']}]")
            continue

        grams, label = result
        if grams is None:
            # Volume recognized but density unknown — ask for weight to enable nutrition calc
            vol_display = label
            state.console.print(f"  [dim]Weight per volume is unknown for this food. "
                          f"Enter grams to calculate nutrition, or press Enter to skip.[/dim]")
            try:
                w_raw = _prompt(f"Weight of {vol_display} in grams  (Enter=skip)", free_text=True).strip()
            except Cancelled:
                w_raw = ""
            if w_raw.lower() == "q":
                raise SystemExit(0)
            if w_raw and w_raw.lower() != "b":
                try:
                    grams = float(w_raw)
                    label = f"{vol_display} ({grams:.0f} gr)"
                except ValueError:
                    pass
            if grams is None:
                grams = 0.0
                label = f"{vol_display} (weight not known)"

        scaled = _usda.scale_nutrients(food["nutrients"], grams, base_size=100.0)
        return grams, label, scaled
