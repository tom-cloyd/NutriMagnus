"""
test_water.py — water intake: USDA's water value, the per-food / per-recipe
drink flag, and the "from drinks" / "from food" split carried through meal,
recipe and day totals (numa_app/services/water.py).
"""
import json
import pathlib

import pytest
from fastapi.testclient import TestClient

import db as _db
import profile as _profile
import usda as _usda
import web.backend as backend
from numa_app.services import meal_list_columns as _mlc
from numa_app.services import water as _water
from numa_app.services import whatif as _wi
from numa_app.services.recipe_nutrients import recipe_total_nutrients

TEA, APPLE, MILK, DRY = 1, 2, 3, 4


@pytest.fixture(autouse=True)
def use_test_web_prefs(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> None:
    prefs_file = tmp_path / "web_prefs.json"
    prefs_file.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs_file)
    from numa_app.services import manual_build as _manual_build
    monkeypatch.setattr(_manual_build, "rebuild_manual_if_stale", lambda: None)


@pytest.fixture()
def client() -> TestClient:
    return TestClient(backend.app)


@pytest.fixture()
def foods():
    """Tea (a drink), apple, milk (not flagged) and a food with no water value."""
    with _db.get_db() as conn:
        for fdc_id, name, nuts, category in (
            (TEA, "Beverages, tea, brewed", {"calories": 1.0, "water_g": 99.7}, None),
            (APPLE, "Apples, raw", {"calories": 52.0, "water_g": 85.6}, "Fruits and Fruit Juices"),
            (MILK, "Milk, whole", {"calories": 61.0, "protein_g": 3.2, "water_g": 88.0}, "Dairy and Egg Products"),
            (DRY, "Mystery bar", {"calories": 400.0}, None),
        ):
            _db.cache_food(conn, fdc_id=fdc_id, name=name, data_type="SR Legacy", brand=None,
                           serving_size=None, serving_unit=None, nutrients=nuts, category=category)


def _meal(items, date="2026-10-01"):
    with _db.get_db() as conn:
        mid = _db.meal_create(conn, "Lunch", date)
        for kind, item_id, amount in items:
            if kind == "food":
                _db.meal_add_food(conn, mid, item_id, "x", amount, "g")
            else:
                _db.meal_add_recipe(conn, mid, item_id, "r", amount)
    return mid


def _recipe(ingredients, servings=1, name="Smoothie"):
    with _db.get_db() as conn:
        rid = _db.recipe_create(conn, name=name, description="", servings=servings, instructions="")
        for kind, item_id, amount in ingredients:
            if kind == "food":
                _db.recipe_add_ingredient(conn, rid, item_id, "x", amount, "g")
            else:
                _db.recipe_add_ingredient(conn, rid, 0, "sub", amount, "serving", ref_recipe_id=item_id)
    return rid


class TestTag:
    def test_drink_water_goes_to_drinks(self):
        assert _water.tag({"water_g": 90.0}, True) == {"water_g": 90.0, "water_drinks_g": 90.0, "water_food_g": 0.0}

    def test_food_water_goes_to_food(self):
        assert _water.tag({"water_g": 85.0}, False) == {"water_g": 85.0, "water_drinks_g": 0.0, "water_food_g": 85.0}

    def test_no_water_value_adds_no_split(self):
        # "no data" must stay no data — never 0 from drinks and 0 from food
        assert _water.tag({"calories": 400.0}, True) == {"calories": 400.0}

    def test_as_drink_moves_all_water_to_drinks(self):
        total = {"water_g": 300.0, "water_drinks_g": 100.0, "water_food_g": 200.0}
        assert _water.as_drink(total) == {"water_g": 300.0, "water_drinks_g": 300.0, "water_food_g": 0.0}

    @pytest.mark.parametrize("name,category,expected", [
        ("Tea, brewed", "Beverages", True),
        ("Coffee", "Coffee and tea beverages", True),
        ("Beverages, water, tap, drinking", None, True),
        ("Milk, whole", "Dairy and Egg Products", False),
        ("Apples, raw", None, False),
    ])
    def test_looks_like_drink(self, name, category, expected):
        assert _water.looks_like_drink(name, category) is expected


