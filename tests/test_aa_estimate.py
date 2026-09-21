"""
Tests for numa_app/services/aa_estimate.py — estimating a food's amino acid
profile by scaling another food's AA values to match its own protein content.
"""
from datetime import date

import pytest

from numa_app.services.aa_estimate import copy_nutrients_note, estimate_aa, source_note

_SOURCE = {
    "protein_g": 20.0,
    "aa_tryptophan_g": 0.2,
    "aa_threonine_g": 0.6,
    "aa_isoleucine_g": 0.6,
    "aa_leucine_g": 1.0,
    "aa_lysine_g": 0.8,
    "aa_methionine_g": 0.4,
    "aa_phenylalanine_g": 0.6,
    "aa_valine_g": 0.7,
    "aa_histidine_g": 0.3,
}


class TestEstimateAA:
    def test_scales_by_protein_ratio(self):
        target = {"protein_g": 10.0, "calories": 100.0}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert err is None
        assert factor == pytest.approx(0.5)
        assert updated["aa_leucine_g"] == pytest.approx(0.5)
        assert updated["aa_tryptophan_g"] == pytest.approx(0.1)
        # Non-AA fields are preserved untouched.
        assert updated["calories"] == 100.0
        assert updated["protein_g"] == 10.0

    def test_scales_up_when_target_has_more_protein(self):
        target = {"protein_g": 40.0}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert err is None
        assert factor == pytest.approx(2.0)
        assert updated["aa_leucine_g"] == pytest.approx(2.0)

    def test_error_when_source_lacks_aa_data(self):
        target = {"protein_g": 10.0}
        source = {"protein_g": 20.0, "aa_leucine_g": 1.0}  # only 1 essential AA present
        updated, factor, err = estimate_aa(target, source)
        assert updated is None
        assert factor is None
        # Exact text, not just a substring — a mutation-testing pass found the
        # existing substring check ("amino acid data" in err) doesn't catch a
        # mangled prefix/case/wrapping, since that phrase survives untouched.
        assert err == "Source food has no amino acid data to copy."

    def test_error_when_target_has_no_protein(self):
        target = {"protein_g": 0.0}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert updated is None
        assert err == "Target food has no protein_g value to scale against."

    def test_error_when_source_has_no_protein(self):
        target = {"protein_g": 10.0}
        source = dict(_SOURCE)
        source["protein_g"] = 0.0
        updated, factor, err = estimate_aa(target, source)
        assert updated is None
        assert err == "Source food has no protein_g value to scale from."

    def test_only_overwrites_keys_present_in_source(self):
        target = {"protein_g": 10.0, "aa_cystine_g": 0.05}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert err is None
        # _SOURCE has no aa_cystine_g — target's existing value must survive untouched.
        assert updated["aa_cystine_g"] == 0.05

    def test_scaled_values_are_rounded_to_4_decimal_places(self):
        # A mutation-testing pass found round(..., 4) -> round(..., 5) survived,
        # since pytest.approx's default tolerance is looser than a 5th-decimal
        # difference. Pick a factor/value pair whose 4- and 5-place roundings
        # actually differ, and assert the exact float.
        target = {"protein_g": 3.0}
        source = dict(_SOURCE)
        source["protein_g"] = 7.0
        source["aa_leucine_g"] = 1.0 / 3
        updated, factor, err = estimate_aa(target, source)
        assert err is None
        raw = (1.0 / 3) * (3.0 / 7.0)
        assert round(raw, 4) != round(raw, 5)
        assert updated["aa_leucine_g"] == round(raw, 4)

    def test_target_protein_of_exactly_one_gram_still_succeeds(self):
        # Boundary check: "<= 0" must not have drifted to "<= 1" — 1.0g of
        # protein is a real, non-degenerate value, not "missing" data.
        target = {"protein_g": 1.0}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert err is None
        assert factor == pytest.approx(1.0 / 20.0)

    def test_source_protein_of_exactly_one_gram_still_succeeds(self):
        target = {"protein_g": 10.0}
        source = dict(_SOURCE)
        source["protein_g"] = 1.0
        updated, factor, err = estimate_aa(target, source)
        assert err is None
        assert factor == pytest.approx(10.0)


class TestSourceNote:
    def test_includes_name_id_and_factor(self):
        note = source_note("Chicken breast", 171477, 0.5)
        assert "Chicken breast" in note
        assert "#171477" in note
        assert "0.50x" in note

    def test_omits_id_parens_when_no_fdc_id(self):
        # Exact match on the pre-comma segment, not just "(#" not in note —
        # a mutation-testing pass found the id_part fallback ("" -> "XXXX")
        # survived that weaker check, since "XXXX" also contains no "(#".
        note = source_note("My custom food", None, 1.25)
        assert note.startswith("AA data estimated by scaling from My custom food, ")
        assert "1.25x" in note


class TestCopyNutrientsNote:
    # Zero coverage (a mutation-testing pass found "no tests" on every
    # branch) despite being a real, user-visible note saved on every
    # nutrient copy — see web/backend.py's copy-nutrients routes.

    def test_no_field_labels_describes_a_full_profile_copy(self):
        note = copy_nutrients_note("Chicken breast", 171477)
        assert note == f"Nutrient profile copied from Chicken breast (#171477), {date.today().isoformat()}"

    def test_omits_id_parens_when_no_fdc_id(self):
        note = copy_nutrients_note("My custom food", None)
        assert note.startswith("Nutrient profile copied from My custom food, ")

    def test_spells_out_up_to_6_field_labels(self):
        note = copy_nutrients_note("Chicken breast", 171477, ["Iron", "Zinc", "Calcium"])
        assert note == (
            f"Copied from Chicken breast (#171477): Iron, Zinc, Calcium, {date.today().isoformat()}"
        )

    def test_exactly_6_field_labels_are_still_spelled_out(self):
        # Boundary check: "<= 6" must not have drifted to "< 6".
        labels = [f"Field{i}" for i in range(6)]
        note = copy_nutrients_note("Chicken breast", 171477, labels)
        assert ", ".join(labels) in note
        assert "fields" not in note

    def test_more_than_6_field_labels_falls_back_to_a_count(self):
        labels = [f"Field{i}" for i in range(7)]
        note = copy_nutrients_note("Chicken breast", 171477, labels)
        assert note == f"Copied from Chicken breast (#171477): 7 fields, {date.today().isoformat()}"
