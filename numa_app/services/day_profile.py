"""
day_profile.py — pin which user profile applies to a given logged day, so
RDA/DCP comparisons for a past date use the profile that was active then
rather than whichever profile is active now. Users can maintain several
named profiles and switch the active one (illness, travel, weight change),
so "today's active profile" is the wrong thing to compare an old day against.

A day's profile is pinned the first time a meal is saved for that date (a
full numeric snapshot, not just a name reference) and can be reassigned
afterward via set_day_profile_override.

A new day starts out following the CURRENT profile (follow_current): its own
pinned copy is kept, it is re-pinned whenever the profile is saved
(refresh_after_profile_save), and restore_pinned puts the kept copy back —
from then on, later edits to the profile don't change that day.
Today is re-pinned on every profile save too, unless set by hand — it's
still in progress, so its goals should follow your settings.
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
    profile yet, following the current profile from the start (the snapshot
    taken now is kept as the day's own copy, for restore_pinned). No-op once
    a day_profile row exists — pinning only ever happens once per date
    unless explicitly overridden."""
    if _db.day_profile_get(conn, meal_date) is not None:
        return
    p = _profile.load_profile()
    if p is None:
        return
    snap = _snapshot(p)
    _db.day_profile_upsert(conn, meal_date, p.name, snap, overridden=False)
    _db.day_profile_set_following(conn, meal_date, p.name, snap)


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
    afterward (web/backend.py has its own refresh routine that filters
    complete/incomplete meals)."""
    p = _profile.load_profile(profile_name)
    if p is None:
        return False
    _db.day_profile_upsert(conn, meal_date, p.name, _snapshot(p), overridden=True)
    return True


def follows_current(row) -> bool:
    """Whether a day_profile row follows the current profile."""
    try:
        return bool(row["follows_current"])
    except (IndexError, KeyError, TypeError):
        return False


def follow_current(conn, meal_date: str) -> bool:
    """Score meal_date against the active profile from now on, keeping its
    own pinned copy for restore_pinned. False with no active profile."""
    p = _profile.load_profile()
    if p is None:
        return False
    ensure_day_profile(conn, meal_date)
    _db.day_profile_set_following(conn, meal_date, p.name, _snapshot(p))
    return True


def restore_pinned(conn, meal_date: str) -> bool:
    """Undo follow_current: back to the day's own pinned copy, exactly."""
    return _db.day_profile_restore_original(conn, meal_date)


def refresh_after_profile_save(conn, today: str) -> list[str]:
    """After the profile is saved: re-pin every day that follows the current
    profile, and today unless its profile was set by hand. Returns the dates
    re-pinned (callers refresh their stored day figures)."""
    p = _profile.load_profile()
    if p is None:
        return []
    snap = _snapshot(p)
    dates = list(_db.day_profile_following_dates(conn))
    for d in dates:
        _db.day_profile_set_snapshot(conn, d, p.name, snap)
    row = _db.day_profile_get(conn, today)
    if row is not None and not row["overridden"] and today not in dates:
        _db.day_profile_set_snapshot(conn, today, p.name, snap)
        dates.append(today)
    return dates


def follow_current_between(conn, start: str, end: str) -> list[str]:
    """Switch every logged day from start to end (inclusive) to follow the
    current profile — except days whose profile was set by hand and days
    already following. Returns the dates switched."""
    switched = []
    for row in _db.day_profile_dates_between(conn, start, end):
        if row["overridden"] or follows_current(row):
            continue
        if follow_current(conn, row["meal_date"]):
            switched.append(row["meal_date"])
    return switched
