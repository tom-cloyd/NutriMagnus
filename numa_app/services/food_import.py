"""
food_import.py — shared nutrient-key validation and per-serving conversion for
manually-compiled food imports, used by the in-app Claude-fetch flow
(numa_app/services/claude_fetch.py), the import_foods.py script, and
import_json_folder.py.

Single source of truth for VALID_NUTRIENT_KEYS: derived from usda_api.NUTRIENT_MAP
so it can't drift out of sync with the nutrients numa actually understands.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/food_import.py — food import validation"
"""
import usda as _usda

VALID_NUTRIENT_KEYS: frozenset[str] = frozenset(v[0] for v in _usda.NUTRIENT_MAP.values())


def convert_per_serving(per_serving: dict[str, float], serving_size_g: float) -> dict[str, float]:
    """Scale a per-serving nutrient dict to per-100g.

    Raises ValueError if serving_size_g is not positive.
    """
    if serving_size_g <= 0:
        raise ValueError(f"serving_size_g must be positive, got {serving_size_g}")
    factor = 100 / serving_size_g
    return {k: v * factor for k, v in per_serving.items()}


def validate_and_strip(raw: dict) -> tuple[dict[str, float], list[str]]:
    """Filter a raw nutrient dict to VALID_NUTRIENT_KEYS, coercing numeric values.

    Returns (clean_nutrients, stripped_key_names). Non-numeric values for an
    otherwise-valid key are dropped (not coerced) and reported as stripped.
    """
    clean: dict[str, float] = {}
    stripped: list[str] = []
    for k, v in raw.items():
        if k not in VALID_NUTRIENT_KEYS:
            stripped.append(k)
            continue
        if isinstance(v, (int, float)):
            clean[k] = float(v)
        else:
            stripped.append(k)
    return clean, stripped
