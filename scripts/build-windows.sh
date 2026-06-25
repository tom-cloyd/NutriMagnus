#!/usr/bin/env bash
# build-windows.sh — Orchestrate a Windows .exe build from Linux using KVM/SSH.
#
# What it does (fully automated after first-time vm-setup):
#   1. Starts the Windows 11 VM in headless mode (via virsh)
#   2. Detects the VM's IP address from ARP
#   3. Waits for SSH to become available
#   4. Syncs the project source into the VM over SSH
#   5. Runs scripts/vm-build.ps1 inside the VM via SSH
#   6. Copies dist-windows/nutrimagnus.exe back to Linux
#   7. Shuts the VM down
#
# Prerequisites:
#   - KVM/libvirt installed (already present on this machine)
#   - Windows 11 dev VM imported: https://developer.microsoft.com/windows/downloads/virtual-machines/
#   - First-time VM setup done:  make vm-setup  (run once)
#
# Configuration (override with env vars):
#   NUMA_VM_NAME   VirtualBox VM name (default: NutriMagnus-Build)
#   NUMA_VM_USER   Windows username   (default: User)
#   NUMA_SSH_KEY   SSH private key    (default: ~/.ssh/numa_build_key)
#   NUMA_VM_IP     Skip ARP detection and use a fixed IP

set -euo pipefail

VM_NAME="${NUMA_VM_NAME:-NutriMagnus-Build}"
VM_USER="${NUMA_VM_USER:-User}"
SSH_KEY="${NUMA_SSH_KEY:-$HOME/.ssh/numa_build_key}"
VM_IP="${NUMA_VM_IP:-}"
WIN_BUILD_DIR="$VM_USER/numa-build"   # relative to the Windows user's home
BOOT_TIMEOUT=180                       # seconds to wait for VM IP + SSH
OUT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/dist-windows"

SSH_OPTS="-i $SSH_KEY -o StrictHostKeyChecking=accept-new -o ConnectTimeout=5 -o BatchMode=yes -o LogLevel=ERROR"

info() { echo "==> $*"; }
ok()   { echo "  OK: $*"; }
fail() { echo "  FAIL: $*" >&2; exit 1; }

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ── Sanity checks ─────────────────────────────────────────────────────────────
if ! command -v virsh &>/dev/null; then
    fail "virsh not found. Install KVM: sudo apt-get install -y qemu-kvm libvirt-daemon-system"
fi

if [[ ! -f "$SSH_KEY" ]]; then
    echo ""
    echo "SSH key not found: $SSH_KEY"
    echo "Run 'make vm-setup' first to generate the key and configure the Windows VM."
    exit 1
fi

if ! virsh list --all 2>/dev/null | grep -q "$VM_NAME"; then
    echo ""
    echo "VM '$VM_NAME' not found in libvirt."
    echo ""
    echo "Steps to set it up:"
    echo "  1. Download the Windows 11 dev VM (.ova or .qcow2) from:"
    echo "     https://developer.microsoft.com/windows/downloads/virtual-machines/"
    echo "     (choose KVM/QEMU format if available, or VirtualBox .ova and convert)"
    echo "  2. Import it via virt-manager (File → Import) or:"
    echo "     virt-install --name '$VM_NAME' --memory 8192 --vcpus 4 \\"
    echo "       --disk /path/to/WinDev.qcow2 --import --os-variant win11"
    echo "  3. Run 'make vm-setup' to configure SSH inside the VM."
    echo ""
    echo "Or set NUMA_VM_NAME to match your existing VM:"
    echo "  NUMA_VM_NAME='My Windows VM' make build-windows"
    exit 1
fi

mkdir -p "$OUT_DIR"

# ── Start VM ──────────────────────────────────────────────────────────────────
VM_STATE=$(virsh domstate "$VM_NAME" 2>/dev/null || echo "unknown")
if [[ "$VM_STATE" == "running" ]]; then
    info "VM '$VM_NAME' is already running"
