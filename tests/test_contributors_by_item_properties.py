"""
Property-based tests for Top Contributors' by-item table
(top_contributors.rank_by_meal_item(), fed by backend._meal_totals()).

The invariant: ranking a meal's items with recipes kept whole gives every
item exactly its own amount. So for ANY meal, and every nutrient, each
item's figure equals that item's own total worked out independently (a food
from its own figures, a recipe from its per-serving totals), and the items
add up to the meal's total; and likewise for glycemic load, each item
against its own food_gl() / recipe_gl() (unrounded total_exact), the items
adding up to the meal's. Checking only the sum is not enough: crediting a
shared food to the wrong item keeps the sum right (a deliberate re-break of
the fix passed a sum-only version of this test).

Written after a real miss (2026-10-14): tap water used in two recipes of one
meal was merged into one food row before ranking, and that row remembered
only the first recipe, so the second recipe showed 6.5 g of water instead of
~480 g. tests/test_top_contributors.py rebuilds that one case; this file
checks the whole class — any food shared by any items, at any depth.

Construction: a fixed pool of foods (made once per test, each with random
nutrient values drawn per test run) and, per Hypothesis example, a fresh
meal of 1-4 items. Each item is a food logged on its own or a recipe of 1-4
pool foods, some recipes holding a sub-recipe — and items draw from the same
small pool, so shared foods are the norm, not the exception. Amounts,
servings and recipe yields are random. Protein (DCP) isn't checked: an
item's standalone DCP deliberately isn't additive (complementarity).

Run just these:
    pytest tests/test_contributors_by_item_properties.py -q
"""
import json
import math

from hypothesis import HealthCheck, given, settings, strategies as st

import db as _db
from numa_app.services.glycemic_load import food_gl, meal_gl, recipe_gl
from numa_app.services.top_contributors import rank_by_meal_item
from web import backend

POOL = list(range(997301, 997307))                  # six foods
KEYS = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g", "water_g", "iron_mg", "b12_mcg"]
_counter = iter(range(10**6))

_value = st.floats(min_value=0.0, max_value=80.0, allow_nan=False, allow_infinity=False)
_grams = st.floats(min_value=1.0, max_value=600.0, allow_nan=False, allow_infinity=False)
_servings = st.sampled_from([0.5, 1.0, 1.5, 2.0, 3.0])

_food_item = st.tuples(st.just("food"), st.sampled_from(POOL), _grams)
_recipe_item = st.tuples(
    st.just("recipe"),
    st.lists(st.tuples(st.sampled_from(POOL), _grams), min_size=1, max_size=4),
    _servings,                                           # recipe yield
    _servings,                                           # servings eaten
    st.one_of(st.none(),                                 # optional sub-recipe
              st.tuples(st.lists(st.tuples(st.sampled_from(POOL), _grams), min_size=1, max_size=3),
                        _servings, _servings)),
)
_meal = st.lists(st.one_of(_food_item, _recipe_item), min_size=1, max_size=4)
_pool_values = st.lists(st.fixed_dictionaries({k: _value for k in KEYS}), min_size=len(POOL),
                        max_size=len(POOL))
_pool_gi = st.lists(st.one_of(st.none(), st.floats(min_value=10, max_value=100)),
                    min_size=len(POOL), max_size=len(POOL))


def _make_pool(values, gis):
    with _db.get_db() as conn:
        for fid, nuts, gi in zip(POOL, values, gis):
            _db.cache_food(conn, fid, f"Pool food {fid}", "SR Legacy", None, 100.0, "g", nuts, [])
            # Set or clear: the pool outlives each example, so a GI left over
            # from the last one would make the next depend on it.
            _db.set_food_annotation(conn, fid, gi_estimate=gi, gi_no_prompt=False, diaas_estimate=None,
                                    diaas_no_prompt=False, prep_context=None)


def _recipe(conn, ingredients, yield_servings, sub=None):
    n = next(_counter)
    rid = _db.recipe_create(conn, f"Recipe {n}", "", yield_servings, "")
    for fid, grams in ingredients:
        _db.recipe_add_ingredient(conn, rid, fid, f"Pool food {fid}", grams, "g")
    if sub is not None:
        sub_ings, sub_yield, sub_used = sub
        sid = _recipe(conn, sub_ings, sub_yield)
        _db.recipe_add_ingredient(conn, rid, 0, f"Sub {sid}", sub_used, "servings", ref_recipe_id=sid)
    return rid