class TestUsdaParse:
    def test_water_and_category_read(self):
        parsed = _usda._parse_food({
            "fdcId": 9, "description": "Tea", "dataType": "SR Legacy",
            "foodCategory": {"description": "Beverages"},
            "foodNutrients": [{"nutrient": {"id": 1051}, "amount": 99.7}],
        })
        assert parsed["nutrients"]["water_g"] == 99.7
        assert parsed["category"] == "Beverages"

    def test_abridged_number_and_branded_category(self):
        parsed = _usda._parse_food({
            "fdcId": 9, "description": "Cola", "brandedFoodCategory": "Soda",
            "foodNutrients": [{"number": "255", "amount": 89.0}],
        })
        assert parsed["nutrients"]["water_g"] == 89.0
        assert parsed["category"] == "Soda"

    def test_split_keys_have_labels_but_are_not_stored_nutrients(self):
        assert _usda.nutrient_label("water_drinks_g") == ("Water from drinks", "g")
        stored = {k for k, _l, _u in _usda.NUTRIENT_MAP.values()}
        assert "water_g" in stored and "water_drinks_g" not in stored


class TestDrinkFlag:
    def test_new_food_guessed_from_category_or_name(self, foods):
        with _db.get_db() as conn:
            assert _water.is_drink(_db.get_cached_food(conn, TEA))
            assert not _water.is_drink(_db.get_cached_food(conn, MILK))

    def test_recache_keeps_users_choice(self, foods):
        with _db.get_db() as conn:
            _db.set_food_is_drink(conn, MILK, True)
            _db.set_food_is_drink(conn, TEA, False)
            _db.cache_food(conn, fdc_id=MILK, name="Milk, whole", data_type="SR Legacy", brand=None,
                           serving_size=None, serving_unit=None, nutrients={"water_g": 88.0})
            _db.cache_food(conn, fdc_id=TEA, name="Beverages, tea, brewed", data_type="SR Legacy", brand=None,
                           serving_size=None, serving_unit=None, nutrients={"water_g": 99.7},
                           category="Beverages")
            assert _water.is_drink(_db.get_cached_food(conn, MILK))
            assert not _water.is_drink(_db.get_cached_food(conn, TEA))


class TestTotals:
    def test_meal_splits_drinks_and_food(self, foods):
        mid = _meal([("food", TEA, 250.0), ("food", APPLE, 200.0), ("food", DRY, 50.0)])
        _, total, _, _ = backend._meal_totals(mid)
        assert total["water_drinks_g"] == pytest.approx(249.25)
        assert total["water_food_g"] == pytest.approx(171.2)
        assert total["water_g"] == pytest.approx(total["water_drinks_g"] + total["water_food_g"])

    def test_recipe_inherits_drink_ingredients(self, foods):
        rid = _recipe([("food", TEA, 200.0), ("food", APPLE, 100.0)])
        with _db.get_db() as conn:
            total = recipe_total_nutrients(rid, conn)
        assert total["water_drinks_g"] == pytest.approx(199.4)
        assert total["water_food_g"] == pytest.approx(85.6)

    def test_drink_recipe_counts_all_its_water_including_sub_recipes(self, foods):
        sub = _recipe([("food", APPLE, 100.0)], name="Apple puree")
        rid = _recipe([("food", MILK, 200.0), ("recipe", sub, 1.0)])
        with _db.get_db() as conn:
            _db.set_recipe_is_drink(conn, rid, True)
            total = recipe_total_nutrients(rid, conn)
            sub_total = recipe_total_nutrients(sub, conn)
        assert total["water_drinks_g"] == pytest.approx(176.0 + 85.6)
        assert total["water_food_g"] == 0.0
        assert sub_total["water_food_g"] == pytest.approx(85.6)   # not a drink on its own

    def test_whatif_matches_meal_page_total(self, foods):
        rid = _recipe([("food", TEA, 200.0), ("food", APPLE, 100.0)], servings=2)
        mid = _meal([("food", MILK, 100.0), ("recipe", rid, 1.0)])
        _, total, _, _ = backend._meal_totals(mid)
        with _db.get_db() as conn:
            wi_total = _wi.meal_nutrients(mid, conn)
        for key in ("water_g", "water_drinks_g", "water_food_g"):
            assert wi_total[key] == pytest.approx(total[key])

    def test_day_total_from_meal_snapshots(self, foods):
        m1 = _meal([("food", TEA, 500.0)])
        m2 = _meal([("food", APPLE, 100.0)])
        backend._compute_and_store_meal_bcp(m1)
        backend._compute_and_store_meal_bcp(m2)
        with _db.get_db() as conn:
            day = _mlc.day_nutrient_raw_totals(conn, "2026-10-01", ["water_drinks_g", "water_food_g"])
        assert day == {"water_drinks_g": pytest.approx(498.5), "water_food_g": pytest.approx(85.6)}

    def test_split_offered_as_column_choice(self):
        keys = [k for k, _l, _u in _mlc.AVAILABLE_NUTRIENTS]
        assert keys.index("water_drinks_g") == keys.index("water_g") + 1
        assert _mlc.sanitize(["water_food_g"]) == ["water_food_g"]