else
    info "Starting VM '$VM_NAME' in headless mode..."
    virsh start "$VM_NAME" >/dev/null
    ok "VM started"
fi

# ── Detect VM IP via ARP ─────────────────────────────────────────────────────
if [[ -z "$VM_IP" ]]; then
    info "Detecting VM IP address (timeout: ${BOOT_TIMEOUT}s)..."
    ELAPSED=0
    while [[ $ELAPSED -lt $BOOT_TIMEOUT ]]; do
        VM_IP=$(virsh domifaddr "$VM_NAME" --source arp 2>/dev/null \
            | awk '/ipv4/ {print $4}' | cut -d/ -f1 | head -1)
        [[ -n "$VM_IP" ]] && break
        sleep 3
        ELAPSED=$((ELAPSED + 3))
        echo "  ... ${ELAPSED}s"
    done
    [[ -n "$VM_IP" ]] || fail "Could not detect VM IP after ${BOOT_TIMEOUT}s. Try setting NUMA_VM_IP manually."
    ok "VM IP: $VM_IP"
fi

# ── Wait for SSH ──────────────────────────────────────────────────────────────
info "Waiting for SSH on $VM_IP ..."
ELAPSED=0
SSH_READY=0
while [[ $ELAPSED -lt $BOOT_TIMEOUT ]]; do
    if ssh $SSH_OPTS "$VM_USER@$VM_IP" "echo ready" 2>/dev/null | grep -q "ready"; then
        SSH_READY=1
        break
    fi
    sleep 5
    ELAPSED=$((ELAPSED + 5))
    echo "  ... ${ELAPSED}s"
done
[[ $SSH_READY -eq 1 ]] || fail "SSH on $VM_IP did not become available. Check VM_USER and that vm-setup.ps1 was run."
ok "SSH ready"

# ── Sync project source into VM ───────────────────────────────────────────────
info "Syncing project source to VM..."
# Pack the project (excluding .venv, dist, .git, tests, __pycache__, *.db)
tar -czf - \
    --exclude='.git' \
    --exclude='.venv' \
    --exclude='dist' \
    --exclude='dist-windows' \
    --exclude='build' \
    --exclude='__pycache__' \
    --exclude='*.db' \
    --exclude='*.spec' \
    --exclude='tests' \
    -C "$PROJECT_DIR" . \
  | ssh $SSH_OPTS "$VM_USER@$VM_IP" \
      "powershell -Command \"
        \$d = \\\"\$env:USERPROFILE\\\\numa-build\\\";
        New-Item -Force -ItemType Directory \\\$d | Out-Null;
        \$input | tar -xzf - -C \\\$d
      \""
ok "Source synced to VM:~/$WIN_BUILD_DIR"

# ── Run the build inside the VM ───────────────────────────────────────────────
info "Running PyInstaller build inside VM..."
ssh $SSH_OPTS "$VM_USER@$VM_IP" \
    "powershell -NonInteractive -ExecutionPolicy Bypass \
     -File \"\$env:USERPROFILE\\numa-build\\scripts\\vm-build.ps1\" \
     -BuildDir \"\$env:USERPROFILE\\numa-build\""

# ── Copy the .exe back to Linux ───────────────────────────────────────────────
EXE_DST="$OUT_DIR/nutrimagnus.exe"
info "Copying nutrimagnus.exe to $EXE_DST ..."
scp $SSH_OPTS "$VM_USER@$VM_IP:/Users/$VM_USER/numa-build/dist/nutrimagnus.exe" "$EXE_DST"
SIZE_MB=$(du -m "$EXE_DST" | cut -f1)
ok "nutrimagnus.exe saved (${SIZE_MB} MB)"

# ── Shut VM down ──────────────────────────────────────────────────────────────
info "Shutting down VM..."
virsh shutdown "$VM_NAME" >/dev/null 2>&1 || virsh destroy "$VM_NAME" >/dev/null 2>&1
ok "VM shut down"

echo ""
echo "Windows build complete: $EXE_DST"
echo "To upload to Codeberg:  make upload-windows"
