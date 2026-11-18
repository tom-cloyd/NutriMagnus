"""
recipe_edit_effects.py — the recipe Edit page's optional "effect of this
change" reports: how a recipe's per-serving nutrients moved since the last
report (or since the edit session began), written to
recipe-edit-effects-data.md.

An edit session starts when the Edit page is opened from any other page
(web/backend.py decides, from the Referer, and calls start_session()). Before
the first ingredient change after a report, the recipe's state is recorded
(before_change()), so one report covers every change since: remove X, then
add Y, reports the exchange. Each add, remove or amount change is described
(after_change()) and leaves an offer for the next page load (take_offer()).

The file is overwritten by the first report of a new session and appended to
after that, so it holds one session's reports and stays after the page
closes. Session state lives in memory only: a restart starts afresh.

Docs: README-numa-documentation.md, Project Structure tree entry for
recipe_edit_effects.py; user-manual.md #recipe-edit-effects
"""
import sys
import threading
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import db as _db
import platform_utils as _platform
import usda as _usda
from numa_app.services import glycemic_load as _gl
from numa_app.services import water as _water
from numa_app.services.recipe_dcp import recipe_dcp_per_serving
from numa_app.services.recipe_nutrients import expand_recipe_ingredients, recipe_total_nutrients

FILE_NAME = "recipe-edit-effects-data.md"

# From source: the project root. The packaged app has no project folder, so
# its data folder (beside the database) instead.
_FILE: Path = (_platform.get_data_dir() if getattr(sys, "frozen", False)
               else Path(__file__).resolve().parents[2]) / FILE_NAME

ALL = "__all__"             # every nutrient
ALL_CHANGED = "__all5__"    # every nutrient that changed by CHANGED_PCT or more
CHANGED_PCT = 5.0

DCP_KEY, GL_KEY = "dcp", "gl"


def file_path() -> Path:
    return _FILE


@dataclass
class Session:
    token: str
    recipe_id: int
    baseline: dict | None = None        # snapshot() before the first unreported change
    changes: list[str] = field(default_factory=list)
    steps: list[dict | None] = field(default_factory=list)   # snapshot() after each change
    offer: bool = False                 # show the offer on the next page load
    selection: list[str] = field(default_factory=list)
    reports: int = 0
    gi_opt_out: bool = False            # as given to the last before_change()


_lock = threading.Lock()
_sessions: dict[int, Session] = {}
_file_token: str | None = None          # the session whose reports the file holds


def start_session(recipe_id: int) -> Session:
    """A new edit session for this recipe: forgets the recorded state, the
    unreported changes and the remembered nutrient choice. The file itself is
    replaced only when this session writes its first report."""
    with _lock:
        s = _sessions[recipe_id] = Session(uuid.uuid4().hex, recipe_id)
        return s


def session(recipe_id: int) -> Session:
    """This recipe's current session, starting one if there is none (the
    server restarted while the page was open)."""
    with _lock:
        s = _sessions.get(recipe_id)
    return s or start_session(recipe_id)


def snapshot(conn, recipe_id: int, *, gi_opt_out: bool = False) -> dict | None:
    """The recipe's per-serving nutrients, DCP and glycemic load now."""
    recipe = _db.recipe_get(conn, recipe_id)
    if not recipe:
        return None
    servings = float(recipe["servings"] or 1) or 1.0
    total = recipe_total_nutrients(recipe_id, conn)
    leaves = expand_recipe_ingredients(recipe_id, conn, portion_factor=1 / servings)
    gl = _gl.gl_for_leaves(leaves, conn, gi_opt_out=gi_opt_out) if leaves else None
    return {
        "name": recipe["name"],
        "servings": servings,
        "per_serving": {k: v / servings for k, v in total.items() if not k.startswith("aa_")},
        DCP_KEY: recipe_dcp_per_serving(recipe_id, conn)[0],
        GL_KEY: gl["total"] if gl else None,
        "gl_complete": gl["complete"] if gl else True,
    }


def before_change(conn, recipe_id: int, *, gi_opt_out: bool = False) -> None:
    """Call just before an ingredient change: records the recipe as it is,
    unless a change since the last report already did."""
    s = session(recipe_id)
    s.gi_opt_out = gi_opt_out
    if s.baseline is None:
        s.baseline = snapshot(conn, recipe_id, gi_opt_out=gi_opt_out)


def after_change(recipe_id: int, description: str) -> None:
    """Call once an ingredient change is saved (its connection closed, so
    this reads the saved state): lists it, records the recipe as it now is
    (a report shows each step), and offers a report on the next page load."""
    s = session(recipe_id)
    with _db.get_db() as conn:
        step = snapshot(conn, recipe_id, gi_opt_out=s.gi_opt_out)
    s.changes.append(description)
    s.steps.append(step)
    s.offer = True


