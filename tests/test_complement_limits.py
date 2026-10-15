"""
test_complement_limits.py — per-meal limits on protein complement suggestions.

A complement suggestion used to offer any amount up to 300 g of any food —
4½ cups of nutritional yeast, say. Each candidate now has a per-meal limit
(usda_nutrients.complement_meal_limit): the user's own, saved from the
suggestion itself (food_annotations.max_meal_g, POST /complement-limit), else
a multiple of its label serving, else a default by food type. A food that
needs more than its limit is offered AT the limit, marked capped; the user
can lift the limit for one page view (uncap_names / ?uncap=).
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import usda as _usda
import web.backend as backend
from numa_app.services import complements as _complements
from usda_nutrients import _score_one_complement, get_aa_gaps


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({"include_animal_foods": True}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)


# Lysine-poor base; a lysine-rich candidate needs ~150 g to close it.
_BASE = {"protein_g": 100.0, "aa_lysine_g": 3.0}
_LYS = {"protein_g": 100.0, "aa_lysine_g": 6.0}


class TestComplementMealLimit:
    def test_user_limit_wins(self):
        assert _usda.complement_meal_limit("Nutritional yeast", user_g=25, serving_g=10) == (
            25.0, "your limit for this food")

    def test_label_serving_multiple(self):
        g, src = _usda.complement_meal_limit("Anything", serving_g=30)
        assert g == 90 and "3 servings" in src

    def test_recipe_serving_multiple(self):
        g, src = _usda.complement_meal_limit("Soup", serving_g=100, is_recipe=True)
        assert g == 200 and "2 servings" in src

    def test_serving_multiple_never_exceeds_practical_ceiling(self):
        g, _ = _usda.complement_meal_limit("Stew", serving_g=500, is_recipe=True)
        assert g == _usda.MAX_PRACTICAL_GAP_CLOSER_GRAMS

    @pytest.mark.parametrize("name, grams", [
        ("Nutritional Yeast Flakes", 15),      # must not fall into "nuts"
        ("Spirulina powder", 15),
        ("Soy protein isolate", 40),
        ("Pea Protein Powder", 40),
        ("Pumpkin seeds", 40),
        ("Brazil nuts", 40),
        ("Peanut butter", 40),
        ("Cheese, cheddar", 60),
        ("Lentils, cooked", 300),
        ("Coconut milk", 300),                 # "coconut" isn't a nut here
    ])
    def test_type_defaults(self, name, grams):
        assert _usda.complement_meal_limit(name)[0] == grams


class TestCappedScoring:
    def test_over_limit_is_offered_at_the_limit(self):
        gaps = get_aa_gaps(_BASE)
        full = _score_one_complement(_BASE, gaps, 1.0, _LYS, 0.9, "aa_lysine_g")
        capped = _score_one_complement(_BASE, gaps, 1.0, _LYS, 0.9, "aa_lysine_g", max_grams=40)
        assert full["capped"] is False and full["grams"] == 150
        assert capped["capped"] is True
        assert capped["grams"] == 40
        assert capped["closing_grams"] == 150
        # Partway: better than before, not closed.
        assert gaps[0][1] < capped["new_scores"]["aa_lysine_g"] < 1.0
        assert capped["protein_added"] == pytest.approx(40.0)

    def test_within_limit_is_not_capped(self):
        gaps = get_aa_gaps(_BASE)
        m = _score_one_complement(_BASE, gaps, 1.0, _LYS, 0.9, "aa_lysine_g", max_grams=200)
        assert m["capped"] is False and m["grams"] == 150

    def test_main_gap_capped_beats_closing_a_minor_gap(self):
        # The candidate closes the minor Isoleucine gap with a token amount but
        # can only get partway on Lysine within its limit. Partway on the main
        # gap is the more useful suggestion.
        base = {"protein_g": 100.0, "aa_lysine_g": 3.0, "aa_isoleucine_g": 2.8}
        cand = {"name": "Lysine Powder", "fdc_id": 1, "max_meal_g": 20,
                "nutrients": {"protein_g": 100.0, "aa_lysine_g": 6.0, "aa_isoleucine_g": 6.0},
                "diaas": 0.9}
        result = _usda.suggest_complements(base, [cand])
        s = result["pantry"][0]
        assert s["target_aa"] == "aa_lysine_g"
        assert s["capped"] is True and s["grams"] == 20


class TestSuggestComplementsLimits:
    def _cand(self, **kw):
        return {"name": "Lysine Food", "fdc_id": 7, "nutrients": _LYS, "diaas": 0.9, **kw}

    def test_user_limit_caps_and_is_reported(self):
        s = _usda.suggest_complements(_BASE, [self._cand(max_meal_g=50)])["pantry"][0]
        assert (s["grams"], s["capped"], s["closing_grams"]) == (50, True, 150)
        assert s["limit_g"] == 50 and s["user_limit"] is True
        assert s["limit_source"] == "your limit for this food"
        assert s["uncapped"] is False

    def test_uncap_lifts_the_limit_for_this_view(self):
        s = _usda.suggest_complements(_BASE, [self._cand(max_meal_g=50)],
                                      uncap_names={"lysine food"})["pantry"][0]
        assert (s["grams"], s["capped"]) == (150, False)
        assert s["uncapped"] is True

    def test_label_serving_sets_the_limit(self):
        s = _usda.suggest_complements(_BASE, [self._cand(serving_g=10)])["pantry"][0]
        assert s["grams"] == 30 and s["capped"] is True

    def test_improver_steps_stop_at_the_limit(self):
        # Nothing here closes a gap analytically, so yeast is a DIAAS booster;
        # its steps must not run past its 15 g default.
        result = _usda.suggest_complements(
            {"protein_g": 20.0, "aa_methionine_g": 0.10, "aa_cystine_g": 0.06, "aa_lysine_g": 0.30},
            [], base_digestibility=0.6, max_improver_grams=120,
        )
        for s in result["diaas_improvers"]:
            limit = _usda.complement_meal_limit(s["name"])[0]
            assert max(step["grams"] for step in s["steps"]) <= limit

    def test_display_carries_limit_fields(self):
        d = _complements.build_complement_display(_BASE, [self._cand(max_meal_g=50)])
        s = d["pantry"][0]
        assert (s["capped"], s["closing_grams"], s["limit_g"], s["user_limit"]) == (True, 150, 50, True)


class TestLabelServing:
    def test_grams_only(self):
        assert _complements.label_serving_g({"serving_size": 30.0, "serving_unit": "g"}) == 30.0
        assert _complements.label_serving_g({"serving_size": 30.0, "serving_unit": "GRM"}) == 30.0
        assert _complements.label_serving_g({"serving_size": 240.0, "serving_unit": "ml"}) is None
        assert _complements.label_serving_g({"serving_size": None, "serving_unit": None}) is None
        assert _complements.label_serving_g(None) is None


class TestDbMealLimit:
    def test_set_read_clear(self, cached_food):
        fid = cached_food["fdcId"]
        with _db.get_db() as conn:
            _db.set_food_meal_limit(conn, fid, 25.0)
            assert _db.food_meal_limits(conn) == {fid: 25.0}
            # A preference, not a data edit.
            assert not _db.has_user_annotation(conn, fid)
            _db.set_food_meal_limit(conn, fid, None)
            assert _db.food_meal_limits(conn) == {}

    def test_leaves_other_annotation_fields_alone(self, cached_food):
        fid = cached_food["fdcId"]
        with _db.get_db() as conn:
            _db.upsert_food_annotation(conn, fid, gi_estimate=55.0, gi_source="test")
            _db.set_food_meal_limit(conn, fid, 30.0)
            row = _db.get_food_annotation(conn, fid)
        assert row["gi_estimate"] == 55.0 and row["max_meal_g"] == 30.0


class TestLimitRoute:
    @pytest.fixture()
    def client(self) -> TestClient:
        return TestClient(backend.app)

    def test_save_then_clear(self, client, cached_food):
        fid = cached_food["fdcId"]
        r = client.post("/complement-limit", data={
            "limit_fdc": str(fid), f"limit_g_{fid}": "20", "limit_next": "/meal/5?q=x",
        }, follow_redirects=False)
        assert r.status_code == 303
        assert r.headers["location"] == f"/meal/5?q=x#limit-{fid}"
        with _db.get_db() as conn:
            assert _db.food_meal_limits(conn) == {fid: 20.0}
        client.post("/complement-limit", data={"limit_fdc": str(fid), f"limit_g_{fid}": ""},
                    follow_redirects=False)
        with _db.get_db() as conn:
            assert _db.food_meal_limits(conn) == {}

    def test_off_site_next_falls_back_to_the_food(self, client, cached_food):
        fid = cached_food["fdcId"]
        r = client.post("/complement-limit", data={
            "limit_fdc": str(fid), f"limit_g_{fid}": "20", "limit_next": "//evil.example/",
        }, follow_redirects=False)
        assert r.headers["location"] == f"/food/{fid}#limit-{fid}"

    @pytest.mark.parametrize("value", ["abc", "0", "-5"])
    def test_bad_value_is_an_error_not_silently_dropped(self, client, cached_food, value):
        fid = cached_food["fdcId"]
        r = client.post("/complement-limit", data={"limit_fdc": str(fid), f"limit_g_{fid}": value},
                        follow_redirects=False)
        assert r.status_code == 400
        with _db.get_db() as conn:
            assert _db.food_meal_limits(conn) == {}

    def test_unknown_food_is_404(self, client):
        r = client.post("/complement-limit", data={"limit_fdc": "999999999", "limit_g_999999999": "20"},
                        follow_redirects=False)
        assert r.status_code == 404


class TestLimitPlumbingMutationGaps20261014:
    """The serving that sets a candidate's limit must reach every tier
    (gaps found by the 2026-10-14 mutation run on usda_nutrients.py)."""

    def test_recipe_limit_uses_its_serving_weight_not_serving_g(self):
        cand = {"name": "Lysine Stew", "recipe_id": 5, "serving_weight_g": 40,
                "serving_g": 10, "nutrients": _LYS, "diaas": 0.9}
        s = _usda.suggest_complements(_BASE, [cand])["pantry"][0]
        assert (s["grams"], s["limit_g"], s["limit_source"]) == (80, 80, "2 servings of 40 g")

    def test_general_tier_cache_food_keeps_its_label_serving(self):
        from usda_nutrients import _find_complement_by_name
        whey = _find_complement_by_name("Whey protein powder")
        real = {"name": "Whey protein powder", "fdc_id": 999, "nutrients": whey["nutrients"],
                "diaas": whey["diaas"], "serving_g": 20}
        general = _usda.suggest_complements(_BASE, [], cache_candidates=[real])["general"]
        s = next(g for g in general if g["name"] == "Whey protein powder")
        assert (s["limit_g"], s["limit_source"]) == (60, "3 servings of 20 g")

    def test_pairs_tier_respects_a_pantry_food_label_serving(self):
        from tests.test_usda import _PAIR_CASCADE_NUTRIENTS
        from usda_nutrients import _find_complement_by_name
        nuts = _find_complement_by_name("Brazil nuts")
        cand = {"name": "My Brazil nuts", "fdc_id": 4242, "nutrients": nuts["nutrients"],
                "diaas": nuts["diaas"]}

        def pairs_with_it(c):
            return [p for p in _usda.suggest_complements(_PAIR_CASCADE_NUTRIENTS, [c])["pairs"]
                    if any(f["name"] == "My Brazil nuts" for f in p["foods"])]

        assert pairs_with_it(cand)                          # 40 g nut default: pairs found
        assert pairs_with_it({**cand, "serving_g": 3}) == []  # 9 g limit: too little to pair