class TestTarget:
    def test_total_water_adequate_intake(self):
        man = _profile.UserProfile(name="m", age=40, sex="male", weight_kg=80, height_cm=180,
                                   activity_level="moderate")
        woman = _profile.UserProfile(name="w", age=40, sex="female", weight_kg=60, height_cm=165,
                                     activity_level="moderate")
        assert _profile.compute_rda(man)["water_g"] == (3700.0, "g", "goal")
        assert _profile.compute_rda(woman)["water_g"][0] == 2700.0


class TestWeb:
    def test_food_page_toggle_cascades_to_meals(self, client, foods):
        mid = _meal([("food", MILK, 200.0)])
        backend._compute_and_store_meal_bcp(mid)
        resp = client.get(f"/food/{MILK}")
        assert 'action="/food/3/drink"' in resp.text
        resp = client.post(f"/food/{MILK}/drink", data={"is_drink": "1"}, follow_redirects=False)
        assert resp.status_code == 303
        with _db.get_db() as conn:
            assert _water.is_drink(_db.get_cached_food(conn, MILK))
            assert mid in _db.stale_meal_ids(conn)
        client.post(f"/food/{MILK}/drink", data={})
        with _db.get_db() as conn:
            assert not _water.is_drink(_db.get_cached_food(conn, MILK))

    def test_marking_a_drink_with_no_water_estimates_it(self, client, foods):
        CIDER = 5
        with _db.get_db() as conn:
            _db.cache_food(conn, fdc_id=CIDER, name="APPLE CIDER", data_type="Branded", brand=None,
                           serving_size=None, serving_unit=None,
                           nutrients={"calories": 50.0, "protein_g": 0.0, "carbs_g": 12.5, "fat_g": 0.0})
        assert "Water estimated as" not in client.get(f"/food/{CIDER}").text
        client.post(f"/food/{CIDER}/drink", data={"is_drink": "1"})
        with _db.get_db() as conn:
            row = _db.get_cached_food(conn, CIDER)
            assert json.loads(row["nutrients_json"])["water_g"] == 87.5
            assert "water_g" in _db.estimated_keys(conn, CIDER)
            assert not row["user_edited"]
        assert "Water estimated as" in client.get(f"/food/{CIDER}").text

    def test_marking_a_drink_keeps_a_measured_water_value(self, client, foods):
        client.post(f"/food/{MILK}/drink", data={"is_drink": "1"})
        with _db.get_db() as conn:
            assert json.loads(_db.get_cached_food(conn, MILK)["nutrients_json"])["water_g"] == 88.0
            assert "water_g" not in _db.estimated_keys(conn, MILK)

    def test_estimate_water(self):
        assert _water.estimate_water({"protein_g": 3.2, "carbs_g": 4.8, "fat_g": 3.3}) == 88.7
        assert _water.estimate_water({"protein_g": 3.2, "carbs_g": 4.8}) is None
        assert _water.estimate_water({"protein_g": 20, "carbs_g": 60, "fat_g": 30}) is None

    def test_recipe_toggle(self, client, foods):
        rid = _recipe([("food", APPLE, 100.0)])
        assert f'action="/recipe/{rid}/drink"' in client.get(f"/recipe/{rid}").text
        client.post(f"/recipe/{rid}/drink", data={"is_drink": "1"})
        with _db.get_db() as conn:
            assert _water.is_drink(_db.recipe_get(conn, rid))

    def test_toggle_returns_only_to_a_local_page(self, client, foods):
        resp = client.post(f"/food/{MILK}/drink", data={"is_drink": "1", "next": "https://evil.example/"},
                           follow_redirects=False)
        assert resp.headers["location"].startswith(f"/food/{MILK}")

    def test_meal_page_shows_split_rows(self, client, foods):
        mid = _meal([("food", TEA, 250.0), ("food", APPLE, 200.0)])
        text = client.get(f"/meal/{mid}").text
        assert "Water from drinks" in text and "Water from food" in text

    def test_food_page_shows_water_without_split(self, client, foods):
        text = client.get(f"/food/{APPLE}").text
        assert "Water" in text and "Water from drinks" not in text

    def test_food_use_page_has_drink_column(self, client, foods):
        rid = _recipe([("food", APPLE, 100.0)])
        _meal([("food", TEA, 250.0), ("recipe", rid, 1.0)])
        text = client.get("/analysis/food-use",
                          params={"mode": "range", "ranges_raw": "2026-10-01:2026-10-01"}).text
        assert f'action="/food/{TEA}/drink"' in text
        assert f'action="/recipe/{rid}/drink"' in text
        resp = client.post(f"/food/{APPLE}/drink",
                           data={"is_drink": "1", "next": "/analysis/food-use?mode=range"},
                           follow_redirects=False)
        assert resp.headers["location"] == "/analysis/food-use?mode=range"


