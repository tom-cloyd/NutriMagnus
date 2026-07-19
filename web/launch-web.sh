#!/usr/bin/env bash
# launch-web.sh — start (or restart) the NutriMagnus web server and open Firefox.
# Safe to run multiple times: kills any stale server on port 8000 first.

set -euo pipefail

NUMA_DIR="/home/tomc/Dropbox/www/__Active/Obsidian-vault/_sync2/Python-work/numa"
PYTHON="$NUMA_DIR/.venv/bin/python"
LAUNCHER="$NUMA_DIR/web/launcher.py"
LOG="$NUMA_DIR/web-server.log"
URL="http://127.0.0.1:8000"

# Kill any existing process on port 8000
if fuser 8000/tcp &>/dev/null 2>&1; then
    fuser -k 8000/tcp &>/dev/null 2>&1 || true
    sleep 0.8
fi

# Start the web server in the background
"$PYTHON" "$LAUNCHER" --no-browser >"$LOG" 2>&1 &
SERVER_PID=$!

# Wait up to 30 seconds for the server to accept connections (cold starts on a
# Dropbox-synced checkout can take longer than a few seconds under load).
SERVER_READY=0
for i in $(seq 1 60); do
    sleep 0.5
    if "$PYTHON" -c "import socket; s=socket.socket(); r=s.connect_ex(('127.0.0.1',8000)); s.close(); exit(r)" 2>/dev/null; then
        SERVER_READY=1
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        notify-send "NutriMagnus" "Web server failed to start. Check $LOG" 2>/dev/null || true
        exit 1
    fi
done

# Only open the browser once the server is confirmed reachable — opening it
# unconditionally after the wait loop (regardless of whether it timed out)
# was the bug: on a slow start the loop would exhaust its budget while the
# server was still starting (not dead, just not ready yet), fall through,
# and open a browser tab against a port nothing was listening on yet —
# Firefox has no reason to retry a plain connection-refused error.
if [ "$SERVER_READY" -eq 1 ]; then
    # Opens a new tab in the running instance and brings the window to front
    firefox "$URL" &>/dev/null &
else
    notify-send "NutriMagnus" "Web server is taking longer than usual to start. Check $LOG, or try again in a few seconds." 2>/dev/null || true
    exit 1
fi
