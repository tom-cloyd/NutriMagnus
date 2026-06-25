@echo off
:: NutriMagnus CLI launcher for Windows
:: Run from anywhere — the script locates itself.
cd /d "%~dp0"
python numa.py %*
