"""
Tests for GL contributor ranking (top_contributors.rank_contributors_by_gl)
and lower-GL swap suggestions (numa_app/services/gl_swaps.py), plus the
meal page's Top Contributors "rank by glycemic load" view.
"""
import json
import re

import pytest

import db as _db
from numa_app.services.gl_swaps import suggest_swaps
from numa_app.services.top_contributors import rank_contributors_by_gl

WHITE, BROWN, BARLEY, POTATO, BREAD, COLA = 971, 972, 973, 974, 975, 976


def _food(conn, fid, name, carbs, gi=None, archived=0):
    conn.execute("INSERT INTO foods (fdc_id, name, data_type, nutrients_json, portions_json, archived) "
                 "VALUES (?,?,?,?,?,?)", (fid, name, "SR Legacy", json.dumps({"carbs_g": carbs}), "[]", archived))
    if gi is not None:
        _db.set_food_annotation(conn, fid, gi_estimate=gi, gi_no_prompt=False, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None)


@pytest.fixture()
def foods(db_conn):
    _food(db_conn, WHITE, "Rice, white, cooked", 28.0, gi=73)
    _food(db_conn, BROWN, "Rice, brown, cooked", 26.0, gi=68)
    _food(db_conn, BARLEY, "Barley, pearled, cooked", 28.0, gi=28)
    _food(db_conn, POTATO, "Potato, baked", 21.0, gi=85)
    _food(db_conn, BREAD, "Bread, rye", 48.0)               # no GI
    _food(db_conn, COLA, "Cola", 10.0, gi=63)                # carbs too different
    db_conn.commit()


def _leaf(fid, name, carbs, grams):
    return {"food_name": name, "fdc_id": fid, "nutrients_100g": {"carbs_g": carbs}, "grams": grams}


def test_rank_by_gl_sums_to_meal_gl_and_lists_no_gi_foods(foods, db_conn):
    leaves = [_leaf(WHITE, "Rice, white, cooked", 28.0, 200.0), _leaf(POTATO, "Potato, baked", 21.0, 100.0),
              _leaf(BREAD, "Bread, rye", 48.0, 50.0), _leaf(WHITE, "Rice, white, cooked", 28.0, 50.0)]
    r = rank_contributors_by_gl(leaves, db_conn)
    assert [i["fdc_id"] for i in r["items"]] == [WHITE, POTATO]
    rice = r["items"][0]
    assert rice["grams"] == 250.0 and rice["amount"] == pytest.approx(73 * 70 / 100)
    assert r["total"] == pytest.approx(73 * 70 / 100 + 85 * 21 / 100)
    assert [g["name"] for g in r["gaps"]] == ["Bread, rye"]
    assert r["coverage_pct"] == round((70 + 21) / (70 + 21 + 24) * 100)


def test_swaps_prefer_shared_name_words_then_bigger_saving(foods, db_conn):
    items = rank_contributors_by_gl([_leaf(WHITE, "Rice, white, cooked", 28.0, 200.0)], db_conn)["items"]
    out = suggest_swaps(db_conn, items)
    names = [s["name"] for s in out[0]["swaps"]]
    # Brown rice shares "rice" and is first despite the smaller saving; cola's
    # carbohydrate per 100 g is too different; potato has a higher GI.
    assert names == ["Rice, brown, cooked", "Barley, pearled, cooked"]
    barley = out[0]["swaps"][1]
    assert barley["gl_after"] == pytest.approx(28 * 28 * 200 / 10000)


def test_no_swap_for_a_small_gi_drop_or_archived_food(db_conn):
    _food(db_conn, WHITE, "Rice, white", 28.0, gi=73)
    _food(db_conn, BROWN, "Rice, brown", 28.0, gi=70)            # only 3 lower
    _food(db_conn, BARLEY, "Barley", 28.0, gi=28, archived=1)
    db_conn.commit()
    items = rank_contributors_by_gl([_leaf(WHITE, "Rice, white", 28.0, 200.0)], db_conn)["items"]
    assert suggest_swaps(db_conn, items) == []


