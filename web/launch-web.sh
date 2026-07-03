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

# Wait up to 8 seconds for the server to accept connections
for i in $(seq 1 16); do
    sleep 0.5
    if "$PYTHON" -c "import socket; s=socket.socket(); r=s.connect_ex(('127.0.0.1',8000)); s.close(); exit(r)" 2>/dev/null; then
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        notify-send "NutriMagnus" "Web server failed to start. Check $LOG" 2>/dev/null || true
        exit 1
    fi
done

# Open Firefox — this opens a new tab in the running instance and brings the window to front
firefox "$URL" &>/dev/null &
