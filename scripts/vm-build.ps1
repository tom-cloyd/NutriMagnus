# vm-build.ps1 — Build nutrimagnus.exe inside the Windows 11 VM.
# Called automatically by build-windows.sh via SSH.
# Safe to run manually inside the VM for debugging.
#
# Expects the project source to be in $BuildDir (default: ~/numa-build).

param(
    [string]$BuildDir = "$env:USERPROFILE\numa-build"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Info($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function OK($msg)   { Write-Host "  OK: $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "  FAIL: $msg" -ForegroundColor Red; exit 1 }

Info "NutriMagnus Windows build"
Info "Build directory: $BuildDir"

if (-not (Test-Path $BuildDir)) {
    Fail "Build directory not found: $BuildDir — run 'make build-windows' from Linux to sync sources."
}

# ── Locate python.exe ─────────────────────────────────────────────────────────
$pythonPathFile = "$env:USERPROFILE\.numa_python_path"
if (Test-Path $pythonPathFile) {
    $pythonExe = (Get-Content $pythonPathFile -Raw).Trim()
} else {
    $pythonExe = (Get-Command python.exe -ErrorAction SilentlyContinue)?.Source
    if (-not $pythonExe) {
        foreach ($c in @(
            "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
            "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
            "C:\Python313\python.exe"
        )) { if (Test-Path $c) { $pythonExe = $c; break } }
    }
}
if (-not $pythonExe -or -not (Test-Path $pythonExe)) {
    Fail "Cannot find python.exe. Run scripts/vm-setup.ps1 first."
}
OK "python.exe: $pythonExe"

# ── Clean previous build artifacts ────────────────────────────────────────────
Info "Cleaning previous artifacts..."
foreach ($d in @("build","dist")) {
    $p = Join-Path $BuildDir $d
    if (Test-Path $p) { Remove-Item $p -Recurse -Force }
}
$spec = Join-Path $BuildDir "nutrimagnus.spec"
if (Test-Path $spec) { Remove-Item $spec -Force }
OK "Clean done"

# ── Run PyInstaller ───────────────────────────────────────────────────────────
Info "Running PyInstaller..."
Push-Location $BuildDir
try {
    & $pythonExe -m PyInstaller --onefile --name nutrimagnus numa.py
    if ($LASTEXITCODE -ne 0) { Fail "PyInstaller failed (exit $LASTEXITCODE)" }
} finally {
    Pop-Location
}

# ── Verify output ─────────────────────────────────────────────────────────────
$exePath = Join-Path $BuildDir "dist\nutrimagnus.exe"
if (-not (Test-Path $exePath)) { Fail "nutrimagnus.exe not found — check PyInstaller output above" }
$sizeMB = [math]::Round((Get-Item $exePath).Length / 1MB, 1)
OK "Built: $exePath ($sizeMB MB)"
Write-Host ""
Write-Host "Build complete." -ForegroundColor Green
