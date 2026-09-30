# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

a = Analysis(
    ["app/main_gui.py"],
    pathex=[str(BASE_DIR / "app")],
    binaries=[],
    datas=[
        ("config", "config"),
        ("data", "data"),
        ("history", "history"),
    ],
    hiddenimports=[
        "interface",
        "modulos",
        "nucleo",
        "inteligencia",
        "web",
        "rede",
        "scanner",
        "seguranca",
        "oraculo",
        "interpretador",
        "modos",
        "configuracao",
        "diagnostico",
        "painel_central",
        "painel_sistema",
        "visual",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="OLHO_DE_DEUS",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)

