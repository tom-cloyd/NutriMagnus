"""
rda_status.py — shared RDA/limit percent-of-target classification, used by
CLI (render.py) and web (backend.py) to color-code nutrient rows. web
previously used its own thresholds (70% vs the CLI's 75% warning cutoff for
minimum/target nutrients; no "approaching limit" tier at all for limit-type
nutrients between 80-100%), so the same data could show a different colored
verdict depending on which UI displayed it.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/rda_status.py — RDA status classification"
"""


def rda_status(pct: float, rda_type: str) -> str:
    """Classify a percent-of-target value into a status tier.

    rda_type == "limit" (Tolerable Upper Intake Level): "met" (<=80%),
    "near" (80-100%, approaching the limit), "over" (>100%).
    Otherwise (RDA / Adequate Intake minimum or target): "met" (>=100%),
    "near" (70-99%), "low" (<70%).
    """
    if rda_type == "limit":
        if pct <= 80:
            return "met"
        elif pct <= 100:
            return "near"
        return "over"
    if pct >= 100:
        return "met"
    elif pct >= 70:
        return "near"
    return "low"


def limit_warning(day_total: float, limit: float) -> bool:
    """True when a day's total is within 10% of a user-defined max limit (or over it).

    Independent of rda_status's built-in "limit" tier (e.g. sodium's Tolerable
    Upper Intake Level) — this checks a separate, user-configured per-nutrient cap.
    """
    return limit > 0 and day_total >= limit * 0.9
