"""
Tests for numa_app/services/top_contributors.py's missing_contributors():
the foods a Top Contributors ranking can't count because they have no data
for the nutrient (an absent key; a stored 0 is data), or, for DCP, no amino
acid data. Ranking itself is covered through the web pages in test_web.py
and, for glycemic load, test_gl_swaps.py.
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
