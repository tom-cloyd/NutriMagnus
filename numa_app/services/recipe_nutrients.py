"""
recipe_nutrients.py — recursive recipe-ingredient expansion and nutrient
totaling, used by the web backend (backend.py). Previously reimplemented
independently in five separate places before being extracted here.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/recipe_nutrients.py — recipe nutrient aggregation"
"""
import json
from collections.abc import Callable

import db as _db
import usda as _usda

from . import supplements as _supps
from . import water as _water

Nutrients = dict[str, float]

# Optional per-ingredient rewrite used by what-if analysis (services/whatif.py):
# given one ingredient as (kind, id, qty) — kind "food" (qty = grams) or
# "recipe" (qty = servings of that sub-recipe) — return what to use in its
# place, as a list of the same tuples ([] drops it). None means "as authored".
Rewrite = Callable[[str, int, float], list[tuple[str, int, float]]]


def expand_recipe_ingredients(
    recipe_id: int,
    conn,
    *,
    portion_factor: float = 1.0,
    rewrite: Rewrite | None = None,
    cooked_water: bool = True,
    _drink: bool | None = None,
) -> list[dict]:
    """Recursively expand a recipe into its leaf food ingredients.

    Sub-recipe ingredients are expanded recursively, scaling by
    (sub-ingredient amount / sub-recipe servings) * portion_factor — i.e.
    portion_factor=1.0 means "one full batch of this recipe as authored".

    rewrite (see Rewrite) is applied to every ingredient row at every depth
    before it is expanded — what-if analysis's hook; it never writes.

    Returns [{"food_name", "fdc_id", "nutrients_100g", "grams",
    "is_supplement"}, ...] — one entry per leaf food ingredient; sub-recipes
    themselves don't appear. A supplement's nutrients_100g also carries the
    from-supplements split (supplements.tag), and "grams" is its internal
    100 g per unit — callers that total weight skip it.
    Each leaf's nutrients_100g carries its water split (water.tag): from
    drinks only when this recipe or a recipe it sits inside is marked as one —
    an ingredient's own drink flag doesn't count inside a recipe (a cup of tap
    water in bread dough is food water). See drink_ingredient_water().
    A recipe with its water once cooked set has its leaves' water rescaled to
    match (apply_cooked_water()); cooked_water=False skips that for this
    recipe itself (not its sub-recipes) — to show the raw figure beside it.
    """
    recipe = _db.recipe_get(conn, recipe_id)
    if _drink is None:
        _drink = _water.is_drink(recipe)
    result: list[dict] = []
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_id"]:
            entries = [("recipe", ing["ref_recipe_id"], float(ing["amount"]))]
        elif ing["fdc_id"]:
            entries = [("food", ing["fdc_id"], float(ing["amount"]))]
        else:
            continue
        rewritten = rewrite is not None
        if rewritten:
            entries = rewrite(*entries[0])
        for kind, item_id, qty in entries:
            if kind == "recipe":
                sub = _db.recipe_get(conn, item_id)
                sub_servings = float(sub["servings"] or 1) if sub else 1.0
                sub_factor = qty / sub_servings * portion_factor
                result.extend(expand_recipe_ingredients(
                    item_id, conn,
                    portion_factor=sub_factor,
                    rewrite=rewrite,
                    _drink=_drink or _water.is_drink(sub),
                ))
                continue
            cached = _db.get_cached_food(conn, item_id)
            if not cached or not cached["nutrients_json"]:
                continue
            nuts_100g = json.loads(cached["nutrients_json"])
            if nuts_100g:
                supp = _supps.is_supplement(cached)
                # Inside a recipe, only the recipe's own drink flag (or an
                # enclosing recipe's) counts: tap water in bread dough isn't
                # a drink, whatever the food's own flag says (2026-11-09).
                nuts_100g = _supps.tag(_water.tag(nuts_100g, _drink), supp)
                result.append({
                    "food_name":      cached["name"] if rewritten and item_id != ing["fdc_id"] else ing["food_name"],
                    "fdc_id":         item_id,
                    "nutrients_100g": nuts_100g,
                    "grams":          qty * portion_factor,
                    "is_supplement":  supp,
                    "food_is_drink":  _water.is_drink(cached),
                })
    if cooked_water:
        apply_cooked_water(recipe, result, portion_factor, drink=_drink)
    return result


