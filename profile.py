"""
profile.py — User profile and personalized RDA computation for numa.

Profiles are stored in ~/.config/numa/profiles/{name}.json.
The active profile name is recorded in ~/.config/numa/active_profile.txt.
Legacy single-profile installs (profile.json) are migrated automatically to
profiles/Default.json on first run.
RDA targets follow the 2020-2025 USDA Dietary Guidelines and NIH/Institute
of Medicine Dietary Reference Intakes (DRIs).
Docs: README-numa-documentation.md, Architecture: "profile.py — User profile and RDA"
"""

from __future__ import annotations

import json
import pathlib
import re
from dataclasses import asdict, dataclass, field
from typing import Optional

import platform_utils as _platform_utils

_CONFIG_DIR      = _platform_utils.get_config_dir()
_LEGACY_FILE     = _CONFIG_DIR / "profile.json"
_PROFILES_DIR    = _CONFIG_DIR / "profiles"
_ACTIVE_NAME_FILE = _CONFIG_DIR / "active_profile.txt"

# Activity level keys → Mifflin-St Jeor multipliers
ACTIVITY_LEVELS: dict[str, float] = {
    "sedentary":   1.2,
    "light":       1.375,
    "moderate":    1.55,
    "active":      1.725,
    "very_active": 1.9,
}

ACTIVITY_LABELS: dict[str, str] = {
    "sedentary":   "Sedentary (desk job, little exercise)",
    "light":       "Lightly active (1–3 days/week)",
    "moderate":    "Moderately active (3–5 days/week)",
    "active":      "Very active (6–7 days/week)",
    "very_active": "Extra active (daily + physical job)",
}

SEX_VALUES: tuple[str, ...] = ("male", "female", "other")


@dataclass
class UserProfile:
    age: int
    sex: str           # "male", "female", or "other"
    weight_kg: float
    height_cm: float
    activity_level: str  # key from ACTIVITY_LEVELS
    weight_unit: str = "kg"        # "kg" or "lb" — controls display
    height_unit: str = "cm"        # "cm" or "imperial" — controls display
    name: str = "Default"          # profile display name; also used as filename stem
    use_oxalate_data: bool = False  # enable Harvard oxalate data lookup for foods
    optimal_targets: dict = field(default_factory=dict)  # nutrient_key -> per-day target, native unit
    max_limits: dict = field(default_factory=dict)       # nutrient_key -> per-day cap, native unit


# ---------------------------------------------------------------------------
# Unit conversion helpers
# ---------------------------------------------------------------------------

def lb_to_kg(lb: float) -> float:
    return lb / 2.20462


def kg_to_lb(kg: float) -> float:
    return kg * 2.20462


def ftin_to_cm(feet: float, inches: float) -> float:
    return (feet * 12.0 + inches) * 2.54