class TestBackfill:
    @pytest.fixture()
    def usda_foods(self):
        """Three USDA foods without water (one marked "Water not needed"), one
        with it, and a custom food — plus a recipe and a meal using one."""
        with _db.get_db() as conn:
            for fdc_id, name, nuts in ((171688, "Apples, raw", {"calories": 52.0}),
                                       (174158, "Water, bottled", {"calories": 0.0}),
                                       (999001, "Mystery", {"calories": 10.0}),
                                       (999002, "Ignored", {"calories": 10.0}),
                                       (2346405, "Celery", {"calories": 14.0, "water_g": 95.0})):
                _db.cache_food(conn, fdc_id=fdc_id, name=name, data_type="SR Legacy", brand=None,
                               serving_size=None, serving_unit=None, nutrients=nuts)
            conn.execute("INSERT INTO foods (fdc_id, name, nutrients_json) VALUES (-5, 'Mine', '{}')")
            _db.set_food_data_ignore(conn, 999002, "water", True)
            rid = _db.recipe_create(conn, name="Apple bowl", description="", servings=1, instructions="")
            _db.recipe_add_ingredient(conn, rid, 171688, "Apples", 100.0, "g")
            mid = _db.meal_create(conn, "Snack", "2026-10-01")
            _db.meal_add_food(conn, mid, 171688, "Apples", 100.0, "g")
        return {"rid": rid, "mid": mid}

    def test_candidates_are_usda_foods_missing_water_not_ignored(self, usda_foods):
        from numa_app.services import water_backfill as _wb
        with _db.get_db() as conn:
            assert _wb.candidates(conn) == [171688, 174158, 999001]

    def test_run_fills_blanks_only_and_cascades(self, usda_foods, monkeypatch):
        from numa_app.services import water_backfill as _wb
        asked = []

        def fake(ids):
            asked.append(list(ids))
            return {171688: 85.6, 174158: 100.0}
        monkeypatch.setattr(_usda, "get_water_values", fake)
        _wb.clear_status()
        _wb.run()
        assert asked == [[171688, 174158, 999001]]
        with _db.get_db() as conn:
            apple = _db.get_cached_food(conn, 171688)
            assert json.loads(apple["nutrients_json"])["water_g"] == 85.6
            assert not apple["user_edited"]          # source data, not the user's edit
            assert _db.food_edited_keys(conn, 171688) == []
            assert json.loads(_db.get_cached_food(conn, 2346405)["nutrients_json"])["water_g"] == 95.0
            assert usda_foods["mid"] in _db.stale_meal_ids(conn)
            assert recipe_total_nutrients(usda_foods["rid"], conn)["water_food_g"] == pytest.approx(85.6)
            assert _wb.candidates(conn) == [999001]
        st = _wb.status()
        assert st["filled"] == 2 and st["no_value"] == ["Mystery"] and st["error"] is None

    def test_failed_request_keeps_earlier_batches(self, usda_foods, monkeypatch):
        from numa_app.services import water_backfill as _wb
        monkeypatch.setattr(_wb, "_BATCH", 1)
        calls = []

        def fake(ids):
            calls.append(ids)
            if len(calls) == 2:
                raise _usda.USDAError("USDA API 429: rate limit hit")
            return {ids[0]: 50.0}
        monkeypatch.setattr(_usda, "get_water_values", fake)
        _wb.clear_status()
        _wb.run()
        st = _wb.status()
        assert st["filled"] == 1 and "429" in st["error"]
        with _db.get_db() as conn:
            assert _wb.candidates(conn) == [174158, 999001]

    def test_get_water_values_batches_by_20(self, monkeypatch):
        import usda_api
        seen = []

        def fake_get(path, params):
            ids = [int(x) for x in params["fdcIds"].split(",")]
            seen.append((path, len(ids), params["nutrients"]))
            return [{"fdcId": i, "foodNutrients": [{"number": "255", "amount": 80.0}]} for i in ids if i % 2]
        monkeypatch.setattr(usda_api, "_get", fake_get)
        values = usda_api.get_water_values(list(range(1, 46)))
        assert [n for _p, n, _ in seen] == [20, 20, 5]
        assert seen[0][0] == "foods" and seen[0][2] == "255"
        assert set(values) == set(range(1, 46, 2)) and values[1] == 80.0

    def test_db_check_page_offers_button(self, client, usda_foods):
        text = client.get("/food/cache/db-check").text
        assert 'action="/food/cache/water-backfill"' in text
        assert "Fill in water for 3 USDA foods from USDA" in text


