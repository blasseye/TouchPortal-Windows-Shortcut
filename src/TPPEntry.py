__version__ = 1
PLUGIN_ID = "TP.Plugins.win_shortcut"

TPSDK_DEFAULT_VERSION = 6

TP_PLUGIN_INFO = {
    "sdk": 6,
    "version": __version__,
    "name": "TouchPortal Windows Shortcut",
    "id": PLUGIN_ID,
    "plugin_start_cmd": "%TP_PLUGIN_FOLDER%TPWinShortcut\\TPWinShortcut.exe",
    "configuration": {
        "colorDark": "#0d162c",
        "colorLight": "#4b84f3",
    },
}

TP_PLUGIN_SETTINGS = {
    "Is Running": {
        "name": "Is Running",
        "type": "text",
        "default": "False",
        "readOnly": True,
    },
    "Shortcut directory": {
        "name": "Shortcut directory",
        "type": "text",
        "readOnly": False,
    },
    "Icon directory": {
        "name": "Icon directory",
        "type": "text",
        "readOnly": False,
    },
    "Refresh shortcut": {
        "name": "Refresh shortcut",
        "type": "number",
        "default": "30",
        "readOnly": False,
    },
}

TP_PLUGIN_CATEGORIES = {
    "main": {
        "id": PLUGIN_ID + ".main",
        "name": "Windows Shortcut",
        "imagepath": "%TP_PLUGIN_FOLDER%TPWinShortcut\\icon.png",
    },
    "icon": {"id": PLUGIN_ID + ".icon", "name": "Path of the shortcut icon"},
    "path": {"id": PLUGIN_ID + ".path", "name": "Path of the shortcut"},
}

TP_PLUGIN_STATES = {}

for i in range(20):
    icon_key = f"shortcut_icon_{i}"
    path_key = f"shortcut_path_{i}"
    TP_PLUGIN_STATES[icon_key] = {
        "category": "icon",
        "id": f"{PLUGIN_ID}.states.{icon_key}",
        "type": "text",
        "desc": f"Path of the shortcut icon {i}",
    }
    TP_PLUGIN_STATES[path_key] = {
        "category": "path",
        "id": f"{PLUGIN_ID}.states.{path_key}",
        "type": "text",
        "desc": f"Path of the shortcut {i}",
    }
