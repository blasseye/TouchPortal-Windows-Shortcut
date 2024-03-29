from TouchPortalAPI.tppbuild import validateBuild, runBuild
from TPPEntry import __version__

PLUGIN_MAIN = "TPWinShortcut.py"

PLUGIN_EXE_NAME = "TPWinShortcut"

PLUGIN_EXE_ICON = "icon.png"

PLUGIN_ENTRY = "TPPEntry.py"

PLUGIN_ENTRY_INDENT = 2

PLUGIN_ROOT = "TPWinShortcut"

PLUGIN_ICON = "icon.png"

OUTPUT_PATH = "./"

PLUGIN_VERSION = __version__

ADDITIONAL_FILES = ["shortcut_icon_default.ico"]

ADDITIONAL_PYINSTALLER_ARGS = ["--log-level=WARN"]

if __name__ == "__main__":
    validateBuild()
    runBuild()
