# Search terms lines in user-manual.md

Moved from `CLAUDE.md` (2026-11-12) so it loads only when a task needs it; `CLAUDE.md` points here. Read before writing or editing a manual section.

## Search terms lines (user-manual.md)

The manual's sidebar search matches only words actually in a section. When you write or
edit a manual section about a topic readers are likely to search for using words the
section doesn't contain (synonyms, everyday terms, other spellings: *seniors* for a
section that says "65 and over"), give it a search-terms line:

```
*Search terms: seniors, elderly, older adults, over 65, ageing, aging.*
```

- One line on its own, with a blank line after it, just under the heading (after any
  `<span id>` anchor lines). Exactly that form: `build_manual.py` hides it on the page
  (search still sees it), and fails the build on a line that starts like one but isn't
  in that form, since that would show as visible text.
- A handful of terms; don't repeat words already in the section's heading or prose.
- American spelling only (fiber, color, aging), no British variants, here or anywhere
  in the manual. Published titles, journal names and URLs quoted in footnotes keep
  their own spelling.
- **When you change a section that has one, reread its list:** drop terms the section no
  longer covers, add any the new wording calls for.
- Not every section needs one. Weekly sweep item 10 checks the week's changed sections
  (`python scripts/search_terms_review.py` lists them);
  the monthly full manual audit (README, *Monthly deep check*) checks every section.
