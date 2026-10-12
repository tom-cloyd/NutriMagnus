VERSION = "2026-10-11:1930"

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
RELEASE_VERSION = "0.1.0-rc.26"

# A short, plain-language note shown next to VERSION on the home page and
# used to describe this build in the update-available banner (see
# numa_app/services/update_check.py). Hand-updated at the same time as
# VERSION, alongside the Part 11 changelog entry it summarizes — pick
# whichever of these best matches that entry's size, or write a short one
# of your own in the same spirit. Don't point readers at "the manual" or
# "the top of the manual" here — home.html already appends its own link to
# Part 11 (the changelog) right after this note, so the note itself only
# needs to describe the change, not say where to read more:
#   "minor problem fixes"
#   "minor function added or improved"
#   "significant improvements implemented"
NEW_VERSION_NOTE = "Water intake, split into water from drinks and water from food, with a one-click fill-in of water for all USDA foods, a check for a wet food picked in place of a dry one, a Settings switch, and a warning from age 65 when drinks fall below the older-adult minimum; protein per meal on meal and day pages; protein complement suggestions now count each food at its own digestibility and stay within a sensible amount per meal; deleting a recipe now warns first when meals or other recipes use it; a whole column of missing data can be marked not needed at once, and a button lists foods USDA has no water value for; Meals and Log shows each meal as a share of the day goal for each nutrient; water goals from IOM or EFSA, a drinks fluid limit, and a weight-based water figure for comparison; saving your profile re-scores today, and any day can switch between its pinned profile and your current one; manual search says plainly when nothing matches; every food and recipe name shows its code; recipes built on a sub-recipe now weigh what they should on Compare; Compare can show recipes as written, per serving or whole; Compare shows every nutrient, omega fatty acids included, and names the ones none of the items has data for; renaming a food now renames it in your recipes, logged meals and pantry too; a food page shows its notes; Food use in recipes can filter by name"
