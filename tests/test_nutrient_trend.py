"""
Tests for numa_app/services/nutrient_trend.py — multi-day nutrient averaging
used by the N-day nutrient trend view.
"""
from numa_app.services.nutrient_trend import average_from_daily_totals


class TestAverageFromDailyTotals:
    def test_empty_input_returns_empty_and_zero_days(self):
        avg, num_days = average_from_daily_totals({})
        assert avg == {}
        assert num_days == 0

    def test_single_day_returns_that_days_totals_unchanged(self):
        avg, num_days = average_from_daily_totals({
            "2026-07-01": {"calories": 2000.0, "b12_mcg": 1.2},
        })
        assert num_days == 1
        assert avg == {"calories": 2000.0, "b12_mcg": 1.2}

    def test_averages_across_multiple_days(self):
        avg, num_days = average_from_daily_totals({
            "2026-07-01": {"calories": 2000.0, "iron_mg": 10.0},
            "2026-07-02": {"calories": 1800.0, "iron_mg": 6.0},
        })
        assert num_days == 2
        assert avg["calories"] == 1900.0
        assert avg["iron_mg"] == 8.0

    def test_missing_nutrient_on_some_days_averages_over_all_days_not_just_present_ones(self):
        # b12_mcg present on day 1 only — still divided by the full day count (2),
        # not just the 1 day it appears on. A day with no logged B12 for a food
        # is 0 intake that day, and that should pull the average down.
        avg, num_days = average_from_daily_totals({
            "2026-07-01": {"b12_mcg": 4.0},
            "2026-07-02": {"calories": 1800.0},
        })
        assert num_days == 2
        assert avg["b12_mcg"] == 2.0

    def test_unlogged_days_are_excluded_not_treated_as_zero(self):
        # Only 2 days have entries here — a caller who queried a 7-day window
        # but only logged meals on 2 of those days should NOT get an average
        # diluted by the 5 unlogged days.
        avg, num_days = average_from_daily_totals({
            "2026-07-01": {"calories": 2000.0},
            "2026-07-05": {"calories": 2200.0},
        })
        assert num_days == 2
        assert avg["calories"] == 2100.0