def drink_ingredient_water(recipe_id: int, conn) -> list[dict]:
    """The drink foods inside a recipe whose water counts as water from food
    because the recipe isn't a drink — for the note on the recipe page.
    [{"name", "water_g"}] per whole batch (after cooking, when set), merged by
    food and heaviest first; [] for a drink recipe or one with none."""
    found: dict[int, dict] = {}
    for lf in expand_recipe_ingredients(recipe_id, conn):
        food_water = lf["nutrients_100g"].get(_water.FOOD_KEY)
        if not lf.get("food_is_drink") or not food_water:
            continue
        entry = found.setdefault(lf["fdc_id"], {"name": lf["food_name"], "water_g": 0.0})
        entry["water_g"] += float(food_water) * lf["grams"] / 100.0
    return sorted(found.values(), key=lambda e: -e["water_g"])


def stated_batch_grams(recipe) -> float | None:
    """The recipe's stated total weight in grams (what one finished batch
    weighs), or None when none is stated or its unit isn't a weight. The
    ingredient-sum fallback recipe_serving_grams() uses is deliberately not
    used here: that's the raw weight, before cooking changed it."""
    from numa_app.services.portions import _UNIT_TO_GRAMS
    if not recipe or not recipe["total_weight"]:
        return None
    factor = _UNIT_TO_GRAMS.get((recipe["total_weight_unit"] or "g").lower())
    return float(recipe["total_weight"]) * factor if factor else None


def cooked_water_per_100g(recipe) -> float | None:
    """recipes.cooked_water_per_100g, or None (unset, or a row selected
    without that column)."""
    try:
        v = recipe["cooked_water_per_100g"]
    except (IndexError, KeyError, TypeError):
        return None
    return float(v) if v is not None else None


def apply_cooked_water(recipe, leaves: list[dict], portion_factor: float,
                       *, drink: bool) -> None:
    """Replace the water `leaves` (one recipe's expanded ingredients, at
    `portion_factor` of a batch) add up to with the recipe's water once
    cooked — recipes.cooked_water_per_100g × its stated total weight — when
    both are set. Cooking drives water off, so the raw ingredients' water
    overstates it. In place; each leaf's water is scaled by the same factor,
    so per-food breakdowns still add up to the recipe's total. The cooked
    water counts as water from food unless the recipe (or one it sits in)
    is a drink: water baked into bread is no longer a drink. Nothing happens
    without both values, so a recipe never loses its water by accident.
    """
    per_100g = cooked_water_per_100g(recipe)
    batch_g = stated_batch_grams(recipe)
    if per_100g is None or not batch_g:
        return
    target = per_100g * batch_g / 100.0 * portion_factor
    food_leaves = [lf for lf in leaves if not lf.get("is_supplement")]
    with_water = [lf for lf in food_leaves if lf["nutrients_100g"].get(_water.WATER_KEY) is not None]
    raw = sum(float(lf["nutrients_100g"][_water.WATER_KEY]) * lf["grams"] / 100.0 for lf in with_water)
    if raw > 0:
        factor = target / raw
        for lf in with_water:
            water = float(lf["nutrients_100g"][_water.WATER_KEY]) * factor
            lf["nutrients_100g"] = _water.tag({**lf["nutrients_100g"], _water.WATER_KEY: water}, drink)
        return
    # No ingredient has a water value: the whole amount goes on the heaviest one.
    heaviest = max((lf for lf in food_leaves if lf["grams"] > 0), key=lambda lf: lf["grams"], default=None)
    if heaviest is not None:
        water = target * 100.0 / heaviest["grams"]
        heaviest["nutrients_100g"] = _water.tag({**heaviest["nutrients_100g"], _water.WATER_KEY: water}, drink)


