# Changelog and version-stamp rules

Moved from `CLAUDE.md` (2026-11-12) so it loads only when a task needs it; `CLAUDE.md` points here. Read before writing a changelog entry or cutting a release.

## Version stamp (from CLAUDE.md's Key Invariants)

- **Bump `version.py`'s `VERSION` stamp before ending any session that changed application behavior** (bug fixes, features, refactors — not pure docs/comments). Run `python3 scripts/bump_version.py` — it sets `VERSION` to the current timestamp; never hand-edit that line. `NEW_VERSION_NOTE` still needs a manual edit to describe the change. Write it in two parts, with both labels in capitals: `SUMMARY:` followed by a short bulleted list of the most important changes, one `* ` bullet per line (adopted 2026-11-23), then `DETAILS: <full note>` on one line. Each time the details change, review the summary for correctness against them: every claim must still be true, and none may overstate the details (adopted 2026-11-15). If `user-manual.md` or `README-numa-documentation.md` were also edited, update their header stamps by hand the same way (see each file's top few lines for the exact format). `RELEASE_VERSION`'s `-rc.N` counter is separate and deliberately NOT bumped on every session (decided 2026-09-21) — it advances only when an actual release is cut, so it stays a meaningful release count rather than a session count.

## Changelog: two files (since 2026-11-14)

Any turn that changes numa's user-facing behavior (new feature, bug fix, threshold change —
not pure layout/wording tweaks, since the owner is currently numa's only user and already
knows about those) ends with **two** additions, plus the `version.py`/manual timestamp bump above:

1. **A dated entry in `docs/updates-log-details.md`**, inserted right after its
   `<!-- Insert new updates below here -->` marker, newest on top, under today's
   `#### Month Day updates` heading (create it if today has none). Every entry title starts
   with `MANUAL: ` or `PROGRAM: ` (e.g. `**PROGRAM: ALL-CAPS TITLE**`). Format below.
2. **A one-line, numbered summary bullet in `user-manual.md`'s What's new section**
   (`## What's new {: #updates-log}`, after the Appendices), under the
   `#### Next release summary to this point` heading that sits right after that section's
   own `<!-- Insert new updates below here -->` marker. Newest on top. Prefix a bullet with
   `MANUAL: ` only for manual-only changes; program changes take no prefix. This running list
   is what users read in the manual; the details file is for developers only. The GitHub
   release page shows only the Version overview's SUMMARY (see "When a release is cut").

(Until 2026-11-14 both lived in the manual, as Part 11 "Recent program updates log"; earlier
Appendix A, and before 2026-08-05 Appendix K.)

**Each summary bullet is numbered** (adopted 2026-10-07, so the reader can see how
many updates are pending): oldest is 1, newest highest, newest on top — e.g.
`- **13.** New item.` above `- **12.** ...`. A new bullet takes the next number up;
nothing else is renumbered. The number is written into a plain bullet because a
Markdown ordered list can only count upward. Don't put a count in the heading — it
would go stale. Numbering restarts at 1 after each release.

**Version overview at every commit** (adopted 2026-10-17): when making a commit, copy
`version.py`'s `NEW_VERSION_NOTE` into the What's new section, first thing under
`#### Next release summary to this point`, above the numbered bullets — replacing the
previous overview if there is one, so there's only ever one. **Split it into three
paragraphs** (adopted 2026-11-15; one long line was unreadable): `Version overview:` alone
on its line, then the `SUMMARY: …` part, then the `DETAILS: …` part, each separated by a
blank line. **The SUMMARY part is a bulleted list too** (adopted 2026-11-23): `SUMMARY:`
alone on its line, a blank line, then the note's `* ` bullets as they are. **The DETAILS part is a bulleted list** (adopted 2026-11-15; a paragraph of
details was unreadable): `DETAILS:` alone on its line, a blank line, then each detail as its
own `* ` bullet (asterisk, so it can't be mistaken for the numbered `- **N.**` bullets).
In `version.py` the DETAILS stay one line; only the manual's copy is split into bullets.

**The layout to end up with in the manual**, reading down from the marker:

```
<!-- Insert new updates below here -->

#### Next release summary to this point

Version overview:

SUMMARY:

* Most important change.
* Next one.

DETAILS:

* One detail.
* Another detail.

- **13.** Newest bullet.    <- your new one-line summary goes on top, next number up
- **12.** Older bullet.

#### Release v<tag> summary <- the previous release; never add to it
```

**And in `docs/updates-log-details.md`:**

```
<!-- Insert new updates below here -->

#### Month Day updates      <- today's date heading (create if not already today's)

**PROGRAM: ALL-CAPS TITLE** <- your new dated entry, newest on top
...
## Release v<tag> — dated entries released in it   <- added by create_release.py
```

**When a release is cut**, `scripts/create_release.py` publishes, as the GitHub release
page, only the SUMMARY of the Version overview, its bullets (found between the manual's marker
and the nearest `#### Release ... summary` heading), without its label, followed by the line
"See full list of changes in the User Manual's 'What's New' section" (adopted 2026-11-15:
the whole overview and every bullet was more than anyone reads). No SUMMARY there, and the
release stops with an error. **So keep the SUMMARY brief and to the point:** it is the one
thing users see before they download. It then renames the running heading in place to
`#### Release <tag> summary`, and adds a `## Release <tag> — dated entries released in it`
heading under the details file's marker. Don't hand-insert release headings in either file.
**After a release** the manual's running heading is gone, so the next update re-creates a
fresh `#### Next release summary to this point` heading between the manual's marker and the
newest `#### Release <tag> summary` line, with its first bullet. (If the running heading is
missing at release time, the script inserts one under the marker, so a release never breaks,
but it'll have no bullets, which is the thing to avoid.)

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

**Keep the `<!-- -->` around the Scope fence.** Release notes no longer include the dated entries, and the details file isn't rendered, but the convention keeps entries readable and lets an entry be pasted anywhere (the manual, a release page) without its Scope block showing. Checklist for every new entry: prose paragraph → blank line → `<!--` alone on its own line → blank line → ` ``` ` fence → Scope text → ` ``` ` fence → blank line → `-->` alone on its own line.

Entries before 2026-07-31 remain in the old single-line format (`* ALL-CAPS SUMMARY -
scope - description.`) — deliberately not reformatted retroactively; use the new format
only going forward. A dated entry's `[learn more...](#anchor)` link can't be followed from the details file, but keep it: it names the manual section, and the anchor is checked by nothing there, so make sure it exists in the manual. After editing the manual, run `python3 scripts/build_manual.py` — it
recomputes the "Reading time" header figure and regenerates `user-manual.html`; don't
hand-edit reading time.
