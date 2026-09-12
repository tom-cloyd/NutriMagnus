# vm-build.ps1 - Build nutrimagnus.exe inside the Windows 11 VM.
# Called automatically by build-windows.sh via SSH.
# Safe to run manually inside the VM for debugging.
#
# Expects the project source to be in $BuildDir (default: ~/numa-build).
# Mirrors the Linux build target in the Makefile: regenerate user-manual.html,
# then run PyInstaller against the maintained nutrimagnus.spec (not a bare
# --onefile build off a plain entry script) so the same bundled data
# (templates, static, manual, oxalate.db) ends up in the Windows build too.

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
    Fail "Build directory not found: $BuildDir - run 'make build-windows' from Linux to sync sources."
}

# -- Locate python.exe --------------------------------------------------------
$pythonPathFile = "$env:USERPROFILE\.numa_python_path"
if (Test-Path $pythonPathFile) {
    $pythonExe = (Get-Content $pythonPathFile -Raw).Trim()
} else {
    $pythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
    $pythonExe = if ($pythonCmd) { $pythonCmd.Source } else { $null }
    if (-not $pythonExe) {
        $candidates = @("$env:LOCALAPPDATA\Programs\Python\Python313\python.exe", "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe", "C:\Python313\python.exe")
        foreach ($c in $candidates) { if (Test-Path $c) { $pythonExe = $c; break } }
    }
}
if (-not $pythonExe -or -not (Test-Path $pythonExe)) {
    Fail "Cannot find python.exe. Run scripts/vm-setup.ps1 first."
}
OK "python.exe: $pythonExe"

# -- Install project dependencies (vm-setup.ps1 only installs rich/pyinstaller
#    for its own one-time OS-level setup; the actual app deps -- fastapi,
#    uvicorn, Jinja2, Markdown, etc. -- live in requirements.txt, which only
#    exists once the source sync below has landed, so it's installed here) ---
$reqFile = Join-Path $BuildDir "requirements.txt"
if (-not (Test-Path $reqFile)) {
    Fail "requirements.txt not found in $BuildDir"
}
Info "Installing project dependencies from requirements.txt..."
& $pythonExe -m pip install -r $reqFile --quiet
if ($LASTEXITCODE -ne 0) { Fail "pip install -r requirements.txt failed (exit $LASTEXITCODE)" }
OK "Dependencies installed"

# -- Clean previous build artifacts -------------------------------------------
Info "Cleaning previous artifacts..."
foreach ($d in @("build","dist")) {
    $p = Join-Path $BuildDir $d
    if (Test-Path $p) { Remove-Item $p -Recurse -Force }
}
OK "Clean done"

# -- Regenerate user-manual.html (mirrors the Linux `make build` target) -----
Info "Regenerating user-manual.html..."
Push-Location $BuildDir
try {
    & $pythonExe scripts\build_manual.py
    if ($LASTEXITCODE -ne 0) { Fail "build_manual.py failed (exit $LASTEXITCODE)" }
} finally {
    Pop-Location
}
OK "Manual regenerated"

# -- Run PyInstaller against the maintained spec ------------------------------
$specPath = Join-Path $BuildDir "nutrimagnus.spec"
if (-not (Test-Path $specPath)) {
    Fail "nutrimagnus.spec not found in $BuildDir - check build-windows.sh's tar excludes."
}
Info "Running PyInstaller..."
Push-Location $BuildDir
try {
    & $pythonExe -m PyInstaller $specPath
    if ($LASTEXITCODE -ne 0) { Fail "PyInstaller failed (exit $LASTEXITCODE)" }
} finally {
    Pop-Location
}

# -- Verify output -------------------------------------------------------------
$exePath = Join-Path $BuildDir "dist\nutrimagnus.exe"
if (-not (Test-Path $exePath)) { Fail "nutrimagnus.exe not found - check PyInstaller output above" }
$sizeMB = [math]::Round((Get-Item $exePath).Length / 1MB, 1)
OK "Built: $exePath ($sizeMB MB)"
Write-Host ""
Write-Host "Build complete." -ForegroundColor Green
