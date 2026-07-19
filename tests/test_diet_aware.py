"""
Tests for numa_app/services/diet_aware.py — diet-preference-aware analysis
notes shown alongside the RDA comparison for vegetarian/plant-based diets.
"""
import pytest

from numa_app.services.diet_aware import b12_deficiency_note, iron_zinc_bioavailability_note


class TestB12DeficiencyNote:
    def test_none_when_diet_pref_all(self):
        assert b12_deficiency_note("all", 0.0) is None

    def test_none_for_vegetarian_even_when_low(self):
        # Vegetarians still have dairy/eggs as a B12 source — not flagged.
        assert b12_deficiency_note("vegetarian", 0.0) is None

    def test_none_when_plant_only_but_adequate_intake(self):
        assert b12_deficiency_note("plant_only", 50.0) is None
        assert b12_deficiency_note("plant_only", 100.0) is None

    def test_warns_when_plant_only_and_low_intake(self):
        note = b12_deficiency_note("plant_only", 0.0)
        assert note is not None
        assert "B12" in note

    def test_boundary_at_50_percent(self):
        assert b12_deficiency_note("plant_only", 49.9) is not None
        assert b12_deficiency_note("plant_only", 50.0) is None


class TestIronZincBioavailabilityNote:
    def test_none_when_diet_pref_all(self):
        assert iron_zinc_bioavailability_note("all") is None

    def test_note_for_vegetarian(self):
        note = iron_zinc_bioavailability_note("vegetarian")
        assert note is not None
        assert "iron" in note.lower() and "zinc" in note.lower()

    def test_note_for_plant_only(self):
        assert iron_zinc_bioavailability_note("plant_only") is not None
