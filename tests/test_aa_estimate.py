"""
Tests for numa_app/services/aa_estimate.py — estimating a food's amino acid
profile by scaling another food's AA values to match its own protein content.
"""
import pytest

from numa_app.services.aa_estimate import estimate_aa, source_note

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
        assert "amino acid data" in err

    def test_error_when_target_has_no_protein(self):
        target = {"protein_g": 0.0}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert updated is None
        assert "Target food" in err

    def test_error_when_source_has_no_protein(self):
        target = {"protein_g": 10.0}
        source = dict(_SOURCE)
        source["protein_g"] = 0.0
        updated, factor, err = estimate_aa(target, source)
        assert updated is None
        assert "Source food" in err

    def test_only_overwrites_keys_present_in_source(self):
        target = {"protein_g": 10.0, "aa_cystine_g": 0.05}
        updated, factor, err = estimate_aa(target, _SOURCE)
        assert err is None
        # _SOURCE has no aa_cystine_g — target's existing value must survive untouched.
        assert updated["aa_cystine_g"] == 0.05


class TestSourceNote:
    def test_includes_name_id_and_factor(self):
        note = source_note("Chicken breast", 171477, 0.5)
        assert "Chicken breast" in note
        assert "#171477" in note
        assert "0.50x" in note

    def test_omits_id_parens_when_no_fdc_id(self):
        note = source_note("My custom food", None, 1.25)
        assert "(#" not in note
        assert "1.25x" in note