def recipe_water_per_100g(recipe_id: int, conn) -> float | None:
    """The recipe's water in g per 100 g as numa counts it — its cooked water
    when set, else its ingredients' water over its batch weight (stated, or
    the complete ingredient sum). None when either is unknown."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return None
    per_100g = cooked_water_per_100g(recipe)
    if per_100g is not None and stated_batch_grams(recipe):
        return per_100g
    serving_g = recipe_serving_grams(recipe_id, conn)
    water = recipe_total_nutrients(recipe_id, conn).get(_water.WATER_KEY)
    if not serving_g or water is None:
        return None
    return water / (serving_g * float(recipe["servings"] or 1)) * 100.0


def cooked_water_info(recipe_id: int, conn) -> dict | None:
    """Figures for the recipe page's "water after cooking" box, or None for
    no recipe: "value" (cooked_water_per_100g, or None), "batch_g" (stated
    total weight in g, or None), "applied" (value and batch_g both set),
    "raw_water_g" (the water the ingredients add up to, before cooking),
    "raw_g" (what the ingredients weigh), "raw_complete" (every ingredient's
    weight known), and "estimate" — g of water per 100 g if everything
    cooking took off the weight was water, or None when there's no stated
    weight, no complete raw weight, or no loss."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return None
    raw_water = None
    for lf in expand_recipe_ingredients(recipe_id, conn, cooked_water=False):
        w = lf["nutrients_100g"].get(_water.WATER_KEY)
        if w is not None and not lf.get("is_supplement"):
            raw_water = (raw_water or 0.0) + float(w) * lf["grams"] / 100.0
    computed = _db.recipe_compute_weight(conn, recipe_id)
    raw_g = computed[0] if computed else None
    raw_complete = bool(computed and computed[1])
    batch_g = stated_batch_grams(recipe)
    value = cooked_water_per_100g(recipe)
    estimate = None
    if batch_g and raw_g and raw_complete and raw_water is not None and raw_g > batch_g:
        left = raw_water - (raw_g - batch_g)
        if left > 0:
            estimate = left / batch_g * 100.0
    return {"value": value, "batch_g": batch_g, "applied": value is not None and bool(batch_g),
            "raw_water_g": raw_water, "raw_g": raw_g, "raw_complete": raw_complete,
            "estimate": estimate}


def atomic_recipe_ingredients(
    recipe_id: int,
    conn,
    *,
    portion_factor: float = 1.0,
    rewrite: Rewrite | None = None,
) -> list[dict]:
    """Expand a recipe into food-level dicts for DIAAS/digestibility pooling —
    direct ingredients expand as usual, but a sub-recipe ingredient is kept as
    ONE atomic food using its own already-computed whole-batch nutrient
    profile, rather than decomposed into its raw ingredients.

    A sub-recipe is often deliberately built from complementary foods to raise
    its own DCP (e.g. a nut butter blended with a seed to fill its limiting
    amino acid). Recursively flattening it for an outer recipe's digestibility
    breakdown would hide that complementarity behind tiny per-component
    protein amounts and misattribute its digestible protein to whichever raw
    ingredient happens to dominate its weight — "recipes taken as a whole" is
    the correct model here.

    Returns [{"food_name", "fdc_id", "recipe_id", "nutrients_100g", "grams"}, ...]
    — fdc_id is None for a sub-recipe entry, recipe_id is None for a direct food.
    Use expand_recipe_ingredients() instead when you need raw-leaf totals (e.g.
    summing calories/vitamins/minerals, where grouping makes no difference).

    rewrite: see expand_recipe_ingredients(); also applied inside each
    sub-recipe's own totals.
    """
    result: list[dict] = []
    for ing in _db.recipe_get_ingredients(conn, recipe_id):
        if ing["ref_recipe_deleted"]:
            continue
        if ing["ref_recipe_id"]:
            entries = [("recipe", ing["ref_recipe_id"], float(ing["amount"]))]
        elif ing["fdc_id"]:
            entries = [("food", ing["fdc_id"], float(ing["amount"]))]
        else:
            continue
        logged = entries[0][:2]
        if rewrite is not None:
            entries = rewrite(*entries[0])
        for kind, item_id, qty in entries:
            if kind == "recipe":
                sub = _db.recipe_get(conn, item_id)
                sub_servings = float(sub["servings"] or 1) if sub else 0.0
                if not sub or sub_servings <= 0:
                    continue
                sub_total = recipe_total_nutrients(item_id, conn, rewrite=rewrite)
                scale = qty / sub_servings * portion_factor
                scaled = {k: v * scale for k, v in sub_total.items()}
                if scaled.get("protein_g", 0.0) <= 0:
                    continue
                result.append({
                    "food_name":      ing["food_name"] if (kind, item_id) == logged else sub["name"],
                    "fdc_id":         None,
                    "recipe_id":      item_id,
                    "nutrients_100g": scaled,
                    "grams":          100.0,
                })
                continue
            cached = _db.get_cached_food(conn, item_id)
            if not cached or not cached["nutrients_json"]:
                continue
            nuts_100g = json.loads(cached["nutrients_json"])
            if not nuts_100g:
                continue
            result.append({
                "food_name":      ing["food_name"] if (kind, item_id) == logged else cached["name"],
                "fdc_id":         item_id,
                "recipe_id":      None,
                "nutrients_100g": nuts_100g,
                "grams":          qty * portion_factor,
            })
    return result


