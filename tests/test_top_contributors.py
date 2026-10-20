"""
Tests for numa_app/services/top_contributors.py's missing_contributors():
the foods a Top Contributors ranking can't count because they have no data
for the nutrient (an absent key; a stored 0 is data), or, for DCP, no amino
acid data. Ranking itself is covered through the web pages in test_web.py
and, for glycemic load, test_gl_swaps.py. Also source_anchor() and
fill_url(): where that list sends you to find the missing data. And
rank_by_meal_item(): the meal page's by-item table, recipes kept whole.
"""
import pytest



def test_missing_contributors_lists_absent_keys_only() -> None:
    from numa_app.services.top_contributors import missing_contributors
    ings = [
        {"food_name": "Has", "fdc_id": 1, "nutrients_100g": {"iron_mg": 2.0}, "grams": 50},
        {"food_name": "Zero", "fdc_id": 2, "nutrients_100g": {"iron_mg": 0.0}, "grams": 50},
        {"food_name": "None", "fdc_id": 3, "nutrients_100g": {"calories": 10}, "grams": 40},
        {"food_name": "None", "fdc_id": 3, "nutrients_100g": {"calories": 10}, "grams": 30},
        {"food_name": "Heavy", "fdc_id": 4, "nutrients_100g": {}, "grams": 200},
        {"food_name": "Unused", "fdc_id": 5, "nutrients_100g": {}, "grams": 0},
    ]
    out = missing_contributors(ings, "iron_mg")
    assert [(m["food_name"], m["grams"]) for m in out] == [("Heavy", 200), ("None", 70)]


def test_missing_contributors_dcp_means_no_amino_acid_data() -> None:
    from numa_app.services.top_contributors import missing_contributors
    aa = {k: 1.0 for k in ["aa_lysine_g", "aa_leucine_g", "aa_valine_g", "aa_threonine_g", "aa_histidine_g"]}
    ings = [
        {"food_name": "Beans", "fdc_id": 1, "nutrients_100g": {"protein_g": 20, **aa}, "grams": 100},
        {"food_name": "Seitan", "fdc_id": 2, "nutrients_100g": {"protein_g": 25}, "grams": 100},
        {"food_name": "Oil", "fdc_id": 3, "nutrients_100g": {"protein_g": 0}, "grams": 10},
        {"food_name": "Mystery", "fdc_id": 4, "nutrients_100g": {}, "grams": 5},
    ]
    assert [m["food_name"] for m in missing_contributors(ings, "protein_g", is_dcp=True)] == ["Seitan", "Mystery"]


def test_every_rankable_nutrient_has_a_where_to_find_it_entry() -> None:
    """Each nutrient the no-data list can name links to an anchor that
    exists in the manual's Appendix G, with its own "Where to find it" line."""
    import re
    from pathlib import Path
    from web.backend import _NUTRIENT_GROUPS
    from numa_app.services.top_contributors import source_anchor
    manual = (Path(__file__).parent.parent / "user-manual.md").read_text()
    anchors = set(re.findall(r"\{: #([\w-]+)\}", manual))
    keys = [k for _g, ks in _NUTRIENT_GROUPS for k in ks]
    for key in keys:
        a = source_anchor(key)
        assert a != "key-sources", f"{key} has no Appendix G entry of its own"
        assert a in anchors, f"{key} -> #{a} is not in the manual"
        entry = manual[manual.index("{: #" + a + "}") + 1:]
        entry = entry[:entry.index("{: #key-")] if "{: #key-" in entry else entry
        assert "**Where to find it:**" in entry, key
    assert source_anchor("protein_g", is_dcp=True) == "key-sources-aa" in anchors
    assert source_anchor("unknown_key") == "key-sources" in anchors


def test_fill_url_searches_for_the_food_by_name() -> None:
    from urllib.parse import parse_qs, urlsplit
    from numa_app.services.top_contributors import fill_url
    u = urlsplit(fill_url({"food_name": "* Tomato sauce", "fdc_id": 42, "recipe_id": None}, "water_g"))
    assert u.path == "/food/42/fill-from"
    assert parse_qs(u.query) == {"q": ["Tomato sauce"], "want": ["water_g"]}
    assert "want=aa" in fill_url({"food_name": "Seitan", "fdc_id": 7}, "protein_g", is_dcp=True)
    assert fill_url({"food_name": "Mine", "fdc_id": -3}, "iron_mg", custom_profile=True) == \
        "/food/custom-profiles/-3/edit?nutrient_source_q=Mine"
    assert "aa_source_q=Mine" in fill_url({"food_name": "Mine", "fdc_id": -3}, "protein_g",
                                           is_dcp=True, custom_profile=True)
    assert fill_url({"food_name": "Stew", "fdc_id": None, "recipe_id": 5}, "iron_mg") is None
    assert fill_url({"food_name": "Name only", "fdc_id": None}, "iron_mg") is None


