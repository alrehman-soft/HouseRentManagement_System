# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('tenant_images', 'tenant_images')],
    hiddenimports=['cv2', 'PIL', 'PIL._tkinter_finder', 'pandas', 'openpyxl', 'reportlab', 'matplotlib', 'dateutil', 'dateutil.relativedelta', 'tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.filedialog', 'uuid', 're', 'os', 'sys', 'datetime', 'threading', 'string', 'random'],
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
    name='HouseRentManagement',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['Logo.ico'],
)
