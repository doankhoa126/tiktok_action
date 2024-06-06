# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('C:\\Dkhoa\\TiktokTool\\data_tiktok_tool\\hotmail.json', 'data_tiktok_tool'),
        ('C:\\Dkhoa\\TiktokTool\\data_tiktok_tool\\proxy.txt', 'data_tiktok_tool'),
        ('C:\\Dkhoa\\TiktokTool\\data_tiktok_tool\\user_agents.txt', 'data_tiktok_tool'),
        ('C:\\Dkhoa\\TiktokTool\\data_tiktok_tool\\id_profile.txt', 'data_tiktok_tool'),
        ('C:\\Dkhoa\\TiktokTool\\data_tiktok_tool\\acc_tiktok.json', 'data_tiktok_tool'),
        ('C:\\Dkhoa\\TiktokTool\\data_tiktok_tool\\config_acc_tiktok.json', 'data_tiktok_tool'),
        ('C:\\Dkhoa\\TiktokTool\\data_json_scripts\\xpath_reg_acc.json', 'data_json_scripts'),
        ('C:\\Dkhoa\\TiktokTool\\data_json_scripts\\xpath_login.json', 'data_json_scripts'),
        ('C:\\Dkhoa\\TiktokTool\\data_json_scripts\\xpath_newfeed.json', 'data_json_scripts')
    ],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