def recipe_total_nutrients(
    recipe_id: int,
    conn,
    *,
    portion_factor: float = 1.0,
    rewrite: Rewrite | None = None,
) -> Nutrients:
    """Sum nutrients across a recipe's (recursively expanded) leaf ingredients.

    portion_factor=1.0 (default) returns totals for one full batch of the
    recipe as authored — callers scale by their own serving-consumption math.
    rewrite: see expand_recipe_ingredients().
    """
    total: Nutrients = {}
    for leaf in expand_recipe_ingredients(
        recipe_id, conn, portion_factor=portion_factor, rewrite=rewrite,
    ):
        scaled = _usda.scale_nutrients(leaf["nutrients_100g"], leaf["grams"], base_size=100.0)
        total = _usda.sum_nutrients(total, scaled)
    return total


def best_aa_nutrients(nutrients: Nutrients, food_name: str) -> Nutrients | None:
    """Merge in complement-table AA data if `nutrients` is missing it.

    Returns `nutrients` unchanged if it already has AA data. If not, tries to
    merge in AA values from usda.get_complement_nutrients(food_name), scaled
    to match the food's actual protein content. Returns None if no AA data is
    available from either source.
    """
    if _usda.has_confirmed_aa_data(nutrients):
        return nutrients
    complement = _usda.get_complement_nutrients(food_name)
    if complement and _usda.has_confirmed_aa_data(complement):
        actual_protein = nutrients.get("protein_g", 0)
        ref_protein = complement.get("protein_g", 0)
        if ref_protein > 0 and actual_protein > 0:
            scale = actual_protein / ref_protein
            merged = dict(nutrients)
            for k, v in complement.items():
                if k.startswith("aa_") and k not in merged:
                    merged[k] = v * scale
            return merged
    return None


def recipe_aa_indicator(recipe_id: int, conn) -> str:
    """AA-column status for a recipe row, in aa_indicator()'s own vocabulary.

    Search/list rows show a food's AA status via usda.aa_indicator(), which
    takes a nutrients dict — a recipe has none of its own, so its status comes
    from the totals of its (recursively expanded) ingredients. An empty recipe,
    or one whose ingredients have no cached nutrients at all, totals to {} and
    so reports "⚠", exactly as an uncached food does.
    """
    return _usda.aa_indicator(recipe_total_nutrients(recipe_id, conn))


def recipe_serving_grams(recipe_id: int, conn) -> float | None:
    """Gram weight of one serving of a recipe, or None if it can't be worked out.

    Two sources, in order: the recipe's own stated total weight (converted from
    whatever unit it was entered in — it is stored as typed, not normalized),
    and failing that the sum of its ingredients' weights, but only when
    db.recipe_compute_weight() reports that sum as complete. An incomplete sum
    is a lower bound, and a serving weight quietly short by an unknown amount is
    worse than none at all.
    """
    from numa_app.services.portions import _UNIT_TO_GRAMS

    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return None
    servings = float(recipe["servings"] or 0)
    if servings <= 0:
        return None

    if recipe["total_weight"]:
        factor = _UNIT_TO_GRAMS.get((recipe["total_weight_unit"] or "g").lower())
        if factor:
            return float(recipe["total_weight"]) * factor / servings

    computed = _db.recipe_compute_weight(conn, recipe_id)
    if computed and computed[1] and computed[0] > 0:
        return computed[0] / servings
    return None
