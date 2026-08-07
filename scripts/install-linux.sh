#!/usr/bin/env bash
# install-linux.sh — one-file installer for NutriMagnus on Linux.
#
# This is the single thing a user downloads (see user-manual.md, Part 1,
# Section A). Running it fetches the actual binary and icon from the latest
# GitHub release and sets everything up:
#   - the program itself:  ~/.local/bin/nutrimagnus
#   - its icon:            ~/.local/share/icons/nutrimagnus.png
#   - an applications-menu entry: ~/.local/share/applications/nutrimagnus.desktop
#
# Entirely per-user — nothing outside $HOME is touched, no root/sudo needed.
# Safe to re-run for an upgrade: it just overwrites the same three files.
set -euo pipefail

REPO="tom-cloyd/NutriMagnus"
BASE_URL="https://github.com/${REPO}/releases/latest/download"

BIN_DIR="$HOME/.local/bin"
ICON_DIR="$HOME/.local/share/icons"
DESKTOP_DIR="$HOME/.local/share/applications"
BIN_PATH="$BIN_DIR/nutrimagnus"
ICON_PATH="$ICON_DIR/nutrimagnus.png"
DESKTOP_PATH="$DESKTOP_DIR/nutrimagnus.desktop"

mkdir -p "$BIN_DIR" "$ICON_DIR" "$DESKTOP_DIR"

echo "Downloading NutriMagnus..."
curl -fL -o "$BIN_PATH" "$BASE_URL/nutrimagnus"
chmod +x "$BIN_PATH"

echo "Downloading icon..."
curl -fL -o "$ICON_PATH" "$BASE_URL/nutrimagnus.png"

cat > "$DESKTOP_PATH" <<EOF
[Desktop Entry]
Type=Application
Name=NutriMagnus
GenericName=Nutritional Analysis
Comment=Nutritional analysis, with a focus on protein quality
Exec=$BIN_PATH
Icon=$ICON_PATH
Terminal=false
Categories=Utility;Science;
EOF

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" 2>/dev/null || true
fi

echo ""
echo "Done. Find NutriMagnus in your applications menu, or run it directly:"
echo "  $BIN_PATH"
