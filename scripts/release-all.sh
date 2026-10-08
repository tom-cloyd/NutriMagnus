#!/usr/bin/env bash
# release-all.sh — cut a full release: Linux, then Windows, in that order.
# Run via `make release-all`.
#
# Runs `make push-release` (starter-data check, upgrade smoke test, git push,
# GitHub release with the Linux binary), then `make release-windows` (build
# the .exe on the VM and attach it to that same release). Sequential, never
# parallel: the Windows upload attaches to the newest release, which the
# Linux step is what creates.
#
# Interactive by design — whenever it needs something it asks at the
# terminal instead of failing: a missing GITHUB_TOKEN, uncommitted changes,
# a final go-ahead before anything is pushed, and what to do if the Windows
# build fails (retry, retry with a fixed VM IP, or stop — the Linux release
# is already out by then and is never redone).
# Docs: README-numa-documentation.md, Maintenance: "Cutting a release"

set -uo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

ask() {  # ask "Question" default(y|n) -> 0 for yes
    local reply
    read -r -p "$1 " reply
    reply="${reply:-$2}"
    [[ "$reply" =~ ^[Yy] ]]
}

if [[ ! -t 0 ]]; then
    echo "release-all needs to ask you things — run it from a terminal: make release-all" >&2
    exit 1
fi

# ── GitHub token ────────────────────────────────────────────────────────────
if [[ -z "${GITHUB_TOKEN:-}" ]]; then
    echo "GITHUB_TOKEN is not set — both the Linux and Windows steps need it."
    if command -v gh >/dev/null && gh auth token >/dev/null 2>&1 \
            && ask "Use the token from your GitHub CLI (gh) login? [Y/n]" y; then
        GITHUB_TOKEN="$(gh auth token)"
    else
        read -r -s -p "Paste a GitHub token with repo write access (input hidden): " GITHUB_TOKEN
        echo
    fi
    [[ -n "$GITHUB_TOKEN" ]] || { echo "No token given — stopping, nothing done."; exit 1; }
    export GITHUB_TOKEN
fi

# ── Uncommitted changes ─────────────────────────────────────────────────────
if [[ -n "$(git status --porcelain)" ]]; then
    echo "You have uncommitted changes — they will NOT be in this release:"
    git status --short
    ask "Release anyway, without them? [y/N]" n || { echo "Stopped — commit first, then re-run."; exit 1; }
fi

# ── Final go-ahead ──────────────────────────────────────────────────────────
echo
echo "About to release from commit: $(git log --oneline -1)"
echo "Unpushed commits: $(git rev-list --count @{u}..HEAD 2>/dev/null || echo '?')"
echo "This pushes to GitHub and publishes a public release (Linux, then Windows)."
ask "Go ahead? [y/N]" n || { echo "Stopped — nothing done."; exit 1; }

# ── Linux ───────────────────────────────────────────────────────────────────
echo
echo "==> Step 1 of 2: Linux release (make push-release)"
if ! make push-release; then
    echo
    echo "The Linux step stopped (see above). Nothing was sent to Windows."
    echo "If it stopped before pushing, fix the problem and re-run make release-all."
    exit 1
fi

# ── Windows ─────────────────────────────────────────────────────────────────
echo
echo "==> Step 2 of 2: Windows build + upload to the release just created"
until make release-windows; do
    echo
    echo "The Windows step failed. The Linux release is already published and stays as is."
    echo "  r = retry"
    echo "  i = retry with a fixed VM IP address (e.g. 192.168.122.39)"
    echo "  q = stop here (later: make release-windows)"
    read -r -p "Choice [r/i/q]: " choice
    case "$choice" in
        i|I) read -r -p "VM IP address: " ip; export NUMA_VM_IP="$ip" ;;
        q|Q) echo "Stopped. Run 'make release-windows' later to add the .exe."; exit 1 ;;
        *)   ;;
    esac
done

echo
echo "Done — Linux and Windows are both on the release: https://github.com/tom-cloyd/NutriMagnus/releases"
