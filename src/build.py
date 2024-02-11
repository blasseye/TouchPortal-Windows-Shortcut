from TouchPortalAPI.tppbuild import *
from TPPEntry import __version__

PLUGIN_MAIN = "winShortcut.py"

PLUGIN_EXE_NAME = "TPWinShortcut"

PLUGIN_EXE_ICON = "icon.png"

PLUGIN_ENTRY = "TPPEntry.py"

PLUGIN_ENTRY_INDENT = -1

PLUGIN_ROOT = "TPWinShortcut"

PLUGIN_ICON = "icon.png"

OUTPUT_PATH = "./"

PLUGIN_VERSION = str(__version__)

ADDITIONAL_FILES = []

ADDITIONAL_PYINSTALLER_ARGS = [
    "--log-level=WARN"
]

if __name__ == "__main__":
    runBuild()