def cm_to_ftin(cm: float) -> tuple[int, float]:
    """Return (whole_feet, decimal_inches) for a cm value."""
    total_inches = cm / 2.54
    feet = int(total_inches // 12)
    inches = total_inches % 12
    return feet, inches


def format_weight(kg: float, unit: str) -> str:
    """Format weight showing preferred unit plus metric in parentheses."""
    if unit == "lb":
        return f"{kg_to_lb(kg):.1f} lb  ({kg:.1f} kg)"
    return f"{kg:.1f} kg"


def format_height(cm: float, unit: str) -> str:
    """Format height showing preferred unit plus metric in parentheses."""
    if unit == "imperial":
        feet, inches = cm_to_ftin(cm)
        return f"{feet}'{inches:.0f}\"  ({cm:.1f} cm)"
    return f"{cm:.1f} cm"


# ---------------------------------------------------------------------------
# Input parsers
# ---------------------------------------------------------------------------

def parse_weight(text: str) -> tuple[Optional[float], str]:
    """
    Parse a weight string. Returns (kg, unit) where unit is "lb" or "kg".
    Returns (None, "") if the input cannot be parsed.

    Accepted formats:
      "80"          → 80.0 kg
      "80 kg"       → 80.0 kg
      "176 lbs"     → 176 / 2.20462 kg, unit "lb"
      "176.4 lb"    → same
      "176 pounds"  → same
    """
    text = text.strip()
    if not text:
        return None, ""
    # Pounds: number + lb/lbs/pound/pounds
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(?:lbs?|pounds?)$", text, re.IGNORECASE)
    if m:
        return lb_to_kg(float(m.group(1))), "lb"
    # Kilograms: number + optional kg
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(?:kg)?$", text, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        return val, "kg"
    return None, ""


def parse_height(text: str) -> tuple[Optional[float], str]:
    """
    Parse a height string. Returns (cm, unit) where unit is "imperial" or "cm".
    Returns (None, "") if the input cannot be parsed.

    Accepted formats (imperial):
      "5'10\""    5 feet 10 inches
      "5'10"      same, no trailing quote
      "5 10"      same, space-separated
      "5ft 10in"  same, word units
      "5ft10"     same, no space
      "6'"        6 feet exactly
      "6ft"       same

    Accepted formats (metric):
      "178"       178 cm
      "178.5"     178.5 cm
      "178 cm"    same
    """
    text = text.strip()
    if not text:
        return None, ""

    # Feet + inches: 5'10", 5'10, 5 10, 5ft10in, 5ft 10, etc.
    ftin_patterns = [
        # 5'10" or 5'10 (quote then digits, optional trailing quote)
        r"""^(\d+)\s*[''′]\s*(\d+(?:\.\d+)?)\s*[""″]?$""",
        # 5 ft 10 in / 5ft10in / 5feet10inches
        r"^(\d+)\s*(?:ft|feet|foot)\s*(\d+(?:\.\d+)?)\s*(?:in|inch|inches)?$",
        # bare "5 10" — two plain integers (ambiguous but common)
        r"^(\d{1,1})\s+(\d{1,2})$",
    ]
    for pattern in ftin_patterns:
        m = re.match(pattern, text, re.IGNORECASE)
        if m:
            feet, inches = float(m.group(1)), float(m.group(2))
            # Sanity: feet 3–8, inches 0–11
            if 3 <= feet <= 8 and 0 <= inches <= 11:
                return ftin_to_cm(feet, inches), "imperial"

    # Feet only: 6', 6ft, 6feet
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(?:ft|feet|foot|[''′])$", text, re.IGNORECASE)
    if m:
        feet = float(m.group(1))
        if 3 <= feet <= 8:
            return ftin_to_cm(feet, 0), "imperial"

    # Metric: number + optional "cm"
    m = re.match(r"^(\d+(?:\.\d+)?)\s*(?:cm)?$", text, re.IGNORECASE)
    if m:
        val = float(m.group(1))
        return val, "cm"

    return None, ""


# ---------------------------------------------------------------------------
# Profile I/O — multi-profile support
# ---------------------------------------------------------------------------

def _migrate_legacy() -> None:
    """One-time migration: move old profile.json → profiles/Default.json."""
    if not _LEGACY_FILE.exists():
        return
    _PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    dest = _PROFILES_DIR / "Default.json"
    if not dest.exists():
        try:
            data = json.loads(_LEGACY_FILE.read_text())
            data.setdefault("name", "Default")
            dest.write_text(json.dumps(data, indent=2) + "\n")
        except Exception:
            return
    _LEGACY_FILE.rename(_LEGACY_FILE.parent / "profile.json.bak")


def list_profiles() -> list[str]:
    """Return sorted list of profile names (stems of *.json files in profiles dir)."""
    _migrate_legacy()
    if not _PROFILES_DIR.exists():
        return []
    return sorted(p.stem for p in _PROFILES_DIR.glob("*.json"))


def get_active_profile_name() -> str:
    """Return the active profile name, falling back to first available or 'Default'."""
    _migrate_legacy()
    if _ACTIVE_NAME_FILE.exists():
        name = _ACTIVE_NAME_FILE.read_text().strip()
        if name and (_PROFILES_DIR / f"{name}.json").exists():
            return name
    names = list_profiles()
    return names[0] if names else "Default"


def set_active_profile_name(name: str) -> None:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _ACTIVE_NAME_FILE.write_text(name + "\n")


def load_profile(name: str | None = None) -> Optional[UserProfile]:
    """Load a named profile (or the active profile if name is None).
    Returns None if no profiles exist or the named profile is not found."""
    _migrate_legacy()
    if name is None:
        name = get_active_profile_name()
    path = _PROFILES_DIR / f"{name}.json"
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        return UserProfile(
            age=int(data["age"]),
            sex=str(data["sex"]),
            weight_kg=float(data["weight_kg"]),
            height_cm=float(data["height_cm"]),
            activity_level=str(data["activity_level"]),
            weight_unit=str(data.get("weight_unit", "kg")),
            height_unit=str(data.get("height_unit", "cm")),
            name=str(data.get("name", name)),
            use_oxalate_data=bool(data.get("use_oxalate_data", False)),
            optimal_targets=dict(data.get("optimal_targets") or {}),
            max_limits=dict(data.get("max_limits") or {}),
        )
    except (KeyError, ValueError, json.JSONDecodeError):
        return None


def save_profile(profile: UserProfile) -> None:
    """Save profile to profiles/{profile.name}.json and update active pointer."""
    _PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    path = _PROFILES_DIR / f"{profile.name}.json"
    path.write_text(json.dumps(asdict(profile), indent=2) + "\n")


def delete_profile(name: str) -> bool:
    """Delete a profile by name. Returns True if it existed."""
    path = _PROFILES_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def rename_profile(old_name: str, new_name: str) -> bool:
    """Rename a profile file and update the active pointer if needed.
    Returns False if old_name doesn't exist or new_name is already taken."""
    old_path = _PROFILES_DIR / f"{old_name}.json"
    new_path = _PROFILES_DIR / f"{new_name}.json"
    if not old_path.exists() or new_path.exists():
        return False
    data = json.loads(old_path.read_text())
    data["name"] = new_name
    new_path.write_text(json.dumps(data, indent=2) + "\n")
    old_path.unlink()
    if get_active_profile_name() == old_name:
        set_active_profile_name(new_name)
    return True


# Keep for any callers that used the old single-file path
def get_profile_file() -> pathlib.Path:
    return _PROFILES_DIR / f"{get_active_profile_name()}.json"


# ---------------------------------------------------------------------------
# BMR and RDA
# ---------------------------------------------------------------------------

def bmr(profile: UserProfile) -> float:
    """Mifflin-St Jeor basal metabolic rate in kcal/day."""
    base = 10.0 * profile.weight_kg + 6.25 * profile.height_cm - 5.0 * profile.age
    if profile.sex == "male":
        return base + 5.0
    elif profile.sex == "female":
        return base - 161.0
    else:
        # "other": midpoint of male (+5) and female (-161)
        return base - 78.0


# IOM/NIH ODS-cited bioavailability adjustments for diets without heme iron
# (meat/fish/poultry) or with phytate-heavy staples that inhibit zinc
# absorption. Applied as a multiplier on the RDA itself — the standard way
# this guidance is expressed (e.g. "vegetarians may need up to 1.8x the iron
# RDA of non-vegetarians"), not as a discount on measured intake. "all" gets
# no adjustment; "vegetarian" and "plant_only" share the same multipliers —
# lacto-ovo vegetarians still lack heme iron, and legumes/grains (the shared
# staple across both patterns) are the primary source of the phytate effect
# on zinc, not meat's absence specifically.
# Sources: IOM (2001) DRI report for iron/zinc; NIH ODS Iron and Zinc Health
# Professional Fact Sheets — see user-manual.md Notes [^4][^5][^6].
_DIET_AWARE_RDA_MULTIPLIERS: dict[str, dict[str, float]] = {
    "vegetarian": {"iron_mg": 1.8, "zinc_mg": 1.5},
    "plant_only": {"iron_mg": 1.8, "zinc_mg": 1.5},
}


def compute_rda(profile: UserProfile, diet_pref: str = "all") -> dict[str, tuple[float, str, str]]:
    """
    Compute personalized Dietary Reference Intake targets from a UserProfile.

    Returns a dict mapping nutrient_key → (value, unit, rda_type) where
    rda_type is one of:
      "target"  — recommended intake (currently just calories)
      "minimum" — Recommended Dietary Allowance or Adequate Intake (includes
                  carbs_g, whose 130 g/day is the brain's minimum glucose
                  requirement — a genuine floor, not a target to hit exactly)
      "limit"   — tolerable upper intake / daily limit

    "minimum" here means the DRI/RDA sense of the word: the daily amount
    that meets the needs of ~97-98% of healthy people in that age/sex group
    (NIH Office of Dietary Supplements) — not a bare-survival floor. See
    manual topic ?rda for the full definition and citation shown to users.

    Only nutrients tracked in usda.NUTRIENT_MAP are included.
    Amino acids and phytonutrients without established DRIs are excluded.

    `diet_pref` ("all" | "vegetarian" | "plant_only", default "all") bumps
    the iron and zinc RDA to reflect reduced dietary bioavailability on
    vegetarian/plant-based patterns — see _DIET_AWARE_RDA_MULTIPLIERS and
    manual topic ?diet-bioavailability. This is the same preference value used
    elsewhere for complement-suggestion filtering (stored in the web app's
    prefs file); callers pass it through explicitly since profile.py itself
    has no dependency on app state.

    Sources: NIH Office of Dietary Supplements; USDA 2020-2025 Dietary
    Guidelines; Institute of Medicine Dietary Reference Intakes.
    """
    age = profile.age
    sex = profile.sex
    male = sex == "male"
    female = sex == "female"
    # "other" uses the midpoint of male and female values where they differ

    activity_factor = ACTIVITY_LEVELS.get(profile.activity_level, 1.55)
    calories = round(bmr(profile) * activity_factor)

    # Protein: RDA 0.8 g/kg for sedentary; higher for active individuals
    if profile.activity_level in ("active", "very_active"):
        protein_g_per_kg = 1.2
    elif profile.activity_level == "moderate":
        protein_g_per_kg = 1.0
    else:
        protein_g_per_kg = 0.8
    protein_g = round(protein_g_per_kg * profile.weight_kg, 1)

    # Fiber (AI): 38g men, 25g women; after 50: 30g men, 21g women
    if male:
        fiber_g = 30.0 if age >= 50 else 38.0
    elif female:
        fiber_g = 21.0 if age >= 50 else 25.0
    else:
        fiber_g = 25.5 if age >= 50 else 31.5

    # Calcium (RDA)
    if male:
        calcium_mg = 1200.0 if age >= 70 else 1000.0
    elif female:
        calcium_mg = 1200.0 if age >= 51 else 1000.0
    else:
        calcium_mg = 1200.0 if age >= 60 else 1000.0

    # Iron (RDA): 8mg men; 18mg premenopausal women; 8mg post-menopausal
    if male:
        iron_mg = 8.0
    elif female:
        iron_mg = 8.0 if age >= 51 else 18.0
    else:
        iron_mg = 8.0 if age >= 51 else 13.0

    # Magnesium (RDA)
    if male:
        magnesium_mg = 420.0 if age >= 31 else 400.0
    elif female:
        magnesium_mg = 320.0 if age >= 31 else 310.0
    else:
        magnesium_mg = 370.0 if age >= 31 else 355.0

    # Potassium (AI)
    potassium_mg = 3400.0 if male else 2600.0 if female else 3000.0

    # Zinc (RDA)
    zinc_mg = 11.0 if male else 8.0 if female else 9.5

    # Iodine (RDA): 150 mcg, adults of any sex
    iodine_mcg = 150.0

    # Selenium (RDA): 55 mcg, adults of any sex
    selenium_mcg = 55.0

    # Vitamin A (RDA, mcg RAE)
    vitamin_a_mcg = 900.0 if male else 700.0 if female else 800.0

    # Vitamin C (RDA)
    vitamin_c_mg = 90.0 if male else 75.0 if female else 82.5

    # Vitamin D (RDA): 15 mcg (<70 yrs), 20 mcg (70+)
    vitamin_d_mcg = 20.0 if age >= 70 else 15.0

    # Vitamin E (RDA)
    vitamin_e_mg = 15.0

    # Vitamin K (AI)
    vitamin_k_mcg = 120.0 if male else 90.0 if female else 105.0

    # B vitamins (RDA)
    thiamin_mg    = 1.2 if male else 1.1
    riboflavin_mg = 1.3 if male else 1.1
    niacin_mg     = 16.0 if male else 14.0

    if age >= 51:
        b6_mg = 1.7 if male else 1.5
    else:
        b6_mg = 1.3

    folate_mcg = 400.0
    b12_mcg    = 2.4

    # Choline (AI)
    choline_mg = 550.0 if male else 425.0 if female else 487.5

    # Phosphorus (RDA)
    phosphorus_mg = 700.0

    # Omega-3 ALA (AI). No official DRI exists for direct EPA/DHA intake —
    # only ALA has an established Adequate Intake. See usda docs / manual
    # topic ?omega3 for the ALA-to-EPA/DHA conversion caveat this implies,
    # especially for plant-based diets relying on ALA as their only source.
    omega3_ala_mg = 1600.0 if male else 1100.0 if female else 1350.0

    diet_multipliers = _DIET_AWARE_RDA_MULTIPLIERS.get(diet_pref, {})
    iron_mg = round(iron_mg * diet_multipliers.get("iron_mg", 1.0), 1)
    zinc_mg = round(zinc_mg * diet_multipliers.get("zinc_mg", 1.0), 1)

    return {
        # Macros
        "calories":      (float(calories), "kcal", "target"),
        "protein_g":     (protein_g,       "g",    "minimum"),
        "carbs_g":       (130.0,           "g",    "minimum"),
        "fiber_g":       (fiber_g,         "g",    "minimum"),
        "sodium_mg":     (2300.0,          "mg",   "limit"),
        "omega3_ala_mg": (omega3_ala_mg,   "mg",   "minimum"),
        # Minerals
        "calcium_mg":    (calcium_mg,      "mg",   "minimum"),
        "iron_mg":       (iron_mg,         "mg",   "minimum"),
        "magnesium_mg":  (magnesium_mg,    "mg",   "minimum"),
        "phosphorus_mg": (phosphorus_mg,   "mg",   "minimum"),
        "potassium_mg":  (potassium_mg,    "mg",   "minimum"),
        "zinc_mg":       (zinc_mg,         "mg",   "minimum"),
        "iodine_mcg":    (iodine_mcg,      "mcg",  "minimum"),
        "selenium_mcg":  (selenium_mcg,    "mcg",  "minimum"),
        # Vitamins
        "vitamin_a_mcg": (vitamin_a_mcg,   "mcg",  "minimum"),
        "vitamin_c_mg":  (vitamin_c_mg,    "mg",   "minimum"),
        "vitamin_d_mcg": (vitamin_d_mcg,   "mcg",  "minimum"),
        "vitamin_e_mg":  (vitamin_e_mg,    "mg",   "minimum"),
        "vitamin_k_mcg": (vitamin_k_mcg,   "mcg",  "minimum"),
        "thiamin_mg":    (thiamin_mg,       "mg",   "minimum"),
        "riboflavin_mg": (riboflavin_mg,   "mg",   "minimum"),
        "niacin_mg":     (niacin_mg,       "mg",   "minimum"),
        "b6_mg":         (b6_mg,           "mg",   "minimum"),
        "folate_mcg":    (folate_mcg,      "mcg",  "minimum"),
        "b12_mcg":       (b12_mcg,         "mcg",  "minimum"),
        "choline_mg":    (choline_mg,      "mg",   "minimum"),
    }


def compute_optimal(profile: UserProfile) -> dict[str, tuple[float, str, str]]:
    """
    Return personalized "optimal" targets the user has configured, in the same
    shape as compute_rda(): nutrient_key -> (value, unit, "target").

    Only nutrients present in profile.optimal_targets are included — nutrients
    without a configured optimal target are simply absent from the dict, so
    callers can distinguish "not customized" from "customized to zero".
    """
    import usda as _usda
    result: dict[str, tuple[float, str, str]] = {}
    for key, val in profile.optimal_targets.items():
        _label, unit = _usda.nutrient_label(key)
        result[key] = (float(val), unit, "target")
    return result


def compute_optimal_defaults(profile: UserProfile) -> dict[str, float]:
    """
    Return a small curated set of "optimal" starting values for nutrients
    where a widely-cited target above (or in place of) the standard RDA
    exists, but isn't itself an official DRI compute_rda() could compute.

    This is a starting point for Settings → Nutrient targets' "load
    recommended optimal targets" action, not personalized medical advice —
    the user can review and adjust every value, or skip nutrients entirely.

    Deliberately narrow: only nutrients with a specific, commonly-cited
    numeric target are included. Amino acids are excluded on purpose — their
    adequacy already depends on total protein intake and is evaluated by the
    app's FAO/DIAAS amino-acid scoring system (see ?diaas, ?fao), not a flat
    daily gram target; a static "optimal" AA value here would duplicate and
    could contradict that more accurate per-meal analysis.

    Sources (population-general, not age/condition-specific):
      - Vitamin D: many clinicians recommend 1000-2000 IU/day (25-50 mcg) for
        general adults, well above the 15-20 mcg RDA — the same example used
        in the Profile Optimal Targets manual topic (?optimal).
      - EPA + DHA: no official DRI exists (see ?omega3), but ~250-500 mg/day
        combined is common guidance (e.g. ISSFAL); split evenly here.
    """
    return {
        "vitamin_d_mcg": 50.0,
        "omega3_epa_mg": 250.0,
        "omega3_dha_mg": 250.0,
    }


def compute_upper_limits(profile: UserProfile) -> dict[str, float]:
    """
    Return built-in Tolerable Upper Intake Levels (UL) — the maximum daily
    amount considered safe for nearly all healthy people — for every tracked
    nutrient that has one, independent of the "limit"-type rows already in
    compute_rda() (currently just sodium; see the sodium note below). These
    apply automatically as the default max limit for any nutrient the user
    hasn't explicitly capped themselves — see get_max_limits().

    Source: NIH Office of Dietary Supplements / Institute of Medicine Dietary
    Reference Intake UL summary tables — see manual topic ?maxlimits for the
    full citation. Age-banded where the DRI tables show a real adult
    difference (calcium, phosphorus); flat across all adult ages otherwise,
    matching the source tables — most ULs simply don't vary by age or sex
    for adults 19+.

    Nutrients tracked by NuMa with NO established adult UL (deliberately
    absent from the dict below, not a bug): potassium, thiamin, riboflavin,
    vitamin B12, vitamin K. The DRI tables mark these "ND" (not determinable
    from available data) — that's different from "no risk at any dose," just
    that no safe upper bound has been established with confidence.

    Magnesium is deliberately excluded even though the DRI table publishes a
    350 mg/day UL: that figure applies only to supplemental (pill-form)
    magnesium, not intake from food — since NuMa sums whole-food magnesium,
    applying it here would flag entirely ordinary diets as "over the limit."

    Sodium already has its own dedicated "limit"-type row in compute_rda()
    (2300 mg/day, the Chronic Disease Risk Reduction intake) — a lower, more
    clinically relevant threshold than a formal UL (which the DRI tables
    don't even establish for sodium — "ND"), so it isn't duplicated here.

    Note: the vitamin_a_mcg UL applies specifically to preformed vitamin A
    (retinol); usda.NUTRIENT_MAP's vitamin_a_mcg is mcg RAE, which folds in
    provitamin-A carotenoids that carry no comparable toxicity risk. Treat this
    UL as a conservative approximation, not a precise clinical threshold.
    """
    age = profile.age
    return {
        "calcium_mg":    2000.0 if age >= 51 else 2500.0,
        "phosphorus_mg": 3000.0 if age >= 70 else 4000.0,
        "iron_mg":       45.0,
        "zinc_mg":       40.0,
        "iodine_mcg":    1100.0,
        "selenium_mcg":  400.0,
        "vitamin_a_mcg": 3000.0,
        "vitamin_c_mg":  2000.0,
        "vitamin_d_mcg": 100.0,
        "vitamin_e_mg":  1000.0,
        "niacin_mg":     35.0,
        "b6_mg":         100.0,
        "folate_mcg":    1000.0,
        "choline_mg":    3500.0,
    }


def get_max_limits(profile: UserProfile) -> dict[str, float]:
    """Return per-day max limits: built-in Tolerable Upper Intake Levels merged
    with the user's own configured caps, which take precedence where both exist.
    Use profile.max_limits directly (not this function) when you need only the
    user's explicit settings — e.g. the Settings editor."""
    return {**compute_upper_limits(profile), **profile.max_limits}