def test_missing_contributors_flags_not_needed_and_has_none() -> None:
    """"ignored": the nutrient or its whole group is marked not needed (DCP:
    amino acids); "can_zero": a 0 can be recorded (DCP: only when there's no
    protein figure — a food with protein has amino acids)."""
    from numa_app.services.top_contributors import missing_contributors
    ings = [
        {"food_name": "A", "fdc_id": 1, "nutrients_100g": {}, "grams": 30},
        {"food_name": "B", "fdc_id": 2, "nutrients_100g": {}, "grams": 20},
        {"food_name": "C", "fdc_id": 3, "nutrients_100g": {}, "grams": 10},
    ]
    ignores = {1: {"iodine_mcg"}, 2: {"minerals"}, 3: {"iron_mg"}}
    out = missing_contributors(ings, "iodine_mcg", ignores=ignores)
    assert [(m["food_name"], m["ignored"], m["can_zero"]) for m in out] == [
        ("A", True, True), ("B", True, True), ("C", False, True)]

    dcp = [{"food_name": "Seitan", "fdc_id": 1, "nutrients_100g": {"protein_g": 25}, "grams": 50},
           {"food_name": "Mystery", "fdc_id": 2, "nutrients_100g": {}, "grams": 5}]
    out = missing_contributors(dcp, "protein_g", is_dcp=True, ignores={2: {"aa"}})
    assert [(m["food_name"], m["ignored"], m["can_zero"]) for m in out] == [
        ("Seitan", False, False), ("Mystery", True, True)]


def test_data_completeness_gap_helpers() -> None:
    from numa_app.services import data_completeness as dc
    assert dc.ignore_key("iodine_mcg") == "iodine_mcg"
    assert dc.ignore_key("water_g") == "water"          # a one-nutrient group
    assert dc.ignore_key("aa_lysine_g", is_dcp=True) == "aa"
    assert dc.none_keys({"iron_mg": 1}, "iron_mg") == []
    assert dc.none_keys({}, "iron_mg") == ["iron_mg"]
    assert dc.none_keys({"protein_g": 3}, "protein_g", is_dcp=True) == []
    assert dc.none_keys({}, "protein_g", is_dcp=True) == ["protein_g"]
    assert dc.group_none_keys({"calories": 0, "fat_g": 0}, "macros") == [
        "protein_g", "carbs_g", "fiber_g", "sugar_g", "saturated_fat_g", "mono_fat_g", "poly_fat_g"]
    assert dc.group_none_keys({}, "aa") == []


def _leaf(name, fid, grams, iron, item_id, item_name, recipe_id=None):
    return {"food_name": name, "fdc_id": fid, "grams": grams, "nutrients_100g": {"iron_mg": iron},
            "item_id": item_id, "item_name": item_name,
            "item_fdc_id": None if recipe_id else fid, "item_recipe_id": recipe_id}


def test_rank_by_meal_item_keeps_a_recipe_whole() -> None:
    from numa_app.services.top_contributors import rank_by_meal_item
    leaves = [_leaf("Lentils", 1, 200, 3.0, 10, "Dal", recipe_id=7),     # 6 mg
              _leaf("Spinach", 2, 100, 2.5, 10, "Dal", recipe_id=7),     # 2.5 mg
              _leaf("Tofu", 3, 100, 5.0, 11, "Tofu")]                    # 5 mg
    result = rank_by_meal_item(leaves, "iron_mg", None)
    assert [(c["food_name"], c["recipe_id"], c["fdc_id"], round(c["amount"], 1)) for c in result["items"]] == [
        ("Dal", 7, None, 8.5), ("Tofu", None, 3, 5.0)]
    assert round(result["total"], 1) == 13.5
    # Leaves with no meal item (a recipe page's own) aren't ranked here.
    assert rank_by_meal_item([{**leaves[0], "item_id": None}], "iron_mg", None)["items"] == []