WET_OKARA, OKARA_FLOUR = 172452, 2396330


@pytest.fixture()
def okara():
    """USDA's wet okara and a dry okara flour, both with water; a recipe and a
    meal that use the wet one under the name "okara flour"."""
    with _db.get_db() as conn:
        _db.cache_food(conn, fdc_id=WET_OKARA, name="Okara", data_type="SR Legacy", brand=None,
                       serving_size=None, serving_unit=None,
                       nutrients={"calories": 76.0, "protein_g": 3.5, "water_g": 81.6})
        _db.cache_food(conn, fdc_id=OKARA_FLOUR, name="Pure Okara Flour (dried)", data_type="Branded",
                       brand=None, serving_size=None, serving_unit=None,
                       nutrients={"calories": 350.0, "protein_g": 25.0, "water_g": 8.0})
        rid = _db.recipe_create(conn, name="Okara bread", description="", servings=1, instructions="")
        _db.recipe_add_ingredient(conn, rid, WET_OKARA, "okara flour", 50.0, "g")
        _db.recipe_add_ingredient(conn, rid, OKARA_FLOUR, "Pure Okara Flour (dried)", 50.0, "g")
        mid = _db.meal_create(conn, "Breakfast", "2026-10-01")
        _db.meal_add_food(conn, mid, WET_OKARA, "Okara flour", 30.0, "g")
    return {"rid": rid, "mid": mid}