def test_meal_page_ranks_by_gl_and_links_swaps_to_whatif(foods, db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    client = TestClient(backend.app)
    meal_id = int(client.post("/meals/create", data={"name": "Dinner", "meal_date": "2026-07-13"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    for fid, name in ((WHITE, "Rice, white, cooked"), (BREAD, "Bread, rye")):
        client.post(f"/meal/{meal_id}/add", data={"fdc_id": fid, "food_name": name, "portion_str": "200 g"},
                    follow_redirects=False)
    html = client.get(f"/meal/{meal_id}").text
    assert f"/meal/{meal_id}?rank=gl#sec-contributors" in html
    assert 'value="gl"' in html
    html = client.get(f"/meal/{meal_id}?rank=gl").text
    assert "Lower-glycemic swaps to try" in html
    assert "Barley, pearled, cooked" in html
    assert "e_op=replace" in html and f"meal_ids={meal_id}" in html and f"e_with=U{BARLEY}" in html
    assert f'href="/food/annotate/{BREAD}"' in html            # no-GI food named
    # The swaps say they come only from foods with a GI, and point to the list.
    assert "Suggestions come only from the 5 foods you" in html
    assert "1 food you use has carbohydrate but no GI" in html
    assert 'href="/food/cache/db-check#missing-gi"' in html
    import html as _html
    import re
    url = _html.unescape(re.search(r'href="(/analysis/whatif\?[^"]*e_with=U%d[^"]*)"' % BARLEY, html).group(1))
    page = client.get(url).text
    assert "Glycemic load" in page and "Barley, pearled, cooked" in page
    assert "Moderate" in page or "Low" in page
    recent = _html.unescape(re.search(r'href="(/analysis/whatif\?[^"]*mode=range[^"]*)"', html).group(1))
    assert client.get(recent).status_code == 200


def test_recipe_page_ranks_foods_inside_sub_recipes(foods, db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    sub = _db.recipe_create(db_conn, name="Rice base", description="", servings=1, instructions="",
                            total_weight=300.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, sub, WHITE, "Rice, white, cooked", 300.0, "g")
    top = _db.recipe_create(db_conn, name="Rice bowl", description="", servings=2, instructions="",
                            total_weight=400.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, top, 0, "Rice base", 1.0, "serving", ref_recipe_id=sub)
    _db.recipe_add_ingredient(db_conn, top, POTATO, "Potato, baked", 100.0, "g")
    db_conn.commit()
    html = TestClient(backend.app).get(f"/recipe/{top}?rank=gl").text
    section = html[html.index('id="sec-contributors"'):]
    assert section.index("Potato, baked") > section.index("Rice, white, cooked")   # rice ranked first
    assert "Lower-glycemic swaps to try" in section
    assert f"recipe_ids={top}" in section


def test_foods_9_lists_used_foods_with_no_gi_and_saves_not_needed(foods, db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    from numa_app.services import data_quality as _dq
    client = TestClient(backend.app)
    _food(db_conn, 977, "Lettuce", 3.0)          # too little carbohydrate to list
    _db.pantry_add(db_conn, "Lettuce", 977)
    _db.pantry_add(db_conn, "Bread, rye", BREAD)
    _db.pantry_add(db_conn, "Rice, white, cooked", WHITE)   # has a GI
    db_conn.commit()
    rows = _dq.missing_gi_in_use(db_conn)
    assert [r["fdc_id"] for r in rows] == [BREAD]

    html = client.get("/food/cache/db-check").text
    sec = html[html.index('id="missing-gi"'):]
    assert "Bread, rye" in sec and f"/food/annotate/{BREAD}?next=" in sec

    r = client.post("/food/cache/db-check/completeness",
                    data={"shown": f"{BREAD}:gi", "ignore": f"{BREAD}:gi", "back": "missing-gi"},
                    follow_redirects=False)
    assert r.headers["location"].endswith("#missing-gi")
    assert _db.get_food_annotation(db_conn, BREAD)["gi_no_prompt"] == 1
    assert _dq.missing_gi_in_use(db_conn)[0]["ignored"] is True
    client.post("/food/cache/db-check/completeness", data={"shown": f"{BREAD}:gi", "back": "missing-gi"})
    assert _db.get_food_annotation(db_conn, BREAD)["gi_no_prompt"] == 0


IMPAIRED_SRC = ("Atkinson 2021 international GI tables, Supplemental Table 1 (ISO 26642:2010 method): "
                "“Barley” · Impaired glucose tolerance (Type 2, n=9)")


def test_values_measured_in_impaired_tolerance_are_marked_everywhere(foods, db_conn):
    """Item 11: a GI measured in people with impaired glucose tolerance or
    diabetes is marked on the food page, the Annotate page, GL Top
    Contributors, swap suggestions and the meal's GL figure."""
    from fastapi.testclient import TestClient
    from web import backend
    for fid, gi in ((BARLEY, 28.0), (WHITE, 73.0)):
        _db.set_food_annotation(db_conn, fid, gi_estimate=gi, gi_no_prompt=False, diaas_estimate=None,
                                diaas_no_prompt=False, prep_context=None,
                                gi_source=IMPAIRED_SRC if fid == BARLEY else "Atkinson 2021: “Rice”"
                                " · Normal glucose tolerance")
    db_conn.commit()
    client = TestClient(backend.app)
    note = "measured in people with impaired glucose tolerance or diabetes"
    food_page = client.get(f"/food/{BARLEY}").text
    assert note in food_page and "/manual#gi-impaired" in food_page
    assert note not in client.get(f"/food/{WHITE}").text
    annotate = client.get(f"/food/annotate/{BARLEY}").text
    assert annotate.count("/manual#gi-impaired") == 2       # lookup label + saved-value note
    assert 'id="gi-pop-note"' in annotate and 'id="gi-pop-note" style="font-size:0.85rem;display:none' not in annotate

    meal_id = int(client.post("/meals/create", data={"name": "Dinner", "meal_date": "2026-07-14"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    client.post(f"/meal/{meal_id}/add", data={"fdc_id": WHITE, "food_name": "Rice, white, cooked",
                                              "portion_str": "200 g"}, follow_redirects=False)
    html = client.get(f"/meal/{meal_id}?rank=gl").text
    swaps = html[html.index('id="gl-swaps"'):]
    assert "&dagger;</sup>" in swaps[:swaps.index("</ul>")]        # barley's swap is marked
    assert "&dagger; GI measured in people with impaired glucose tolerance" in swaps
    assert "/manual#gi-impaired" in swaps

    client.post(f"/meal/{meal_id}/add", data={"fdc_id": BARLEY, "food_name": "Barley, pearled, cooked",
                                              "portion_str": "100 g"}, follow_redirects=False)
    html = client.get(f"/meal/{meal_id}").text
    assert "GI measured in people with impaired glucose tolerance or diabetes for: Barley, pearled, cooked" in html
    assert html.count("/manual#gi-impaired") >= 1


def test_compare_shows_gi_and_gl_per_100g_lowest_highlighted(foods, db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    rid = _db.recipe_create(db_conn, name="Rice and bread", description="", servings=1, instructions="",
                            total_weight=200.0, total_weight_unit="g")
    _db.recipe_add_ingredient(db_conn, rid, WHITE, "Rice, white, cooked", 100.0, "g")
    _db.recipe_add_ingredient(db_conn, rid, BREAD, "Bread, rye", 100.0, "g")
    db_conn.commit()
    html = TestClient(backend.app).get(f"/compare?items=f{WHITE},f{BARLEY},r{rid}").text
    import re
    sec = html[html.index('id="cmp-gl"'):html.index('id="cmp-nutrients"')]
    cells = [re.sub(r"<[^>]+>|\s+", " ", c).strip() for c in re.findall(r'<td class="compare-val-col[^"]*">(.*?)</td>', sec, re.S)]
    assert cells[:3] == ["73", "28", "&mdash;"]
    # GL per 100 g: rice 73 x 28 / 100 = 20.4; barley 7.8 (lowest, highlighted);
    # the recipe is half rice (10.2) and half bread with no GI, so "at least".
    assert cells[3:5] == ["20.4", "7.8"]
    assert cells[5].startswith("&ge;&thinsp;10.2") and "covers 37% of carbs" in cells[5]
    assert sec.count("compare-max") == 1
    assert re.search(r'compare-max">\s*7\.8', sec)


def test_recent_days_has_a_day_gl_column(foods, db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    client = TestClient(backend.app)
    meal_id = int(client.post("/meals/create", data={"name": "Lunch", "meal_date": "2026-07-15"},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    client.post(f"/meal/{meal_id}/add", data={"fdc_id": WHITE, "food_name": "Rice, white, cooked",
                                              "portion_str": "200 g"}, follow_redirects=False)
    html = client.get("/summary").text
    assert ">Day GL</th>" in html
    import re
    row = html[html.index(">2026-07-15<"):]
    assert re.search(r">\s*41\s*</span><br>", row)          # 73 x 56 / 100 = 40.9, shown whole
    client.post(f"/meal/{meal_id}/add", data={"fdc_id": BREAD, "food_name": "Bread, rye",
                                              "portion_str": "100 g"}, follow_redirects=False)
    html = client.get("/summary").text
    assert "&ge;&thinsp;41" in html and "% covered" in html
    assert client.get("/summary/nutrient-plot?nutrients=gl&submitted=1").status_code == 200



def test_daily_gl_target_shows_on_day_pages_recent_days_and_trend(foods, db_conn):
    """Step 5: a profile's daily GL target, saved in Settings, colours Day GL
    in Recent Days, adds a target line on the day page, counts days over on
    the trend page — and saving Settings keeps the active profile's name."""
    import profile as _profile
    from fastapi.testclient import TestClient
    from web import backend
    client = TestClient(backend.app)
    active = _profile.load_profile()
    form = {"age": active.age, "sex": active.sex, "weight": active.weight_kg, "weight_unit": "kg",
            "height_cm": active.height_cm, "height_unit": "cm", "activity_level": active.activity_level,
            "gl_day_target": "30"}
    client.post("/settings", data=form, follow_redirects=False)
    saved = _profile.load_profile()
    assert saved.gl_day_target == 30.0 and saved.name == active.name

    import datetime
    today = datetime.date.today().isoformat()
    meal_id = int(client.post("/meals/create", data={"name": "Lunch", "meal_date": today},
                              follow_redirects=False).headers["location"].rsplit("/", 1)[-1])
    client.post(f"/meal/{meal_id}/add", data={"fdc_id": WHITE, "food_name": "Rice, white, cooked",
                                              "portion_str": "200 g"}, follow_redirects=False)
    day = client.get(f"/summary/{today}").text
    assert "Your daily target: 30" in day and "over it" in day
    recent = client.get("/summary").text
    assert 'class="rda-over" title="136% of your daily target of 30"' in recent
    trend = client.get("/summary/trend?days=7").text
    assert "1 of 1 day(s)</span> over your daily glycemic load target" in trend

    # Blank turns it off.
    client.post("/settings", data={**form, "gl_day_target": ""}, follow_redirects=False)
    assert _profile.load_profile().gl_day_target is None


@pytest.mark.parametrize("tolerance, expected", [
    ("impaired", "Your profile says you have impaired glucose tolerance or diabetes, so this fits you"),
    ("normal", "Your profile says normal glucose tolerance, so treat it as an approximation"),
    ("", "Set your glucose tolerance</a> to tailor this note"),
])
def test_impaired_value_note_is_tailored_to_profile(foods, db_conn, tolerance, expected):
    import profile as _profile
    from fastapi.testclient import TestClient
    from web import backend
    _db.set_food_annotation(db_conn, BARLEY, gi_estimate=28.0, gi_no_prompt=False, diaas_estimate=None,
                            diaas_no_prompt=False, prep_context=None, gi_source=IMPAIRED_SRC)
    db_conn.commit()
    p = _profile.load_profile()
    p.glucose_tolerance = tolerance
    _profile.save_profile(p)
    client = TestClient(backend.app)
    assert expected in client.get(f"/food/{BARLEY}").text.replace("&#39;", "'")
    assert expected in client.get(f"/food/annotate/{BARLEY}").text.replace("&#39;", "'")


def test_settings_offers_gl_target_choices_linked_to_manual(foods, db_conn):
    from fastapi.testclient import TestClient
    from web import backend
    html = TestClient(backend.app).get("/settings").text
    assert "Help me choose a target" in html and "/manual#gl-target-choose" in html
    assert 'data-value="80"' in html                                   # the convention
    assert re.search(r'js-gl-target-pick" data-value="\d+">Use \d+</button><br>\s*80 per 2,000 kcal', html)
    assert "Needs at least 7 days" in html                              # no history in the test DB
