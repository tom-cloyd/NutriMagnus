"""
Tests for numa_app/services/rda_status.py — percent-of-target status
classification used by the web backend (web/backend.py). Originally extracted
to unify web's and the (since-removed) CLI's diverging thresholds — web used
75% instead of the CLI's 70% for the minimum/target "near" cutoff, and had no
intermediate tier at all for limit-type nutrients between 80-100%, so the
same nutrient data could show a different colored verdict depending on which
UI displayed it.
"""
import pytest

from numa_app.services.rda_status import rda_status, limit_warning


class TestMinimumTargetThresholds:
    @pytest.mark.parametrize("pct,expected", [
        (0, "low"), (69, "low"), (70, "near"), (75, "near"),
        (99, "near"), (100, "met"), (150, "met"),
    ])
    def test_thresholds(self, pct, expected):
        assert rda_status(pct, "min") == expected


class TestTargetThresholds:
    """target is two-sided (calories, or a user-configured Revised Optimal
    value) — unlike "min", drifting too far over 100% should stop reading as
    "met" and eventually flag as "over", the same shape as the limit type."""
    @pytest.mark.parametrize("pct,expected", [
        (0, "low"), (69, "low"), (70, "near"), (99, "near"),
        (100, "met"), (130, "met"), (131, "near"), (150, "near"),
        (151, "over"), (200, "over"),
    ])
    def test_thresholds(self, pct, expected):
        assert rda_status(pct, "target") == expected


class TestLimitThresholds:
    @pytest.mark.parametrize("pct,expected", [
        (0, "met"), (80, "met"), (81, "near"), (99, "near"),
        (100, "near"), (101, "over"), (200, "over"),
    ])
    def test_thresholds(self, pct, expected):
        assert rda_status(pct, "limit") == expected


class TestLimitWarning:
    @pytest.mark.parametrize("day_total,limit,expected", [
        (0, 2000, False), (1799, 2000, False), (1800, 2000, True),
        (2000, 2000, True), (2500, 2000, True),
    ])
    def test_thresholds(self, day_total, limit, expected):
        assert limit_warning(day_total, limit) is expected

    def test_no_limit_configured_never_warns(self):
        assert limit_warning(10_000, 0) is False
