# NutriMagnus CLI launcher for Windows PowerShell
# Run from anywhere — the script locates itself.
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir
python numa.py @args
