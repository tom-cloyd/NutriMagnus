#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "[OK] Virtual environment created at $ROOT_DIR/.venv"
echo "Activate it with: source .venv/bin/activate"
echo "Run the app with: python numa.py"