class TestWetDry:
    @pytest.mark.parametrize("name,word", [
        ("okara flour", "flour"),
        ("Cocoa, dry powder, unsweetened", "dry"),
        ("Plums, dried (prunes), uncooked", "dried"),
        ("Beverages, chocolate powder, prepared with milk", None),
        ("Tomatoes, sun-dried, packed in oil", None),
        ("Wine, table, white, dry", None),
        ("Okara (wet pulp, as pressed — about 82% water)", None),
        ("Oatmeal, cooked", None),
        ("Apples, raw", None),
    ])
    def test_dry_word(self, name, word):
        assert _water.dry_word(name) == word

    def test_conflict_needs_dry_name_and_high_water(self):
        assert _water.wet_dry_conflict(["Okara", "okara flour"], {"water_g": 81.6})["word"] == "flour"
        assert _water.wet_dry_conflict(["Plums, dried (prunes)"], {"water_g": 30.9}) is None  # truly dried
        assert _water.wet_dry_conflict(["okara flour"], {"calories": 76.0}) is None          # no water: no verdict
        assert _water.wet_dry_conflict(["Okara"], {"water_g": 81.6}) is None

    def test_foods9_list_names_where_used(self, client, okara):
        from numa_app.services import data_quality as _dq
        with _db.get_db() as conn:
            rows = _dq.wet_dry_in_use(conn)
        assert [r["fdc_id"] for r in rows] == [WET_OKARA]
        assert [w["id"] for w in rows[0]["recipes"]] == [okara["rid"]]
        assert [w["id"] for w in rows[0]["meals"]] == [okara["mid"]]
        text = client.get("/food/cache/db-check").text
        assert 'id="wet-dry"' in text and "Named dry, but mostly water (1)" in text

    def test_recipe_and_meal_rows_flag_the_wet_one_only(self, client, okara):
        text = client.get(f"/recipe/{okara['rid']}").text
        assert "82% water &mdash; but named flour?" in text
        assert "(8% water)" in text                     # the real flour: just its water
        assert "Named dry, but mostly water" in text    # footnote
        assert "82% water &mdash; but named flour?" in client.get(f"/recipe/{okara['rid']}/edit").text
        assert "82% water &mdash; but named flour?" in client.get(f"/meal/{okara['mid']}").text


class TestTrackWaterSwitch:
    def test_on_by_default(self, client, foods):
        assert backend._track_water()
        assert 'id="water-tracking"' in client.get("/settings").text

    def test_off_hides_water_everywhere_and_keeps_data(self, client, foods, okara):
        resp = client.post("/settings/water", data={}, follow_redirects=False)
        assert resp.status_code == 303 and not backend._track_water()
        mid = _meal([("food", TEA, 250.0), ("food", APPLE, 200.0)])
        assert "Water from drinks" not in client.get(f"/meal/{mid}").text
        assert 'id="drink-toggle"' not in client.get(f"/food/{APPLE}").text
        assert "but named flour?" not in client.get(f"/recipe/{okara['rid']}").text
        db_check = client.get("/food/cache/db-check").text
        assert 'id="water-backfill"' not in db_check and 'id="wet-dry"' not in db_check
        use = client.get("/analysis/food-use", params={"mode": "range", "ranges_raw": "2026-10-01:2026-10-01"}).text
        assert f'action="/food/{TEA}/drink"' not in use
        _, total, _, _ = backend._meal_totals(mid)        # still summed, just not shown
        assert total["water_drinks_g"] > 0
        client.post("/settings/water", data={"track_water": "1"})
        assert "Water from drinks" in client.get(f"/meal/{mid}").text

    def test_off_drops_water_from_pickers(self, client):
        client.post("/settings/water", data={})
        assert 'value="water_drinks_g"' not in client.get("/settings").text
        assert not any(k in _water.ALL_KEYS for _g, keys in backend._shown_groups(backend._NUTRIENT_GROUPS) for k in keys)


