VERSION = "2026-09-23:2023"

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
RELEASE_VERSION = "0.1.0-rc.21"

# A short, plain-language note shown next to VERSION on the home page and
# used to describe this build in the update-available banner (see
# numa_app/services/update_check.py). Hand-updated at the same time as
# VERSION, alongside the Appendix A changelog entry it summarizes — pick
# whichever of these best matches that entry's size, or write a short one
# of your own in the same spirit. Don't point readers at "the manual" or
# "the top of the manual" here — home.html already appends its own link to
# Appendix A (the changelog) right after this note, so the note itself only
# needs to describe the change, not say where to read more:
#   "minor problem fixes"
#   "minor function added or improved"
#   "significant improvements implemented"
NEW_VERSION_NOTE = "the database itself now refuses to delete a food still in use"
