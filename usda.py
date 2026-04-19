# usda.py — backwards-compatible re-export shim.
# To work on this code, edit usda_api.py or usda_nutrients.py directly.
#   usda_api.py      — HTTP client: API key, search_foods, get_food_detail
#   usda_nutrients.py — nutrient math, AA analysis, DIAAS, complements, density
# Docs: README-numa-documentation.md, Architecture: "usda.py — backwards-compatible shim"

from usda_api import (       # noqa: F401
    NUTRIENT_MAP,
    ESSENTIAL_AMINO_ACIDS,
    AA_REFERENCE_MG_PER_G_PROTEIN,
    USDAError,
    get_api_key,
    set_api_key,
    search_foods,
    get_food_detail,
    _parse_food,             # used by tests
)
from usda_nutrients import (  # noqa: F401
    Nutrients,
    scale_nutrients,
    sum_nutrients,
    has_amino_acid_data,
    protein_completeness,
    nutrient_label,
    get_aa_gaps,
    get_complement_nutrients,
    suggest_complements,
    get_diaas,
    get_antinutrient_flags,
    get_density_g_per_ml,
)