class TestOlderAdultsAndShare:
    def _p(self, age, sex):
        return _profile.UserProfile(name="p", age=age, sex=sex, weight_kg=70, height_cm=170,
                                    activity_level="moderate")

    def test_drinks_goal_is_iom_at_any_age(self):
        assert _profile.compute_rda(self._p(40, "female"))["water_drinks_g"] == (2200.0, "g", "goal")
        assert _profile.compute_rda(self._p(80, "male"))["water_drinks_g"][0] == 3000.0

    def test_espen_floor_from_65_only(self):
        assert _profile.drinks_floor(self._p(64, "female")) is None
        assert _profile.drinks_floor(self._p(65, "female")) == 1600.0
        assert _profile.drinks_floor(self._p(80, "male")) == 2000.0
        assert _profile.drinks_floor(None) is None

    def test_floor_warning_on_drinks_row_only_when_below(self):
        def label(drinks):
            return [r["label"] for s in backend._nutrient_sections(
                {"water_g": drinks + 500.0, "water_drinks_g": drinks, "water_food_g": 500.0},
                drinks_floor=1600.0) for r in s["rows"] if r["label"].startswith("Water from drinks")][0]
        assert "below the 1.6 L a day of drinks" in label(1200.0)
        assert label(1700.0) == "Water from drinks"

    def test_day_page_warns_for_older_profile(self, client, foods, monkeypatch):
        monkeypatch.setattr(_profile, "load_profile", lambda *a, **k: self._p(70, "female"))
        _meal([("food", TEA, 500.0)])
        assert "recommended as a minimum from age 65 (ESPEN)" in client.get("/summary/2026-10-01").text

    def test_food_share_in_label(self):
        rows = {r["label"]: r for s in backend._nutrient_sections(
            {"water_g": 400.0, "water_drinks_g": 300.0, "water_food_g": 100.0}) for r in s["rows"]}
        assert "Water from food (25% of the total)" in rows


