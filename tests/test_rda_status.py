"""
Tests for numa_app/services/rda_status.py — shared percent-of-target status
classification used by CLI (render.py) and web (backend.py). web previously
used its own thresholds (75% instead of 70% for the minimum/target "near"
cutoff, and no intermediate tier at all for limit-type nutrients between
80-100%), so the same nutrient data could show a different colored verdict
depending on which UI displayed it.
"""
import pytest

from numa_app.services.rda_status import rda_status


class TestMinimumTargetThresholds:
    @pytest.mark.parametrize("pct,expected", [
        (0, "low"), (69, "low"), (70, "near"), (75, "near"),
        (99, "near"), (100, "met"), (150, "met"),
    ])
    def test_thresholds(self, pct, expected):
        assert rda_status(pct, "min") == expected


class TestLimitThresholds:
    @pytest.mark.parametrize("pct,expected", [
        (0, "met"), (80, "met"), (81, "near"), (99, "near"),
        (100, "near"), (101, "over"), (200, "over"),
    ])
    def test_thresholds(self, pct, expected):
        assert rda_status(pct, "limit") == expected
