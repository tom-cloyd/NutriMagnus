# -*- mode: python ; coding: utf-8 -*-
# Builds a single-file executable that launches the NutriMagnus web app and
# opens a browser tab — see web/launcher.py. Replaces the old CLI-based spec
# (which pointed at the now-removed numa.py) as of the CLI's removal.

a = Analysis(
    ['web/launcher.py'],
    pathex=['.', 'web'],
    binaries=[],
    datas=[
        # backend.py is bundled as a top-level module (via hiddenimports below),
        # so its own Path(__file__).parent-relative lookups expect templates/
        # and static/ as its *siblings* at the bundle root, not under web/.
        ('web/templates', 'templates'),
        ('web/static', 'static'),
        ('home.md', '.'),
        ('user-manual.md', '.'),
        ('user-manual.html', '.'),
        ('scripts/build_manual.py', 'scripts'),
        ('oxalate.db', '.'),
    ],
    hiddenimports=['backend'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='nutrimagnus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
