"""
day_profile.py — pin which user profile applies to a given logged day (CLI +
web), so RDA/DCP comparisons for a past date use the profile that was active
then rather than whichever profile is active now. Users can maintain several
named profiles and switch the active one (illness, travel, weight change),
so "today's active profile" is the wrong thing to compare an old day against.

A day's profile is pinned the first time a meal is saved for that date (a
full numeric snapshot, not just a name reference, so later edits to that
profile don't retroactively change historical comparisons) and can be
reassigned afterward via set_day_profile_override.
Docs: README-numa-documentation.md, Architecture: "numa_app/services/day_profile.py — per-day profile pinning"
"""
import json
from dataclasses import asdict

import db as _db
import profile as _profile


def _snapshot(p: _profile.UserProfile) -> str:
    return json.dumps(asdict(p))


def _from_snapshot(row) -> _profile.UserProfile:
    return _profile.UserProfile(**json.loads(row["profile_json"]))


def ensure_day_profile(conn, meal_date: str) -> None:
    """Pin meal_date to the currently-active profile if it has no pinned
    profile yet. No-op once a day_profile row exists — pinning only ever
    happens once per date unless explicitly overridden."""
    if _db.day_profile_get(conn, meal_date) is not None:
        return
    p = _profile.load_profile()
    if p is None:
        return
    _db.day_profile_upsert(conn, meal_date, p.name, _snapshot(p), overridden=False)


def get_profile_for_date(conn, meal_date: str) -> "_profile.UserProfile | None":
    """Return the profile pinned to meal_date, pinning it first if needed."""
    ensure_day_profile(conn, meal_date)
    row = _db.day_profile_get(conn, meal_date)
    if row is None:
        return None
    return _from_snapshot(row)


def backfill_missing_day_profiles(conn) -> int:
    """Pin every currently-logged date that has no day_profile row yet to
    today's active profile. Called once at app startup so existing data
    doesn't require the user to touch a day before it gets a profile."""
    dates = _db.day_profile_dates_missing(conn)
    for meal_date in dates:
        ensure_day_profile(conn, meal_date)
    return len(dates)


def protein_target_for_date(conn, meal_date: str, diet_pref: str = "all") -> float | None:
    """The daily protein RDA target from the profile pinned to meal_date (not
    whatever profile happens to be active now). Callers use this in place of
    loading `profile.load_profile()` directly when scoring a specific date."""
    p = get_profile_for_date(conn, meal_date)
    if p is None:
        return None
    rda = _profile.compute_rda(p, diet_pref=diet_pref)
    target = rda.get("protein_g", (0.0,))[0] if rda else None
    return target or None


def set_day_profile_override(conn, meal_date: str, profile_name: str) -> bool:
    """Reassign meal_date to a specific named profile, snapshotting it and
    marking the day as manually overridden. Returns False if profile_name
    doesn't exist. Caller is responsible for refreshing day_pct_goal
    afterward (each of CLI/web already has its own refresh routine that
    filters complete/incomplete meals slightly differently)."""
    p = _profile.load_profile(profile_name)
    if p is None:
        return False
    _db.day_profile_upsert(conn, meal_date, p.name, _snapshot(p), overridden=True)
    return True
