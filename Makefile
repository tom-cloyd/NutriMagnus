.PHONY: devserver build push push-release release-linux vm-setup build-windows upload-windows release-windows clean

# ── Linux build ───────────────────────────────────────────────────────────────
# Packages web/launcher.py (starts uvicorn, opens a browser tab) into a single
# executable via nutrimagnus.spec — a hand-maintained spec (not auto-generated;
# see its own comments), since it bundles web/templates, web/static, the
# manual source/output, and oxalate.db as data alongside the app.
devserver: build
	./dist/nutrimagnus

build:
	.venv/bin/python3 scripts/build_manual.py
	.venv/bin/pyinstaller nutrimagnus.spec

# ── Push: source only, no release ─────────────────────────────────────────────
# The safe default. .forgejo/workflows/release.yml is manual-trigger only, so
# this can never publish a release or binary no matter what version.py says —
# it's just `git push`, made explicit so "push" and "publish a release" are
# never the same reflex.
push:
	git push origin main

# ── Linux: create a Codeberg release and upload the binary ───────────────────
# Manual/local use (e.g. testing a release without waiting on CI, or firing
# one on purpose — see push-release below). Requires CODEBERG_TOKEN in the
# environment.
release-linux: build
	python3 scripts/create_release.py

# ── Push + publish: push source, then build and publish a public release ─────
# Deliberate, explicit step — only run this when you actually want a
# downloadable release live on Codeberg.
push-release: push release-linux

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
# Note: nutrimagnus.spec is NOT removed here — it's hand-maintained and committed.
clean:
	rm -rf build/ dist/ dist-windows/
