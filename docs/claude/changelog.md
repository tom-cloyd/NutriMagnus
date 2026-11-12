# Changelog and version-stamp rules

Moved from `CLAUDE.md` (2026-11-12) so it loads only when a task needs it; `CLAUDE.md` points here. Read before writing a Part 11 log entry or cutting a release.

## Version stamp (from CLAUDE.md's Key Invariants)

- **Bump `version.py`'s `VERSION` stamp before ending any session that changed application behavior** (bug fixes, features, refactors — not pure docs/comments). Run `python3 scripts/bump_version.py` — it sets `VERSION` to the current timestamp; never hand-edit that line. `NEW_VERSION_NOTE` still needs a manual edit to describe the change. If `user-manual.md` or `README-numa-documentation.md` were also edited, update their header stamps by hand the same way (see each file's top few lines for the exact format). `RELEASE_VERSION`'s `-rc.N` counter is separate and deliberately NOT bumped on every session (decided 2026-09-21) — it advances only when an actual release is cut, so it stays a meaningful release count rather than a session count.

## Changelog (user-manual.md, Part 11)

Any turn that changes numa's user-facing behavior (new feature, bug fix, threshold change —
not pure layout/wording tweaks, since the owner is currently numa's only user and already
knows about those) ends with a new entry under today's `#### Month Day updates`
heading in
**Part 11, "Recent program updates log"** (its own Part at the end of the manual since
2026-09-30; earlier Appendix A, and before 2026-08-05 Appendix K),
plus the `version.py`/manual timestamp bump above.

**Where entries go** (decided 2026-09-21): insert each new entry after the line
`<!-- Insert new updates below here -->` in Part 11, newest on top, under today's
`#### Month Day updates` heading (new form only; older `... program updates` headings stay
as they are). Every entry title starts with `MANUAL: ` or `PROGRAM: ` (e.g.
`**PROGRAM: ALL-CAPS TITLE**`).

**Also add a one-line summary bullet** (adopted 2026-09-23) under the
`#### Next release summary to this point` heading, which sits between the marker and
those dated entries — so every dated entry you write gets a matching bullet, newest on
top. That running list is what the reader (and the GitHub release page) sees first; the
dated entries below it are the detail. Prefix a bullet with `MANUAL: ` only for
manual-only changes; program changes take no prefix. Append ` (dated details below)` to
the heading only while dated entry sections actually follow it.

**Version overview at every commit** (adopted 2026-10-17): when making a commit, copy
`version.py`'s `NEW_VERSION_NOTE` into Part 11 as the first line under
`#### Next release summary to this point`, above the numbered bullets, as
`Version overview: <note text>` — replacing the previous overview line if there is one,
so there's only ever one. `NEW_VERSION_NOTE` is never printed on the home page.

**Each summary bullet is numbered** (adopted 2026-10-07, so the reader can see how
many updates are pending): oldest is 1, newest highest, newest on top — e.g.
`- **13.** New item.` above `- **12.** ...`. A new bullet takes the next number up;
nothing else is renumbered. The number is written into a plain bullet because a
Markdown ordered list can only count upward. Don't put a count in the heading — it
would go stale. Numbering restarts at 1 after each release.

**The layout to end up with**, always, reading down from the marker:

```
<!-- Insert new updates below here -->

#### Next release summary to this point (dated details below)

- **13.** Newest bullet.    <- your new one-line summary goes on top, next number up
- **12.** Older bullet.

#### Month Day updates      <- today's date heading (create if not already today's)

**PROGRAM: ALL-CAPS TITLE** <- your new dated entry, newest on top
...
#### Release v<tag> summary <- the previous release; never edit above-the-line into this
```

**After a release has just been cut** the running heading is gone — `create_release.py`
renamed it to `#### Release v<tag> summary`, which now sits directly under the marker.
So the next log update has to rebuild the top of that structure in order: a fresh
`#### Next release summary to this point` heading, its first bullet, then today's
`#### Month Day updates` heading, then the entry — all inserted between the marker and
that `#### Release v<tag> summary` line. Nothing does this for you; it's the one part
of the cycle that's yours to re-create.

When cutting a release, `scripts/create_release.py` handles the bottom of the cycle: it
renames the running heading in place to `#### Release <tag> summary`, so the summary
you've been keeping becomes that release's summary, with the dated entries left
untouched below it. Pending = everything between the marker and the newest
`#### Release ... summary` heading. Don't hand-insert release headings. (If the running
heading is missing at release time, the script inserts one under the marker itself, so a
release never breaks — but it'll have no summary bullets, which is the thing to avoid.)

Every entry from 2026-07-31 onward uses this format — adopted 2026-08-05 because the prior
single dense run-on line per entry was hard to skim:

```
**PROGRAM: ALL-CAPS TITLE**

One or two plain-language sentences a casual reader can grasp in a hurry. Lead with
what the user can now do / now sees / now gets — NOT with what was wrong before or
how it used to work. A [learn more...](#anchor) link goes here if a relevant manual
section/anchor exists.

<!--
​```
Scope (menu path / files touched), then fuller technical detail — root cause,
mechanism, implementation notes — git-commit-message style. Only include this
block if there's real technical detail worth keeping; skip it for a trivial change.
​```
-->
```

**The `<!-- -->` around the Scope fence is not optional decoration — it's load-bearing.**
Without it the Scope block renders as visible body text in the actual manual (caught
2026-09-11, forgotten at least twice before that fix stuck). Checklist for every new
entry: prose paragraph → blank line → `<!--` alone on its own line → blank line →
` ``` ` fence → Scope text → ` ``` ` fence → blank line → `-->` alone on its own line.
After writing an entry, grep the freshly-built `user-manual.html` for a distinctive
word from that entry's Scope text and confirm it lands between `<!--` and `-->`, not
as bare `<p>`/`<pre>` text — that's the actual verification, not just eyeballing the
markdown source.

Entries before 2026-07-31 remain in the old single-line format (`* ALL-CAPS SUMMARY -
scope - description.`) — deliberately not reformatted retroactively; use the new format
only going forward. After editing the manual, run `python3 scripts/build_manual.py` — it
recomputes the "Reading time" header figure and regenerates `user-manual.html`; don't
hand-edit reading time.