@pytest.fixture()
def client(tmp_path, monkeypatch):
    import json
    from fastapi.testclient import TestClient
    from web import backend
    from numa_app.services import manual_build
    prefs = tmp_path / "prefs.json"
    prefs.write_text(json.dumps({}))
    monkeypatch.setattr(backend, "_PREFS_FILE", prefs)
    monkeypatch.setattr(manual_build, "rebuild_manual_if_stale", lambda: None)
    return TestClient(backend.app)


def test_meal_page_shows_the_by_item_table_only_with_a_recipe(client) -> None:
    import db as _db
    with _db.get_db() as conn:
        for fid, name, iron in ((998101, "Lentil tc", 3.0), (998102, "Spinach tc", 2.5), (998103, "Tofu tc", 5.0)):
            _db.cache_food(conn, fid, name, "SR Legacy", None, 100.0, "g",
                           {"calories": 100.0, "protein_g": 5.0, "carbs_g": 10.0, "fat_g": 1.0, "iron_mg": iron}, [])
        rid = _db.recipe_create(conn, "Dal tc", "", 2, "")
        _db.recipe_add_ingredient(conn, rid, 998101, "Lentil tc", 400, "g")
        _db.recipe_add_ingredient(conn, rid, 998102, "Spinach tc", 200, "g")
        mid = _db.meal_create(conn, "Supper", "2026-10-14")
        _db.meal_add_food(conn, mid, 998103, "Tofu tc", 100, "g")
    page = client.get(f"/meal/{mid}?rank=iron_mg").text
    assert 'id="contrib-by-item"' not in page                       # no recipe: nothing to keep whole
    assert 'id="contrib-by-food"' not in page and 'href="#contrib-by-food"' not in page
    with _db.get_db() as conn:
        _db.meal_add_recipe(conn, mid, rid, "Dal tc", 1)
    page = client.get(f"/meal/{mid}?rank=iron_mg").text
    assert 'id="contrib-by-item"' in page
    # Both tables get a heading, each listed under Top Contributors in the sidebar.
    assert page.index('id="contrib-by-food"') < page.index('id="contrib-by-item"')
    assert 'href="#contrib-by-food"' in page and 'href="#contrib-by-item"' in page
    by_item = page[page.index('id="contrib-by-item"'):]
    assert by_item.index("Dal tc") < by_item.index("Tofu tc")       # 8.5 mg beats 5 mg
    assert "Lentil tc" not in by_item.split("</table>")[0]
    # Protein ranks by each item's standalone DCP, glycemic load by its GL.
    for rank, heading in (("protein_g", "Digestible Complete Protein (standalone)"), ("gl", "Glycemic load")):
        resp = client.get(f"/meal/{mid}?rank={rank}")
        assert resp.status_code == 200
        assert 'id="contrib-by-item"' in resp.text


def test_by_item_splits_a_food_shared_by_two_recipes(client) -> None:
    """Tap water in two recipes of one meal is merged into one food row for
    the food-level table; the by-item table must still give each recipe its
    own water, not all of it to the first (seen on a real meal, 2026-10-14)."""
    import db as _db
    from web import backend
    from numa_app.services.top_contributors import rank_by_meal_item
    with _db.get_db() as conn:
        _db.cache_food(conn, 998201, "Water tc", "SR Legacy", None, 100.0, "g", {"water_g": 100.0}, [])
        _db.cache_food(conn, 998202, "Coffee tc", "SR Legacy", None, 100.0, "g", {"water_g": 3.0}, [])
        coffee = _db.recipe_create(conn, "Coffee drink tc", "", 1, "")
        _db.recipe_add_ingredient(conn, coffee, 998201, "Water tc", 500, "g")
        _db.recipe_add_ingredient(conn, coffee, 998202, "Coffee tc", 10, "g")
        soup = _db.recipe_create(conn, "Soup tc", "", 1, "")
        _db.recipe_add_ingredient(conn, soup, 998201, "Water tc", 473, "g")
        mid = _db.meal_create(conn, "Breakfast", "2026-10-14")
        _db.meal_add_recipe(conn, mid, coffee, "Coffee drink tc", 1)
        _db.meal_add_recipe(conn, mid, soup, "Soup tc", 1)
    _items, totals, _diaas, leaves = backend._meal_totals(mid)
    with _db.get_db() as conn:
        result = rank_by_meal_item(leaves, "water_g", conn)
    assert {c["food_name"]: round(c["amount"], 1) for c in result["items"]} == {
        "Coffee drink tc": 500.3, "Soup tc": 473.0}
    assert round(result["total"], 1) == round(totals["water_g"], 1)
