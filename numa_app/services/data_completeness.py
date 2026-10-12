"""
data_completeness.py — which nutrient groups a cached food is missing.

The groups are the six blocks of a Nutritional Analysis table plus the
amino acids shown under Protein Quality. A group counts as missing when the
food has no value at all for it — except Macronutrients, which is missing
when any of the four core values (calories, protein, carbs, fat) is absent,
and Amino Acids, which is missing only for a food with protein but without
enough AA values to score (has_amino_acid_data()'s rule). A group with a
few values present is normal for real USDA records, so it isn't flagged.

The user can mark a group "not needed" for one food (herbs and spices don't
need macronutrients — too little is used to matter); those choices live in
db.food_data_ignores and are passed in here as `ignored`.

Docs: README-numa-documentation.md, Architecture: "numa_app/services/data_completeness.py — nutrient-group completeness check"
"""
from __future__ import annotations

import usda as _usda

CORE_MACRO_KEYS = ("calories", "protein_g", "carbs_g", "fat_g")

# (group key stored in the DB, label shown to the user, nutrient keys)
GROUPS: list[tuple[str, str, list[str]]] = [
    ("macros", "Macronutrients", [
        "calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "sugar_g",
        "saturated_fat_g", "mono_fat_g", "poly_fat_g",
    ]),
    ("water", "Water", ["water_g"]),
    ("omega", "Omega Fatty Acids", [
        "omega3_ala_mg", "omega3_epa_mg", "omega3_dha_mg", "omega6_la_mg",
    ]),
    ("minerals", "Minerals", [
        "calcium_mg", "iron_mg", "magnesium_mg", "phosphorus_mg",
        "potassium_mg", "sodium_mg", "zinc_mg", "iodine_mcg", "selenium_mcg",
    ]),
    ("vitamins", "Vitamins", [
        "vitamin_a_mcg", "vitamin_c_mg", "vitamin_d_mcg", "vitamin_e_mg",
        "vitamin_k_mcg", "thiamin_mg", "riboflavin_mg", "niacin_mg",
        "b6_mg", "folate_mcg", "b12_mcg",
    ]),
    ("phyto", "Phytonutrients", [
        "beta_carotene_mcg", "alpha_carotene_mcg", "lycopene_mcg",
        "lutein_zeaxanthin_mcg", "choline_mg", "beta_sitosterol_mg", "isoflavones_mg",
    ]),
    ("aa", "Amino Acids", [
        "aa_tryptophan_g", "aa_threonine_g", "aa_isoleucine_g", "aa_leucine_g",
        "aa_lysine_g", "aa_methionine_g", "aa_cystine_g", "aa_phenylalanine_g",
        "aa_tyrosine_g", "aa_valine_g", "aa_histidine_g",
    ]),
]

GROUP_KEYS: list[str] = [g for g, _, _ in GROUPS]
GROUP_LABELS: dict[str, str] = {g: label for g, label, _ in GROUPS}
# The completeness check's starting "groups to check". Omega and
# phytonutrient values are absent from so many ordinary foods (most USDA
# records never measured them) that checking them by default buries the
# gaps that matter. Water likewise: numa only began recording it in October
# 2026, so every food cached before then lacks it until refreshed — tick
# Water to list them.
DEFAULT_CHECKED: list[str] = [g for g in GROUP_KEYS if g not in ("omega", "phyto", "water")]
_GROUP_NUTRIENTS: dict[str, list[str]] = {g: keys for g, _, keys in GROUPS}


def _group_missing(group: str, nutrients: dict) -> bool:
    if group == "macros":
        return any(k not in nutrients for k in CORE_MACRO_KEYS)
    if group == "aa":
        return nutrients.get("protein_g", 0) > 0 and not _usda.has_amino_acid_data(nutrients)
    return not any(k in nutrients for k in _GROUP_NUTRIENTS[group])


def missing_groups(nutrients: dict) -> list[str]:
    """Every group this food is missing, ignores not applied, in GROUPS order."""
    return [g for g in GROUP_KEYS if _group_missing(g, nutrients)]


def active_gaps(nutrients: dict, ignored: set[str] | frozenset[str] = frozenset(),
                checked: set[str] | None = None) -> list[str]:
    """missing_groups() minus the ones the user marked not needed for this
    food, limited to `checked` groups when given."""
    return [g for g in missing_groups(nutrients)
            if g not in ignored and (checked is None or g in checked)]


def is_blank(key: str, nutrients: dict) -> bool:
    """True if `key` has no usable value: absent, or — for an amino acid in
    a food with protein — a 0 placeholder (some imports store every AA as 0
    rather than omitting them, which is what has_amino_acid_data() reads as
    "no AA data")."""
    if key not in nutrients:
        return True
    return (key.startswith("aa_") and not nutrients[key]
            and nutrients.get("protein_g", 0) > 0)


def requested_keys(nutrients: dict, groups: list[str]) -> list[str]:
    """The nutrient keys to ask for to fill `groups` — only the blank ones,
    so a reply can't overwrite values the food already has."""
    return [k for g in groups for k in _GROUP_NUTRIENTS[g] if is_blank(k, nutrients)]


_GROUP_OF: dict[str, str] = {k: g for g, _, keys in GROUPS for k in keys}
# Everything food_data_ignores may hold for a nutrient gap: a whole group
# ("minerals"), or one nutrient ("iodine_mcg") — marked from the no-data list
# under Top Contributors, where hiding a food's missing iron because its
# iodine doesn't matter would be wrong.
IGNORE_KEYS: frozenset[str] = frozenset(GROUP_KEYS) | frozenset(_GROUP_OF)


def ignore_key(nutrient_key: str, *, is_dcp: bool = False) -> str:
    """The food_data_ignores key that marks `nutrient_key` not needed for a
    food: "aa" for DCP (amino acids), the group for a one-nutrient group
    (water), else the nutrient itself."""
    if is_dcp:
        return "aa"
    group = _GROUP_OF.get(nutrient_key)
    if group and len(_GROUP_NUTRIENTS[group]) == 1:
        return group
    return nutrient_key


def nutrient_ignored(ignored: set[str] | frozenset[str], nutrient_key: str, *, is_dcp: bool = False) -> bool:
    """True if the food's gap for `nutrient_key` is marked not needed — the
    nutrient itself, or its whole group."""
    if is_dcp:
        return "aa" in ignored
    return nutrient_key in ignored or _GROUP_OF.get(nutrient_key) in ignored


def none_keys(nutrients: dict, nutrient_key: str, *, is_dcp: bool = False) -> list[str]:
    """The keys "this food has none" records as 0 for a no-data gap: the
    nutrient if blank; for DCP, protein when there is no protein figure (a
    food with protein can't have no amino acids, so nothing then)."""
    if is_dcp:
        return ["protein_g"] if nutrients.get("protein_g") is None else []
    return [nutrient_key] if nutrient_key in _GROUP_OF and nutrients.get(nutrient_key) is None else []


def group_none_keys(nutrients: dict, group: str) -> list[str]:
    """The keys "has none" records as 0 for a whole missing group (Foods →
    9): its blank values. Never amino acids — a food listed there has
    protein, so it has amino acids too."""
    if group == "aa" or group not in _GROUP_NUTRIENTS:
        return []
    return [k for k in _GROUP_NUTRIENTS[group] if k not in nutrients]


def groups_for_keys(keys: list[str]) -> list[str]:
    """The groups (GROUPS order) that any of `keys` belong to."""
    wanted = set(keys)
    return [g for g in GROUP_KEYS if wanted & set(_GROUP_NUTRIENTS[g])]
