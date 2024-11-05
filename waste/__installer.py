# based off https://stackoverflow.com/a/77181745
from pathlib import Path

import PyInstaller.__main__

PKG_DIR = Path(__file__).parent.absolute()

tool_to_args = {
    "nabu": [
        str(PKG_DIR / "nabu.py"),
        "--onefile",
        "--windowed",
        f"--icon={str(PKG_DIR / 'icons/nabu.icns')}",
    ],
}


def install():
    for _, args in tool_to_args.items():
        PyInstaller.__main__.run(args)