class TestReferenceAndLimits:
    """IOM/EFSA choice, water's "goal" status, a fluid limit, and the two
    day-page notes (NICE weight-based figure, high protein)."""

    def _p(self, sex="female", ref="iom", weight=70.0, height=170.0, age=40):
        return _profile.UserProfile(name="p", age=age, sex=sex, weight_kg=weight, height_cm=height,
                                    activity_level="moderate", water_reference=ref)

    def test_efsa_goals(self):
        rda = _profile.compute_rda(self._p("male", "efsa"))
        assert rda["water_g"] == (2500.0, "g", "goal")
        assert rda["water_drinks_g"][0] == 2000.0
        rda = _profile.compute_rda(self._p("female", "efsa"))
        assert (rda["water_g"][0], rda["water_drinks_g"][0]) == (2000.0, 1600.0)

    def test_reference_survives_save_and_day_snapshot(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_profile, "_PROFILES_DIR", tmp_path)
        _profile.save_profile(self._p(ref="efsa"))
        assert _profile.load_profile("p").water_reference == "efsa"
        from numa_app.services import day_profile as _dp
        assert _dp._from_snapshot({"profile_json": _dp._snapshot(self._p(ref="efsa"))}).water_reference == "efsa"
        # A profile saved before the choice existed reads as IOM.
        (tmp_path / "old.json").write_text(json.dumps(
            {"age": 40, "sex": "male", "weight_kg": 70, "height_cm": 170, "activity_level": "moderate"}))
        assert _profile.load_profile("old").water_reference == "iom"

    def test_past_goal_is_plain_not_met(self):
        from numa_app.services.rda_status import rda_status
        assert rda_status(120, "goal") == "reached"
        assert rda_status(85, "goal") == "near" and rda_status(40, "goal") == "low"
        rows = {r["label"]: r for s in backend._nutrient_sections(
            {"water_g": 4000.0}, _profile.compute_rda(self._p())) for r in s["rows"]}
        assert rows["Water"]["rda_css"] == "rda-reached"
        assert rows["Water"]["rda_minimum"] == "2700.0 g"

    def test_fluid_limit_drops_colour_and_older_warning(self):
        rda = _profile.compute_rda(self._p(age=70))
        n = {"water_g": 1000.0, "water_drinks_g": 800.0, "water_food_g": 200.0}
        def rows(limits):
            return {r["label"].split(" —")[0]: r for s in backend._nutrient_sections(
                n, rda, n, max_limits=limits, drinks_floor=1600.0) for r in s["rows"]}
        free = rows({})
        assert free["Water"]["rda_css"] == "rda-low"
        assert "below the 1.6 L" in [r["label"] for r in free.values() if r["label"].startswith("Water from drinks")][0]
        capped = rows({"water_drinks_g": 1500.0})
        assert capped["Water"]["rda_css"] is None and capped["Water from drinks"]["rda_css"] is None
        assert capped["Water from drinks"]["label"] == "Water from drinks"
        assert capped["Water from drinks"]["ul_display"] == "1500 g"

    def test_drinks_max_limit_is_settable(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(_profile, "_PROFILES_DIR", tmp_path)
        _profile.save_profile(self._p())
        monkeypatch.setattr(_profile, "get_active_profile_name", lambda: "p")
        assert 'name="key" value="water_drinks_g"' in client.get("/settings").text
        client.post("/settings/nutrient-target", data={"key": "water_drinks_g", "optimal": "", "limit": "1500"})
        assert _profile.load_profile("p").max_limits == {"water_drinks_g": 1500.0}

    def test_settings_choice_saves_and_survives_water_off(self, client, tmp_path, monkeypatch):
        monkeypatch.setattr(_profile, "_PROFILES_DIR", tmp_path)
        _profile.save_profile(self._p())
        monkeypatch.setattr(_profile, "get_active_profile_name", lambda: "p")
        assert 'name="water_reference"' in client.get("/settings").text
        form = {"age": "40", "sex": "female", "weight": "70", "weight_unit": "kg",
                "height_cm": "170", "height_unit": "cm", "activity_level": "moderate"}
        client.post("/settings", data={**form, "water_reference": "efsa"})
        assert _profile.load_profile("p").water_reference == "efsa"
        # Water tracking off hides the choice; saving the profile keeps it.
        backend._save_prefs_file({"track_water": False})
        assert 'name="water_reference"' not in client.get("/settings").text
        client.post("/settings", data=form)
        assert _profile.load_profile("p").water_reference == "efsa"

    def test_nice_band(self):
        band = _profile.nice_water_band(self._p(weight=60.0))
        assert (band["low"], band["high"], band["ideal_weight"]) == (1500.0, 1800.0, False)
        # Capped at 3 L.
        assert _profile.nice_water_band(self._p(weight=115.0, height=200.0))["high"] == 3000.0
        # BMI 30+: ideal body weight (Devine). 160 cm woman: 45.5 + 2.3 x 2.99 in ~ 52.4 kg.
        band = _profile.nice_water_band(self._p(weight=100.0, height=160.0))
        assert band["ideal_weight"] and band["weight_kg"] == pytest.approx(52.4, abs=0.1)
        assert _profile.nice_water_band(None) is None

    def test_day_notes(self, monkeypatch):
        rda = _profile.compute_rda(self._p())
        notes = backend._water_day_notes({"protein_g": rda["protein_g"][0] * 2}, rda, self._p(), {})
        assert "1.8–2.1 L of total water" in notes["nice"]
        assert "below your IOM goal of 2.7 L, which stays your goal" in notes["nice"]
        assert "well above your goal" in notes["protein"]
        assert backend._water_day_notes({"protein_g": rda["protein_g"][0]}, rda, self._p(), {})["protein"] is None
        # Under a fluid limit, neither note.
        assert backend._water_day_notes({"protein_g": 500.0}, rda, self._p(),
                                        {"water_g": 1500.0}) == {"nice": None, "protein": None}

    def test_notes_on_day_page(self, client, foods, monkeypatch):
        monkeypatch.setattr(_profile, "load_profile", lambda *a, **k: self._p())
        _meal([("food", TEA, 500.0)])
        text = client.get("/summary/2026-10-01").text
        assert "NICE starts routine fluid maintenance" in text