def take_offer(recipe_id: int) -> Session | None:
    """The session, if a change since the last page load is waiting for an
    answer; the offer is shown once (ignoring it is the same as No)."""
    with _lock:
        s = _sessions.get(recipe_id)
        if not s or not s.offer or not s.changes:
            return None
        s.offer = False
        return s


def has_reports(recipe_id: int) -> bool:
    """True once this recipe's session has written to the file (and the
    file still holds that session's reports)."""
    with _lock:
        s = _sessions.get(recipe_id)
        return bool(s and s.reports and _file_token == s.token and _FILE.exists())


# ---------------------------------------------------------------------------
# The report
# ---------------------------------------------------------------------------

def _places(*values: float | None) -> int:
    """Decimal places for a row: one precision for its before, after and
    change, set by the larger of before and after."""
    big = max((abs(v) for v in values if v is not None), default=0.0)
    return 0 if big >= 100 else 1 if big >= 10 else 2


def _fmt(v: float | None, places: int, sign: bool = False) -> str:
    if v is None:
        return "?"
    return f"{v:{'+' if sign else ''},.{places}f}"


def _row(label: str, unit: str, b: float | None, a: float | None,
         steps: list[float | None] = (), *, keep: bool = False) -> dict | None:
    """One nutrient: before, after, and the values after each change in
    between (steps). Change and change % are before -> after. None when it
    has no value anywhere, unless `keep`."""
    if not keep and not b and not a and not any(steps):
        return None
    if b is None or a is None:
        delta = pct = None
    else:
        delta = a - b
        pct = delta / b * 100 if b else (float("inf") if delta else 0.0)
    return {"label": label, "unit": unit, "before": b, "after": a, "steps": list(steps),
            "delta": delta, "pct": pct}


def _pct_text(pct: float | None) -> str:
    if pct is None:
        return "?"
    if pct == float("inf"):
        return "new"
    if abs(pct) < 0.05:
        return "0%"
    return f"{pct:+.1f}%"


def _changed_enough(r: dict) -> bool:
    return r["pct"] is None or abs(r["pct"]) >= CHANGED_PCT


def build_sections(before: dict, after: dict, groups: list[tuple[str, list[str]]],
                   selection: list[str], *, include_gl: bool = True,
                   steps: list[dict] = ()) -> list[tuple[str, list[dict]]]:
    """[(group name, rows)] for the chosen groups (or every group, for ALL /
    ALL_CHANGED). DCP follows protein and glycemic load ends the group
    holding carbohydrate, as on the What-if page. `steps` are the snapshots
    between before and after (after each change but the last); the 5% filter
    looks at before -> after only. Nutrients present but in no
    group come last as "Other" (never water: when it isn't in `groups`,
    water tracking is off)."""
    b, a = before["per_serving"], after["per_serving"]
    mids = [st["per_serving"] for st in steps]
    known = {k for _, keys in groups for k in keys}
    extra = sorted(k for k in set(b).union(a, *mids) if k not in known and k not in _water.ALL_KEYS)
    every = list(groups) + ([("Other", extra)] if extra else [])
    whole = ALL in selection or ALL_CHANGED in selection
    out = []
    for name, keys in every:
        if not whole and name not in selection:
            continue
        rows = []
        for k in keys:
            label, unit = _usda.nutrient_label(k)
            rows.append(_row(label, unit, b.get(k, 0.0), a.get(k, 0.0), [m.get(k, 0.0) for m in mids]))
            if k == "protein_g" and rows[-1]:
                # Always beside raw protein, even when it can't be worked
                # out anywhere ("?" throughout says so).
                rows.append(_row("Protein (DCP)", "g", before[DCP_KEY], after[DCP_KEY],
                                 [st[DCP_KEY] for st in steps], keep=True))
        if include_gl and "carbs_g" in keys:
            r = _row("Glycemic load", "", before[GL_KEY], after[GL_KEY], [st[GL_KEY] for st in steps])
            if r and not all(x["gl_complete"] for x in (before, after, *steps)):
                r["label"] += " (some foods have no GI)"
            rows.append(r)
        rows = [r for r in rows if r]
        if ALL_CHANGED in selection:
            rows = [r for r in rows if _changed_enough(r)]
        if rows:
            out.append((name, rows))
    return out


def _selection_text(selection: list[str]) -> str:
    if ALL_CHANGED in selection:
        return f"all nutrients that changed by {CHANGED_PCT:g}% or more"
    if ALL in selection:
        return "all nutrients"
    return ", ".join(selection)


