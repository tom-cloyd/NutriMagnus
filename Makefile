.PHONY: devserver build release-linux vm-setup build-windows upload-windows release-windows clean

# ── Linux build ───────────────────────────────────────────────────────────────
devserver: build
	./dist/nutrimagnus

build:
	.venv/bin/pyinstaller --onefile --name nutrimagnus numa.py

# ── Linux: create a Codeberg release and upload the binary ───────────────────
# Normally done automatically by .forgejo/workflows/release.yml on every push
# to main; this is the same script, for manual/local use (e.g. testing a
# release without waiting on CI). Requires CODEBERG_TOKEN in the environment.
release-linux: build
	python3 scripts/create_release.py

# ── Windows: first-time VM setup (run once after importing the dev VM) ────────
# Starts an HTTP server so the Windows VM can download the SSH key and setup script,
# then opens virt-manager so you can log into the VM and paste a single command.
#
# Inside the VM, open PowerShell and run:
#   powershell -ExecutionPolicy Bypass -Command "iwr 'http://192.168.122.1:8765/scripts/vm-setup.ps1' -OutFile $env:TEMP\vm-setup.ps1; & $env:TEMP\vm-setup.ps1"
vm-setup:
	@test -f ~/.ssh/numa_build_key || \
	    ssh-keygen -t ed25519 -f ~/.ssh/numa_build_key -N "" -C "numa-build@$$(hostname)"
	@echo ""
	@echo "==> SSH public key (~/.ssh/numa_build_key.pub):"
	@cat ~/.ssh/numa_build_key.pub
	@echo ""
	@echo "==> Starting VM '${NUMA_VM_NAME:-NutriMagnus-Build}'..."
	@virsh start "$${NUMA_VM_NAME:-NutriMagnus-Build}" 2>/dev/null || true
	@echo ""
	@echo "==> Opening virt-manager so you can log into the VM..."
	@virt-manager --connect qemu:///system \
	    --show-domain-console "$${NUMA_VM_NAME:-NutriMagnus-Build}" &
	@echo ""
	@echo "==> Serving setup files at http://192.168.122.1:8765/"
	@echo "    (keep this running; Ctrl+C when setup is complete)"
	@echo ""
	@echo "    Inside the VM, open PowerShell and paste this one line:"
	@echo ""
	@echo '    powershell -ExecutionPolicy Bypass -Command "iwr '"'"'http://192.168.122.1:8765/scripts/vm-setup.ps1'"'"' -OutFile $$env:TEMP\vm-setup.ps1; & $$env:TEMP\vm-setup.ps1"'
	@echo ""
	python3 -m http.server 8765 --directory .

# ── Windows: automated build (headless VM, SSH, PyInstaller) ─────────────────
# Requires vm-setup to have been run once.
# Override VM name: NUMA_VM_NAME="My VM" make build-windows
build-windows:
	./scripts/build-windows.sh

# ── Windows: upload dist-windows/nutrimagnus.exe to latest Codeberg release ──
upload-windows:
	@test -f dist-windows/nutrimagnus.exe || \
	    (echo "ERROR: dist-windows/nutrimagnus.exe not found. Run 'make build-windows' first." && exit 1)
	@test -n "$$CODEBERG_TOKEN" || \
	    (echo "ERROR: CODEBERG_TOKEN is not set." && exit 1)
	$(eval RELEASE_ID := $(shell curl -s \
	    -H "Authorization: token $$CODEBERG_TOKEN" \
	    "https://codeberg.org/api/v1/repos/Tom_Cloyd/NutriMagnus/releases?limit=1" \
	    | python3 -c "import json,sys; print(json.load(sys.stdin)[0]['id'])"))
	@echo "==> Uploading nutrimagnus.exe to Codeberg release $(RELEASE_ID)..."
	curl -s -X POST \
	    -H "Authorization: token $$CODEBERG_TOKEN" \
	    "https://codeberg.org/api/v1/repos/Tom_Cloyd/NutriMagnus/releases/$(RELEASE_ID)/assets" \
	    -F "attachment=@dist-windows/nutrimagnus.exe"
	@echo ""
	@echo "Done. https://codeberg.org/Tom_Cloyd/NutriMagnus/releases"

# ── Windows: full release (build + upload) ───────────────────────────────────
release-windows: build-windows upload-windows

# ── Clean ─────────────────────────────────────────────────────────────────────
clean:
	rm -rf build/ dist/ dist-windows/ nutrimagnus.spec
