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


def compute_rda(profile: UserProfile) -> dict[str, tuple[float, str, str]]:
    """
    Compute personalized Dietary Reference Intake targets from a UserProfile.

    Returns a dict mapping nutrient_key → (value, unit, rda_type) where
    rda_type is one of:
      "target"  — recommended intake (e.g. calories, carbs)
      "minimum" — Recommended Dietary Allowance or Adequate Intake
      "limit"   — tolerable upper intake / daily limit

    Only nutrients tracked in usda.NUTRIENT_MAP are included.
    Amino acids and phytonutrients without established DRIs are excluded.

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

    return {
        # Macros
        "calories":      (float(calories), "kcal", "target"),
        "protein_g":     (protein_g,       "g",    "minimum"),
        "carbs_g":       (130.0,           "g",    "minimum"),
        "fiber_g":       (fiber_g,         "g",    "minimum"),
        "sodium_mg":     (2300.0,          "mg",   "limit"),
        # Minerals
        "calcium_mg":    (calcium_mg,      "mg",   "minimum"),
        "iron_mg":       (iron_mg,         "mg",   "minimum"),
        "magnesium_mg":  (magnesium_mg,    "mg",   "minimum"),
        "phosphorus_mg": (phosphorus_mg,   "mg",   "minimum"),
        "potassium_mg":  (potassium_mg,    "mg",   "minimum"),
        "zinc_mg":       (zinc_mg,         "mg",   "minimum"),
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


def get_max_limits(profile: UserProfile) -> dict[str, float]:
    """Return the user's configured per-day max limits: nutrient_key -> cap value."""
    return dict(profile.max_limits)