def report_markdown(n: int, before: dict, after: dict, changes: list[str],
                    sections: list[tuple[str, list[dict]]], selection: list[str],
                    when: datetime) -> str:
    """One report, as Markdown: the changes it covers, then a table per group."""
    lines = [f"## Report {n} — {when:%H:%M}", "",
             "Changes since " + ("the last report:" if n > 1 else "the edit session began:"), ""]
    lines += [f"{i}. {c}" for i, c in enumerate(changes, 1)]
    lines += ["", f"Showing: {_selection_text(selection)}, per serving."]
    # One column per step, when every step was recorded (see write_report()).
    many = len(changes) > 1 and all(len(r["steps"]) == len(changes) - 1
                                    for _name, rows in sections for r in rows)
    if many:
        last = len(changes)
        lines += ["", f"**Before** is the recipe before change 1; **After 1** to **After {last}** are the "
                      f"recipe after each change. **Change** and **Change %** are the whole effect, "
                      f"Before to After {last}" + (" (the 5% filter looks at that too)."
                                                   if ALL_CHANGED in selection else ".")]
    if before["servings"] != after["servings"]:
        lines += ["", f"Servings changed from {before['servings']:g} to {after['servings']:g}, "
                      "which changes every per-serving figure too."]
    lines.append("")
    if not sections:
        if ALL_CHANGED in selection:
            lines += [f"No nutrient changed by {CHANGED_PCT:g}% or more.", ""]
        else:
            lines += ["None of the chosen nutrients has a value in this recipe.", ""]
    unknown = False
    for name, rows in sections:
        heads = ["Before"] + ([f"After {i}" for i in range(1, len(changes) + 1)] if many else ["After"])
        lines += [f"### {name}", "",
                  "| Nutrient | " + " | ".join(heads) + " | Change | Change % |",
                  "|---|" + "---:|" * (len(heads) + 2)]
        for r in rows:
            label = f"{r['label']} ({r['unit']})" if r["unit"] else r["label"]
            values = [r["before"], *(r["steps"] if many else []), r["after"]]
            unknown = unknown or None in values
            places = _places(*values)
            if r["delta"] is None:
                delta = "?"
            elif abs(r["delta"]) < 0.5 * 10 ** -places:
                delta = "0"
            else:
                delta = _fmt(r["delta"], places, sign=True)
            cells = " | ".join(_fmt(v, places) for v in values)
            lines.append(f"| {label} | {cells} | {delta} | {_pct_text(r['pct'])} |")
        lines.append("")
    if unknown:
        lines += ["? = can't be worked out at that point. For Protein (DCP), a food that supplies much of "
                  "the protein has no amino acid data.", ""]
    return "\n".join(lines)


def write_report(conn, recipe_id: int, selection: list[str], groups: list[tuple[str, list[str]]], *,
                 include_gl: bool = True, gi_opt_out: bool = False,
                 now: datetime | None = None) -> Path | None:
    """Writes a report on the changes since the last one, and starts the
    next from here. Returns the file's path, or None when there is nothing
    to report (no change since the last report, nothing chosen, or the
    recipe is gone)."""
    global _file_token
    s = session(recipe_id)
    if not s.changes or s.baseline is None or not selection:
        return None
    after = snapshot(conn, recipe_id, gi_opt_out=gi_opt_out)
    if after is None:
        return None
    now = now or datetime.now()
    mids = [st for st in s.steps[:-1] if st is not None]
    if len(mids) != len(s.steps) - 1:
        mids = []           # a step couldn't be recorded: show before and after only
    sections = build_sections(s.baseline, after, groups, selection, include_gl=include_gl, steps=mids)
    with _lock:
        fresh = _file_token != s.token or not _FILE.exists()
        text = report_markdown(1 if fresh else s.reports + 1, s.baseline, after, s.changes,
                               sections, selection, now)
        if fresh:
            head = (f"# Recipe edit effects: {after['name']} (R{recipe_id})\n\n"
                    f"Edit session began {now:%Y-%m-%d %H:%M}. Each report compares the recipe, "
                    "per serving, with how it was at the report before it (the first, with how it "
                    "was when the session began).\n\n")
            _FILE.write_text(head + text, encoding="utf-8")
            s.reports = 1
            _file_token = s.token
        else:
            with _FILE.open("a", encoding="utf-8") as f:
                f.write("\n" + text)
            s.reports += 1
        s.selection = list(selection)
        s.baseline = after
        s.changes = []
        s.steps = []
        s.offer = False
    return _FILE


def read_file() -> str:
    try:
        return _FILE.read_text(encoding="utf-8")
    except OSError:
        return ""


def reset_for_tests() -> None:
    """Forget every session (tests start clean)."""
    global _file_token
    with _lock:
        _sessions.clear()
        _file_token = None
