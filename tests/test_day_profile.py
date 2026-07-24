"""
Tests for numa_app/services/day_profile.py — pinning which user profile a
logged day is scored against. Profiles can change over time (illness,
travel, weight change); a past day's DCP/RDA comparisons must stay pinned to
whichever profile was active when that day was first logged, not whatever
profile happens to be active now.
"""
import dataclasses
import json

import pytest

import db as _db
import profile as _profile
from numa_app.services import day_profile as _day_profile


def _save_travel_profile(name="Travel") -> None:
    p = _profile.UserProfile(
        age=35, sex="male", weight_kg=90.0, height_cm=178.0,
        activity_level="very_active", name=name,
    )
    _profile.save_profile(p)


class TestEnsureAndGet:
    def test_pins_active_profile_on_first_call(self, db_conn):
        _db.meal_create(db_conn, "Breakfast", "2026-07-11")
        db_conn.commit()
        _day_profile.ensure_day_profile(db_conn, "2026-07-11")
        row = _db.day_profile_get(db_conn, "2026-07-11")
        assert row is not None
        assert row["profile_name"] == "Default"
        assert not row["overridden"]

    def test_no_op_once_pinned(self, db_conn):
        _day_profile.ensure_day_profile(db_conn, "2026-07-11")
        first = dict(_db.day_profile_get(db_conn, "2026-07-11"))
        # Switch active profile, then create a meal on the SAME date — the
        # existing pin must not move.
        _save_travel_profile()
        _profile.set_active_profile_name("Travel")
        _day_profile.ensure_day_profile(db_conn, "2026-07-11")
        second = dict(_db.day_profile_get(db_conn, "2026-07-11"))
        assert second["profile_name"] == first["profile_name"] == "Default"
        assert second["pinned_at"] == first["pinned_at"]

    def test_switching_profile_does_not_affect_past_dates(self, db_conn):
        _day_profile.ensure_day_profile(db_conn, "2026-07-01")
        _save_travel_profile()
        _profile.set_active_profile_name("Travel")
        _day_profile.ensure_day_profile(db_conn, "2026-07-15")

        old_day = _day_profile.get_profile_for_date(db_conn, "2026-07-01")
        new_day = _day_profile.get_profile_for_date(db_conn, "2026-07-15")
        assert old_day.name == "Default"
        assert new_day.name == "Travel"

    def test_snapshot_survives_later_profile_edits(self, db_conn):
        """Editing a profile's numbers afterward must not retroactively
        change a day already pinned to it."""
        _day_profile.ensure_day_profile(db_conn, "2026-07-01")

        edited = _profile.UserProfile(
            age=99, sex="male", weight_kg=200.0, height_cm=178.0,
            activity_level="sedentary", name="Default",
        )
        _profile.save_profile(edited)

        pinned = _day_profile.get_profile_for_date(db_conn, "2026-07-01")
        assert pinned.weight_kg == 75.0
        assert pinned.age == 35


class TestBackfill:
    def test_backfills_dates_missing_a_pin(self, db_conn):
        _db.meal_create(db_conn, "Lunch", "2026-06-01")
        _db.meal_create(db_conn, "Dinner", "2026-06-02")
        db_conn.commit()
        assert _db.day_profile_get(db_conn, "2026-06-01") is None

        count = _day_profile.backfill_missing_day_profiles(db_conn)

        assert count == 2
        assert _db.day_profile_get(db_conn, "2026-06-01")["profile_name"] == "Default"
        assert _db.day_profile_get(db_conn, "2026-06-02")["profile_name"] == "Default"

    def test_idempotent(self, db_conn):
        _db.meal_create(db_conn, "Lunch", "2026-06-01")
        db_conn.commit()
        _day_profile.backfill_missing_day_profiles(db_conn)
        assert _day_profile.backfill_missing_day_profiles(db_conn) == 0


class TestOverride:
    def test_override_reassigns_and_marks_manual(self, db_conn):
        _save_travel_profile()
        _day_profile.ensure_day_profile(db_conn, "2026-07-11")

        ok = _day_profile.set_day_profile_override(db_conn, "2026-07-11", "Travel")

        assert ok
        row = _db.day_profile_get(db_conn, "2026-07-11")
        assert row["profile_name"] == "Travel"
        assert row["overridden"]

    def test_override_unknown_profile_fails(self, db_conn):
        assert not _day_profile.set_day_profile_override(db_conn, "2026-07-11", "Nonexistent")

    def test_override_only_affects_its_own_date(self, db_conn):
        _save_travel_profile()
        _day_profile.ensure_day_profile(db_conn, "2026-07-01")
        _day_profile.ensure_day_profile(db_conn, "2026-07-02")

        _day_profile.set_day_profile_override(db_conn, "2026-07-01", "Travel")

        assert _day_profile.get_profile_for_date(db_conn, "2026-07-01").name == "Travel"
        assert _day_profile.get_profile_for_date(db_conn, "2026-07-02").name == "Default"


class TestProteinTargetForDate:
    def test_uses_pinned_profile_not_active_one(self, db_conn):
        _save_travel_profile()
        _day_profile.ensure_day_profile(db_conn, "2026-07-01")  # pins Default
        _profile.set_active_profile_name("Travel")

        target_default = _day_profile.protein_target_for_date(db_conn, "2026-07-01")
        rda_default = _profile.compute_rda(_profile.load_profile("Default"))
        assert target_default == pytest.approx(rda_default["protein_g"][0])
