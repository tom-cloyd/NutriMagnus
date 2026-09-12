# vm-setup.ps1 - First-time setup inside the Windows 11 dev VM.
#
# Run this ONCE manually inside the VM. It:
#   1. Downloads your SSH public key from the Linux host (served over HTTP)
#   2. Installs Python 3.13 via winget
#   3. Installs Rich and PyInstaller
#   4. Enables the OpenSSH server so Linux can SSH in for future builds
#   5. Sets PowerShell as the default SSH shell
#
# How to run (inside the VM, open PowerShell and paste this one line):
#
#   powershell -ExecutionPolicy Bypass -Command "iwr 'http://192.168.122.1:8765/scripts/vm-setup.ps1' -OutFile $env:TEMP\vm-setup.ps1; & $env:TEMP\vm-setup.ps1"
#
# The Linux host must be running: make vm-setup  (which starts the HTTP server)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Info($msg) { Write-Host "==> $msg" -ForegroundColor Cyan }
function OK($msg)   { Write-Host "  OK: $msg" -ForegroundColor Green }
function Fail($msg) { Write-Host "  FAIL: $msg" -ForegroundColor Red; exit 1 }

Info "NutriMagnus Windows build environment setup"

# -- 1. Find the Linux host (always 192.168.122.1 on KVM's default NAT) -------
$HostIP = "192.168.122.1"
$KeyURL = "http://${HostIP}:8765/numa_build_key.txt"
Info "Fetching SSH public key from $KeyURL ..."
try {
    $PubKey = (Invoke-WebRequest -Uri $KeyURL -UseBasicParsing).Content.Trim()
    OK "Public key fetched"
} catch {
    Fail "Could not fetch SSH key from $KeyURL - is 'make vm-setup' still running on the Linux host?"
}

# -- 2. Install Python 3.13 via winget ----------------------------------------
Info "Installing Python 3.13..."
$pyCheck = Get-Command python.exe -ErrorAction SilentlyContinue
$pythonWorks = $false
if ($pyCheck -and $pyCheck.Source -notlike "*WindowsApps*") {
    try {
        $ver = & python.exe --version 2>&1
        if ($LASTEXITCODE -eq 0) { $pythonWorks = $true }
    } catch {}
}
if ($pythonWorks) {
    OK "Python already installed: $ver"
} else {
    winget install --id Python.Python.3.13 --source winget --silent --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { Fail "winget install Python failed" }
    OK "Python 3.13 installed"
}

# Refresh PATH so python.exe is visible in this session
$MachinePath = [System.Environment]::GetEnvironmentVariable("PATH","Machine")
$UserPath = [System.Environment]::GetEnvironmentVariable("PATH","User")
$env:PATH = $MachinePath + ";" + $UserPath

$pythonCmd = Get-Command python.exe -ErrorAction SilentlyContinue
$pythonExe = if ($pythonCmd) { $pythonCmd.Source } else { $null }
if (-not $pythonExe) {
    $candidates = @("$env:LOCALAPPDATA\Programs\Python\Python313\python.exe", "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe", "C:\Python313\python.exe")
    foreach ($c in $candidates) { if (Test-Path $c) { $pythonExe = $c; break } }
}
if (-not $pythonExe) { Fail "Cannot locate python.exe. Reopen PowerShell and re-run." }
OK "python.exe: $pythonExe"

# -- 3. Install pip dependencies -----------------------------------------------
Info "Installing rich and pyinstaller..."
& $pythonExe -m pip install --upgrade pip --quiet
& $pythonExe -m pip install rich pyinstaller --quiet
if ($LASTEXITCODE -ne 0) { Fail "pip install failed" }
OK "rich and pyinstaller installed"

# -- 4. Save python path so vm-build.ps1 can find it without PATH lookup -------
$PythonPathFile = "$env:USERPROFILE\.numa_python_path"
$pythonExe | Set-Content $PythonPathFile -Encoding UTF8
OK "Python path saved to $PythonPathFile"

# -- 5. Install OpenSSH server (standalone release; avoids DISM/Windows Update,
#       which requires reaching Microsoft servers that may be unreachable due
#       to WSUS group policy or network restrictions) ---------------------------
Info "Installing OpenSSH server..."
$sshdCheck = Get-Service sshd -ErrorAction SilentlyContinue
if ($sshdCheck) {
    OK "OpenSSH server already installed"
} else {
    $OpenSSHMsi = "$env:TEMP\OpenSSH-Win64.msi"
    Invoke-WebRequest -Uri "https://github.com/PowerShell/Win32-OpenSSH/releases/download/10.0.0.0p2-Preview/OpenSSH-Win64-v10.0.0.0.msi" -OutFile $OpenSSHMsi -UseBasicParsing
    Start-Process msiexec.exe -ArgumentList "/i `"$OpenSSHMsi`" /quiet /norestart" -Wait
    OK "OpenSSH server installed"
}
Start-Service sshd -ErrorAction SilentlyContinue
Set-Service -Name sshd -StartupType Automatic
OK "sshd started and set to auto-start"

# Allow SSH through Windows Firewall
New-NetFirewallRule -Name "OpenSSH-In-TCP" -DisplayName "OpenSSH Server" -Enabled True -Direction Inbound -Protocol TCP -Action Allow -LocalPort 22 -ErrorAction SilentlyContinue | Out-Null
OK "Firewall rule for port 22 added"

# -- 6. Set PowerShell as the default SSH shell --------------------------------
$psExe = "C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
if (Test-Path "HKLM:\SOFTWARE\OpenSSH") {
    New-ItemProperty -Path "HKLM:\SOFTWARE\OpenSSH" -Name DefaultShell -Value $psExe -PropertyType String -Force | Out-Null
    OK "Default SSH shell set to PowerShell"
}

# -- 7. Install SSH public key -------------------------------------------------
# Written with ASCIIEncoding (never UTF8 -- Set-Content -Encoding UTF8 on
# Windows PowerShell 5.1 prepends a BOM, which corrupts authorized_keys and
# silently breaks key auth). Also written to administrators_authorized_keys:
# sshd's default sshd_config redirects AuthorizedKeysFile for any account in
# the local Administrators group (the default first user account) to that
# single shared ProgramData file instead of the per-user .ssh/authorized_keys,
# so the per-user copy alone is silently ignored for an admin account.
Info "Installing SSH public key..."
$sshDir = "$env:USERPROFILE\.ssh"
New-Item -Force -ItemType Directory $sshDir | Out-Null
$KeyLine = $PubKey + "`n"
$AsciiEnc = New-Object System.Text.ASCIIEncoding
[System.IO.File]::WriteAllText("$sshDir\authorized_keys", $KeyLine, $AsciiEnc)
icacls "$sshDir\authorized_keys" /inheritance:r /grant "${env:USERNAME}:F" | Out-Null

$AdminKeysFile = "$env:ProgramData\ssh\administrators_authorized_keys"
[System.IO.File]::WriteAllText($AdminKeysFile, $KeyLine, $AsciiEnc)
icacls $AdminKeysFile /inheritance:r | Out-Null
icacls $AdminKeysFile /grant SYSTEM:F /grant Administrators:F | Out-Null
OK "SSH public key installed to $sshDir\authorized_keys and $AdminKeysFile"

# -- Done ----------------------------------------------------------------------
Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "The Linux host can now SSH in as: $env:USERNAME@<this VM's IP>" -ForegroundColor Green
Write-Host "You can now close virt-manager and run: make build-windows" -ForegroundColor Green
