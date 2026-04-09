"""
Tests for profile.py — user profile load/save and personalized RDA computation.
"""

import json
import pathlib

import pytest

import profile as _profile
from profile import (
    UserProfile, compute_rda, load_profile, save_profile, bmr,
    parse_weight, parse_height, format_weight, format_height,
    lb_to_kg, kg_to_lb, ftin_to_cm, cm_to_ftin,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def male_35(tmp_path, monkeypatch):
    monkeypatch.setattr(_profile, "_PROFILE_FILE", tmp_path / "profile.json")
    return UserProfile(age=35, sex="male", weight_kg=80.0, height_cm=178.0,
                       activity_level="moderate")


@pytest.fixture()
def female_55(tmp_path, monkeypatch):
    monkeypatch.setattr(_profile, "_PROFILE_FILE", tmp_path / "profile.json")
    return UserProfile(age=55, sex="female", weight_kg=65.0, height_cm=163.0,
                       activity_level="light")


@pytest.fixture()
def other_25(tmp_path, monkeypatch):
    monkeypatch.setattr(_profile, "_PROFILE_FILE", tmp_path / "profile.json")
    return UserProfile(age=25, sex="other", weight_kg=70.0, height_cm=170.0,
                       activity_level="active")


# ---------------------------------------------------------------------------
# load_profile / save_profile
# ---------------------------------------------------------------------------

class TestLoadSave:
    def test_load_returns_none_when_no_file(self, tmp_path, monkeypatch):
        monkeypatch.setattr(_profile, "_PROFILE_FILE", tmp_path / "profile.json")
        assert load_profile() is None

    def test_roundtrip(self, male_35, tmp_path, monkeypatch):
        monkeypatch.setattr(_profile, "_PROFILE_FILE", tmp_path / "profile.json")
        save_profile(male_35)
        loaded = load_profile()
        assert loaded is not None
        assert loaded.age == 35
        assert loaded.sex == "male"
        assert loaded.weight_kg == pytest.approx(80.0)
        assert loaded.height_cm == pytest.approx(178.0)
        assert loaded.activity_level == "moderate"

    def test_save_creates_parent_dirs(self, tmp_path, monkeypatch):
        deep = tmp_path / "a" / "b" / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", deep)
        p = UserProfile(age=30, sex="male", weight_kg=75.0, height_cm=175.0,
                        activity_level="sedentary")
        save_profile(p)
        assert deep.exists()

    def test_load_returns_none_on_corrupt_file(self, tmp_path, monkeypatch):
        f = tmp_path / "profile.json"
        f.write_text("not valid json")
        monkeypatch.setattr(_profile, "_PROFILE_FILE", f)
        assert load_profile() is None

    def test_load_returns_none_on_missing_keys(self, tmp_path, monkeypatch):
        f = tmp_path / "profile.json"
        f.write_text(json.dumps({"age": 30}))
        monkeypatch.setattr(_profile, "_PROFILE_FILE", f)
        assert load_profile() is None

    def test_save_writes_valid_json(self, male_35, tmp_path, monkeypatch):
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        save_profile(male_35)
        data = json.loads(pf.read_text())
        assert data["age"] == 35
        assert data["sex"] == "male"


# ---------------------------------------------------------------------------
# BMR
# ---------------------------------------------------------------------------

class TestBMR:
    def test_male_bmr(self):
        p = UserProfile(age=35, sex="male", weight_kg=80.0,
                        height_cm=178.0, activity_level="sedentary")
        # 10*80 + 6.25*178 - 5*35 + 5 = 800 + 1112.5 - 175 + 5 = 1742.5
        assert bmr(p) == pytest.approx(1742.5)

    def test_female_bmr(self):
        p = UserProfile(age=35, sex="female", weight_kg=65.0,
                        height_cm=163.0, activity_level="sedentary")
        # 10*65 + 6.25*163 - 5*35 - 161 = 650 + 1018.75 - 175 - 161 = 1332.75
        assert bmr(p) == pytest.approx(1332.75)

    def test_other_bmr_is_midpoint(self):
        p_m = UserProfile(age=35, sex="male",   weight_kg=70.0,
                          height_cm=170.0, activity_level="sedentary")
        p_f = UserProfile(age=35, sex="female", weight_kg=70.0,
                          height_cm=170.0, activity_level="sedentary")
        p_o = UserProfile(age=35, sex="other",  weight_kg=70.0,
                          height_cm=170.0, activity_level="sedentary")
        assert bmr(p_o) == pytest.approx((bmr(p_m) + bmr(p_f)) / 2)


# ---------------------------------------------------------------------------
# compute_rda — structure
# ---------------------------------------------------------------------------

class TestComputeRdaStructure:
    def test_returns_dict(self, male_35):
        rda = compute_rda(male_35)
        assert isinstance(rda, dict)

    def test_calories_present(self, male_35):
        rda = compute_rda(male_35)
        assert "calories" in rda

    def test_value_unit_type_tuple(self, male_35):
        rda = compute_rda(male_35)
        for key, entry in rda.items():
            assert len(entry) == 3, f"{key}: expected 3-tuple"
            val, unit, rda_type = entry
            assert isinstance(val, float)
            assert isinstance(unit, str)
            assert rda_type in ("target", "minimum", "limit"), f"{key}: bad type '{rda_type}'"

    def test_sodium_is_limit(self, male_35):
        rda = compute_rda(male_35)
        assert rda["sodium_mg"][2] == "limit"

    def test_protein_is_minimum(self, male_35):
        rda = compute_rda(male_35)
        assert rda["protein_g"][2] == "minimum"

    def test_calories_is_target(self, male_35):
        rda = compute_rda(male_35)
        assert rda["calories"][2] == "target"

    def test_all_values_positive(self, male_35):
        rda = compute_rda(male_35)
        for key, (val, _, _) in rda.items():
            assert val > 0, f"{key} should be > 0"

    def test_essential_nutrients_present(self, male_35):
        rda = compute_rda(male_35)
        for key in ("protein_g", "fiber_g", "calcium_mg", "iron_mg",
                    "vitamin_c_mg", "vitamin_d_mcg", "b12_mcg"):
            assert key in rda, f"Missing {key}"


# ---------------------------------------------------------------------------
# compute_rda — calorie calculation
# ---------------------------------------------------------------------------

class TestCalories:
    def test_calories_increase_with_activity(self):
        base = dict(age=30, sex="male", weight_kg=75.0, height_cm=175.0)
        cal_sed  = compute_rda(UserProfile(**base, activity_level="sedentary"))["calories"][0]
        cal_mod  = compute_rda(UserProfile(**base, activity_level="moderate"))["calories"][0]
        cal_very = compute_rda(UserProfile(**base, activity_level="very_active"))["calories"][0]
        assert cal_sed < cal_mod < cal_very

    def test_calories_reasonable_range(self, male_35):
        cal = compute_rda(male_35)["calories"][0]
        assert 1200 <= cal <= 4500


# ---------------------------------------------------------------------------
# compute_rda — protein
# ---------------------------------------------------------------------------

class TestProtein:
    def test_protein_scales_with_weight(self):
        light = UserProfile(age=30, sex="male", weight_kg=60.0,
                            height_cm=170.0, activity_level="sedentary")
        heavy = UserProfile(age=30, sex="male", weight_kg=100.0,
                            height_cm=170.0, activity_level="sedentary")
        prot_light = compute_rda(light)["protein_g"][0]
        prot_heavy = compute_rda(heavy)["protein_g"][0]
        assert prot_heavy > prot_light

    def test_active_has_higher_protein_per_kg(self):
        sed = UserProfile(age=30, sex="male", weight_kg=80.0,
                          height_cm=175.0, activity_level="sedentary")
        act = UserProfile(age=30, sex="male", weight_kg=80.0,
                          height_cm=175.0, activity_level="active")
        assert compute_rda(act)["protein_g"][0] > compute_rda(sed)["protein_g"][0]

    def test_protein_unit_is_g(self, male_35):
        assert compute_rda(male_35)["protein_g"][1] == "g"


# ---------------------------------------------------------------------------
# compute_rda — sex-specific values
# ---------------------------------------------------------------------------

class TestSexSpecific:
    def test_iron_higher_for_premenopausal_female(self):
        m = UserProfile(age=30, sex="male",   weight_kg=75, height_cm=175, activity_level="sedentary")
        f = UserProfile(age=30, sex="female", weight_kg=60, height_cm=163, activity_level="sedentary")
        assert compute_rda(f)["iron_mg"][0] > compute_rda(m)["iron_mg"][0]

    def test_iron_same_after_menopause(self):
        f_young = UserProfile(age=30, sex="female", weight_kg=60, height_cm=163, activity_level="sedentary")
        f_old   = UserProfile(age=55, sex="female", weight_kg=60, height_cm=163, activity_level="sedentary")
        m       = UserProfile(age=30, sex="male",   weight_kg=75, height_cm=175, activity_level="sedentary")
        assert compute_rda(f_old)["iron_mg"][0] == pytest.approx(compute_rda(m)["iron_mg"][0])
        assert compute_rda(f_young)["iron_mg"][0] > compute_rda(f_old)["iron_mg"][0]

    def test_potassium_higher_for_male(self):
        m = UserProfile(age=30, sex="male",   weight_kg=75, height_cm=175, activity_level="sedentary")
        f = UserProfile(age=30, sex="female", weight_kg=60, height_cm=163, activity_level="sedentary")
        assert compute_rda(m)["potassium_mg"][0] > compute_rda(f)["potassium_mg"][0]

    def test_other_sex_iron_between_male_and_female(self):
        m = UserProfile(age=30, sex="male",   weight_kg=70, height_cm=170, activity_level="sedentary")
        f = UserProfile(age=30, sex="female", weight_kg=70, height_cm=170, activity_level="sedentary")
        o = UserProfile(age=30, sex="other",  weight_kg=70, height_cm=170, activity_level="sedentary")
        iron_m = compute_rda(m)["iron_mg"][0]
        iron_f = compute_rda(f)["iron_mg"][0]
        iron_o = compute_rda(o)["iron_mg"][0]
        assert iron_m <= iron_o <= iron_f


# ---------------------------------------------------------------------------
# compute_rda — age-specific values
# ---------------------------------------------------------------------------

class TestAgeSpecific:
    def test_vitamin_d_higher_at_70_plus(self):
        young = UserProfile(age=40, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        old   = UserProfile(age=75, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        assert compute_rda(old)["vitamin_d_mcg"][0] > compute_rda(young)["vitamin_d_mcg"][0]

    def test_calcium_higher_for_women_over_50(self):
        young = UserProfile(age=40, sex="female", weight_kg=60, height_cm=163, activity_level="sedentary")
        old   = UserProfile(age=60, sex="female", weight_kg=60, height_cm=163, activity_level="sedentary")
        assert compute_rda(old)["calcium_mg"][0] > compute_rda(young)["calcium_mg"][0]

    def test_calcium_same_for_young_men(self):
        m30 = UserProfile(age=30, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        m60 = UserProfile(age=60, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        # Men only get higher calcium at 70+
        assert compute_rda(m30)["calcium_mg"][0] == pytest.approx(compute_rda(m60)["calcium_mg"][0])

    def test_fiber_decreases_after_50(self):
        young = UserProfile(age=35, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        old   = UserProfile(age=55, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        assert compute_rda(old)["fiber_g"][0] < compute_rda(young)["fiber_g"][0]

    def test_b6_higher_after_50_male(self):
        young = UserProfile(age=35, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        old   = UserProfile(age=60, sex="male", weight_kg=75, height_cm=175, activity_level="sedentary")
        assert compute_rda(old)["b6_mg"][0] > compute_rda(young)["b6_mg"][0]


# ---------------------------------------------------------------------------
# compute_rda — sodium limit
# ---------------------------------------------------------------------------

class TestSodiumLimit:
    def test_sodium_limit_2300(self, male_35):
        rda = compute_rda(male_35)
        assert rda["sodium_mg"][0] == pytest.approx(2300.0)
        assert rda["sodium_mg"][1] == "mg"
        assert rda["sodium_mg"][2] == "limit"


# ---------------------------------------------------------------------------
# Unit conversion helpers
# ---------------------------------------------------------------------------

class TestUnitConversions:
    def test_lb_to_kg(self):
        assert lb_to_kg(220.462) == pytest.approx(100.0, rel=1e-4)

    def test_kg_to_lb(self):
        assert kg_to_lb(100.0) == pytest.approx(220.462, rel=1e-4)

    def test_ftin_to_cm_5ft10in(self):
        assert ftin_to_cm(5, 10) == pytest.approx(177.8, rel=1e-3)

    def test_ftin_to_cm_6ft_exactly(self):
        assert ftin_to_cm(6, 0) == pytest.approx(182.88, rel=1e-3)

    def test_cm_to_ftin_roundtrip(self):
        feet, inches = cm_to_ftin(177.8)
        assert feet == 5
        assert inches == pytest.approx(10.0, abs=0.1)

    def test_ftin_cm_roundtrip(self):
        original_cm = 175.0
        feet, inches = cm_to_ftin(original_cm)
        assert ftin_to_cm(feet, inches) == pytest.approx(original_cm, abs=0.1)


# ---------------------------------------------------------------------------
# parse_weight
# ---------------------------------------------------------------------------

class TestParseWeight:
    def test_plain_number_is_kg(self):
        kg, unit = parse_weight("80")
        assert kg == pytest.approx(80.0)
        assert unit == "kg"

    def test_explicit_kg(self):
        kg, unit = parse_weight("72.5 kg")
        assert kg == pytest.approx(72.5)
        assert unit == "kg"

    def test_lbs_converts_to_kg(self):
        kg, unit = parse_weight("176 lbs")
        assert kg == pytest.approx(lb_to_kg(176), rel=1e-4)
        assert unit == "lb"

    def test_lb_singular(self):
        kg, unit = parse_weight("155 lb")
        assert unit == "lb"
        assert kg == pytest.approx(lb_to_kg(155), rel=1e-4)

    def test_pounds_word(self):
        kg, unit = parse_weight("140 pounds")
        assert unit == "lb"

    def test_decimal_lbs(self):
        kg, unit = parse_weight("165.5 lbs")
        assert unit == "lb"
        assert kg == pytest.approx(lb_to_kg(165.5), rel=1e-4)

    def test_empty_returns_none(self):
        kg, unit = parse_weight("")
        assert kg is None

    def test_garbage_returns_none(self):
        kg, unit = parse_weight("heavy")
        assert kg is None

    def test_case_insensitive(self):
        kg, unit = parse_weight("150 LBS")
        assert unit == "lb"


# ---------------------------------------------------------------------------
# parse_height
# ---------------------------------------------------------------------------

class TestParseHeight:
    def test_plain_cm(self):
        cm, unit = parse_height("178")
        assert cm == pytest.approx(178.0)
        assert unit == "cm"

    def test_explicit_cm_label(self):
        cm, unit = parse_height("178 cm")
        assert cm == pytest.approx(178.0)
        assert unit == "cm"

    def test_decimal_cm(self):
        cm, unit = parse_height("172.5")
        assert cm == pytest.approx(172.5)
        assert unit == "cm"

    def test_feet_inches_quote_format(self):
        cm, unit = parse_height("5'10\"")
        assert cm == pytest.approx(ftin_to_cm(5, 10), rel=1e-3)
        assert unit == "imperial"

    def test_feet_inches_no_closing_quote(self):
        cm, unit = parse_height("5'10")
        assert unit == "imperial"
        assert cm == pytest.approx(ftin_to_cm(5, 10), rel=1e-3)

    def test_feet_inches_word_units(self):
        cm, unit = parse_height("5ft 10in")
        assert unit == "imperial"
        assert cm == pytest.approx(ftin_to_cm(5, 10), rel=1e-3)

    def test_feet_inches_compact_word(self):
        cm, unit = parse_height("5ft10in")
        assert unit == "imperial"
        assert cm == pytest.approx(ftin_to_cm(5, 10), rel=1e-3)

    def test_six_feet_exactly(self):
        cm, unit = parse_height("6'0\"")
        assert unit == "imperial"
        assert cm == pytest.approx(ftin_to_cm(6, 0), rel=1e-3)

    def test_feet_only_with_quote(self):
        cm, unit = parse_height("6'")
        assert unit == "imperial"
        assert cm == pytest.approx(ftin_to_cm(6, 0), rel=1e-3)

    def test_feet_only_ft_word(self):
        cm, unit = parse_height("6ft")
        assert unit == "imperial"
        assert cm == pytest.approx(ftin_to_cm(6, 0), rel=1e-3)

    def test_empty_returns_none(self):
        cm, unit = parse_height("")
        assert cm is None

    def test_garbage_returns_none(self):
        cm, unit = parse_height("tall")
        assert cm is None

    def test_out_of_range_cm_returns_valid_value(self):
        # 2103 cm is out of the accepted range, but parse_height itself just
        # parses the number; range validation is done in the caller.
        cm, unit = parse_height("2103")
        assert cm == pytest.approx(2103.0)
        assert unit == "cm"


# ---------------------------------------------------------------------------
# format_weight / format_height
# ---------------------------------------------------------------------------

class TestFormatters:
    def test_format_weight_kg(self):
        assert format_weight(80.0, "kg") == "80.0 kg"

    def test_format_weight_lb_shows_both(self):
        result = format_weight(80.0, "lb")
        assert "lb" in result
        assert "kg" in result
        assert "176" in result   # 80 kg ≈ 176 lb

    def test_format_height_cm(self):
        assert format_height(178.0, "cm") == "178.0 cm"

    def test_format_height_imperial_shows_both(self):
        result = format_height(177.8, "imperial")
        assert "'" in result or "ft" in result
        assert "cm" in result
        assert "5" in result   # 177.8 cm ≈ 5'10"


# ---------------------------------------------------------------------------
# UserProfile — unit fields default and roundtrip
# ---------------------------------------------------------------------------

class TestUnitFields:
    def test_default_units_are_metric(self):
        p = UserProfile(age=30, sex="male", weight_kg=75, height_cm=175,
                        activity_level="sedentary")
        assert p.weight_unit == "kg"
        assert p.height_unit == "cm"

    def test_unit_fields_saved_and_loaded(self, tmp_path, monkeypatch):
        pf = tmp_path / "profile.json"
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        p = UserProfile(age=30, sex="male", weight_kg=75, height_cm=175,
                        activity_level="sedentary", weight_unit="lb",
                        height_unit="imperial")
        _profile.save_profile(p)
        loaded = _profile.load_profile()
        assert loaded.weight_unit == "lb"
        assert loaded.height_unit == "imperial"

    def test_old_profile_without_unit_fields_loads_with_defaults(self, tmp_path, monkeypatch):
        """Profiles saved before unit fields existed load cleanly with metric defaults."""
        pf = tmp_path / "profile.json"
        pf.write_text('{"age":35,"sex":"male","weight_kg":80.0,"height_cm":178.0,'
                      '"activity_level":"moderate"}')
        monkeypatch.setattr(_profile, "_PROFILE_FILE", pf)
        loaded = _profile.load_profile()
        assert loaded is not None
        assert loaded.weight_unit == "kg"
        assert loaded.height_unit == "cm"