def _make_meal(spec) -> int:
    with _db.get_db() as conn:
        mid = _db.meal_create(conn, f"Meal {next(_counter)}", "2026-10-14")
        for item in spec:
            if item[0] == "food":
                _kind, fid, grams = item
                _db.meal_add_food(conn, mid, fid, f"Pool food {fid}", grams, "g")
            else:
                _kind, ings, yield_servings, eaten, sub = item
                rid = _recipe(conn, ings, yield_servings, sub)
                _db.meal_add_recipe(conn, mid, rid, f"Recipe {rid}", eaten)
    return mid


def _close(a: float, b: float) -> bool:
    return math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-6)


def _own_totals(mid: int, key: str) -> dict:
    """Each meal item's own amount of `key`, worked out without the ranking
    or the meal-wide food merge: a food from its own figures, a recipe from
    its per-serving totals x servings eaten. Keyed by the item's name, as
    the ranking reports it; items with none are left out."""
    out = {}
    with _db.get_db() as conn:
        for item in _db.meal_get_items(conn, mid):
            if item["item_type"] == "food":
                nuts = json.loads(_db.get_cached_food(conn, item["fdc_id"])["nutrients_json"])
                amount = (nuts.get(key) or 0.0) * item["amount"] / 100.0
            else:
                amount = backend._recipe_nutrients_per_serving(item["recipe_id"], conn).get(key, 0.0) * item["amount"]
            if amount > 0:
                out[item["food_name"]] = out.get(item["food_name"], 0.0) + amount
    return out


@settings(max_examples=60, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(values=_pool_values, gis=_pool_gi, data=st.data())
def test_items_add_up_to_the_meal_total_for_every_nutrient(values, gis, data):
    _make_pool(values, gis)
    mid = _make_meal(data.draw(_meal))
    _items, totals, _diaas, leaves = backend._meal_totals(mid)
    with _db.get_db() as conn:
        for key in KEYS:
            ranked = rank_by_meal_item(leaves, key, conn)
            # Every item gets exactly its own amount — not just a total that
            # adds up (misattributing a shared food keeps the total right:
            # that was the original bug, and an add-up check alone missed it).
            got = {}
            for c in ranked["items"]:
                got[c["food_name"]] = got.get(c["food_name"], 0.0) + c["amount"]
            want = _own_totals(mid, key)
            assert set(got) == set(want), key
            for name in want:
                assert _close(got[name], want[name]), (key, name)
            assert _close(ranked["total"], totals.get(key, 0.0)), key


@settings(max_examples=40, deadline=None, suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(values=_pool_values, gis=_pool_gi, data=st.data())
def test_items_add_up_to_the_meal_glycemic_load(values, gis, data):
    _make_pool(values, gis)
    mid = _make_meal(data.draw(_meal))
    _items, _totals, _diaas, leaves = backend._meal_totals(mid)
    with _db.get_db() as conn:
        ranked = rank_by_meal_item(leaves, "gl", conn, is_gl=True)
        # Every item gets exactly its own glycemic load, worked out the other
        # way glycemic_load has: a food alone (food_gl), a recipe from its own
        # ingredient lines (recipe_gl), unrounded.
        got = {}
        for c in ranked["items"]:
            got[c["food_name"]] = got.get(c["food_name"], 0.0) + c["amount"]
        want = {}
        for item in _db.meal_get_items(conn, mid):
            if item["item_type"] == "food":
                own = food_gl(item["food_name"], item["fdc_id"],
                              json.loads(_db.get_cached_food(conn, item["fdc_id"])["nutrients_json"]),
                              item["amount"], _db.get_food_annotation(conn, item["fdc_id"]))
            else:
                own = recipe_gl(conn, item["recipe_id"], item["amount"])
            if own["total_exact"] > 0:
                want[item["food_name"]] = want.get(item["food_name"], 0.0) + own["total_exact"]
        assert set(got) == set(want)
        for name in want:
            assert _close(got[name], want[name]), name
        # ...and they add up to the meal's, exactly before its display rounding.
        assert _close(ranked["total"], meal_gl(conn, mid)["total_exact"])
