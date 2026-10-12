"""
Tests for numa_app/services/top_contributors.py's missing_contributors():
the foods a Top Contributors ranking can't count because they have no data
for the nutrient (an absent key; a stored 0 is data), or, for DCP, no amino
acid data. Ranking itself is covered through the web pages in test_web.py
and, for glycemic load, test_gl_swaps.py. Also source_anchor() and
fill_url(): where that list sends you to find the missing data.
"""


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
