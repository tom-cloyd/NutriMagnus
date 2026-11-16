VERSION = "2026-11-15:0553"

# RELEASE_VERSION is the human-facing SemVer identifier (MAJOR.MINOR.PATCH,
# optionally with a -rc.N/-beta.N/-alpha.N pre-release suffix) shown to users
# alongside the VERSION build stamp above. It's purely a display label —
# release tagging and the update-available check both key off VERSION (the
# build timestamp), not this, so bumping it doesn't affect either. The
# -rc.N/-beta.N/-alpha.N counter advances only when an actual release is cut
# (decided 2026-09-21 -- previously scripts/bump_version.py auto-incremented
# it on every dev-session bump, which drifted it away from the real release
# count); bump the MAJOR.MINOR.PATCH part by hand only for a deliberate
# milestone (e.g. reaching 1.0.0).
RELEASE_VERSION = "0.1.0-rc.29"

# A short, plain-language note shown next to VERSION on the home page and
# used to describe this build in the update-available banner (see
# numa_app/services/update_check.py). Hand-updated at the same time as
# VERSION, alongside the changelog entry it summarizes — pick
# whichever of these best matches that entry's size, or write a short one
# of your own in the same spirit. Don't point readers at "the manual" or
# "the top of the manual" here — home.html already appends its own link to
# the manual's What's new section right after this note, so the note itself only
# needs to describe the change, not say where to read more:
#   "minor problem fixes"
#   "minor function added or improved"
#   "significant improvements implemented"
# Once the note grows past a sentence or two, write it in two parts, kept on
# one line (no newlines: it is copied into the manual's one-line "Version
# overview:"): "SUMMARY: <one succinct sentence> DETAILS: <the full note>".
# The labels are in capitals. Each time the details change, re-check the
# summary against them: every claim must still be true and must not
# overstate the details.
NEW_VERSION_NOTE = (
    "SUMMARY: each food's data problems, and their fixes, now in one place; smarter searches (leave words out with `!`, retry USDA with your words reversed, a how-to hint under every search box, arrow keys through results); meals and recipes can be marked complete, and recipes and foods marked as drinks, straight from lists and searches; Compare keeps your picks across searches; a shorter, reorganized manual with a Return button; and Settings tests a USDA API key before saving it. "
    "DETAILS: New Problems by food page (Foods → 9) and an Everything to check on this food box on each food's page: all of a food's data problems in one place, with their fixes. Searches no longer put partial matches from your own data above full matches when you already have an item matching every word, singular and plural search words match each other, a food can be deleted from its own page, and each meal item now records and shows the time of day it was entered. Recipes can be marked complete or as drinks, and foods as drinks, straight from the Recipes list and every search; arrow keys move through search results, and Back returns to the one you opened; Print pages and other NuMa links stay in NuMa's own window; quiet buttons are blue; the manual's search opens the section you picked, with your words highlighted; and Compare ticks are kept as you search again or move between lists, so one comparison can gather foods from several searches. A `!` before a search word leaves out results with that word (`beans red !kidney cooked`), and the list says how many results they hid; a search for a cooked food no longer misses canned products online; a hint under every search box sums up how to write a search; and NuMa offers to search USDA again with your words reversed, which finds many branded products. On the Annotate page, each estimate being asked for has its own Skip button beside it, and the Meals & Log list's Complete column is a checkbox, so a meal can be marked complete without opening it. On a meal, the Add Food or Recipe header, search box and search hint line up along the top, and the hint's Learn more opens the manual at word order. A `!` word works in list filter boxes too (Recipes, Food Cache, My Pantry, Search meal history and the rest). Removing an item from a meal no longer makes the page jump around. The User Manual is reorganized and much shorter, with step-by-step workflows. A Return button above the manual (Alt+Shift+U) goes straight back to the page you came from, and Manual reopens it where you left off; and Settings checks a USDA API key with USDA before saving it, with a Test key button."
)
