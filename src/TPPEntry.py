from TouchPortalAPI.tppbuild import *

__version__ = 1
PLUGIN_ID = "TP.Plugins.win_shortcut"

TPSDK_DEFAULT_VERSION = 6

TP_PLUGIN_INFO = {
    'sdk': 6,
    'version': __version__,
    'name': "Windows-Shortcut",
    "id": PLUGIN_ID,
    'plugin_start_cmd_windows': "%TP_PLUGIN_FOLDER%winShortcut\\winShortcut.exe",
    'configuration': {
        'colorDark': '#0d162c',
        'colorLight': '#4b84f3',
    },
    "doc": {
        "repository": "KillerBOSS2019:TP-Speed-Test-Plugin",
        "Install": "1. Download latest version of plugin for your system.\n2. Import downloaded tpp by click the gear button next to email/notification icon.\n3. If this is first plugin, you will need to restart TouchPortal for it to work.",
        "description": "SpeedTest Plugin using https://www.speedtest.net/ API for [TouchPortal](https://www.touch-portal.com/)"
    }
}

TP_PLUGIN_SETTINGS = {
    "Shortcut directory": {
        "name":"Shortcut directory",
        "type":"text",
        "isPassword":False,
        "readOnly": False
    }
}

TP_PLUGIN_CATEGORIES = {
    "main": {
        "id": PLUGIN_ID + ".main",
        "name": "Touch Portal Windows Shortcut",
        "imagepath": "%TP_PLUGIN_FOLDER%winShortcut\\icon.png",
    },
    "icon": {
        "id": PLUGIN_ID + ".icon",
        "name": "Path of the shortcut icon"
    },
    "path": {
        "id": PLUGIN_ID + ".path",
        "name": "Path of the shortcut"
    }
}

TP_PLUGIN_ACTIONS = {

}

TP_PLUGIN_STATES = {
    #icon
    "shortcut_icon_0": {
        "category": "icon",
        "id": PLUGIN_ID + ".states.shortcut_icon_0",
        "type": "text",
        "desc": "Path of the shortcut icon 0",
        "default": "%TP_PLUGIN_FOLDER%winShortcut\shortcut_icon_0.ico"
    },
    "shortcut_icon_1": {
        "category": "icon",
        "id": PLUGIN_ID + ".states.shortcut_icon_1",
        "type": "text",
        "desc": "Path of the shortcut icon 1",
        "default": "%TP_PLUGIN_FOLDER%winShortcut\shortcut_icon_1.ico"
    },
    "shortcut_icon_2": {
        "category": "icon",
        "id": PLUGIN_ID + ".states.shortcut_icon_2",
        "type": "text",
        "desc": "Path of the shortcut icon 2",
        "default": "%TP_PLUGIN_FOLDER%winShortcut\shortcut_icon_2.ico"
    },
    "shortcut_icon_3": {
        "category": "icon",
        "id": PLUGIN_ID + ".states.shortcut_icon_3",
        "type": "text",
        "desc": "Path of the shortcut icon 3",
        "default": "%TP_PLUGIN_FOLDER%winShortcut\shortcut_icon_3.ico"
    },
    "shortcut_icon_4": {
        "category": "icon",
        "id": PLUGIN_ID + ".states.shortcut_icon_4",
        "type": "text",
        "desc": "Path of the shortcut icon 4",
        "default": "%TP_PLUGIN_FOLDER%winShortcut\shortcut_icon_4.ico"
    },
    "shortcut_icon_5": {
        "category": "icon",
        "id": PLUGIN_ID + ".states.shortcut_icon_5",
        "type": "text",
        "desc": "Path of the shortcut icon 5",
        "default": "%TP_PLUGIN_FOLDER%winShortcut\shortcut_icon_5.ico"
    },

    #path
    "shortcut_path_0": {
        "category": "path",
        "id": PLUGIN_ID + ".states.shortcut_path_0",
        "type": "text",
        "desc": "Path of the shortcut 0",
        "default": ""
    },
    "shortcut_path_1": {
        "category": "path",
        "id": PLUGIN_ID + ".states.shortcut_path_1",
        "type": "text",
        "desc": "Path of the shortcut 1",
        "default": ""
    },
    "shortcut_path_2": {
        "category": "path",
        "id": PLUGIN_ID + ".states.shortcut_path_2",
        "type": "text",
        "desc": "Path of the shortcut 2",
        "default": ""
    },
    "shortcut_path_3": {
        "category": "path",
        "id": PLUGIN_ID + ".states.shortcut_path_3",
        "type": "text",
        "desc": "Path of the shortcut 3",
        "default": ""
    },
    "shortcut_path_4": {
        "category": "path",
        "id": PLUGIN_ID + ".states.shortcut_path_4",
        "type": "text",
        "desc": "Path of the shortcut 4",
        "default": ""
    },
    "shortcut_path_5": {
        "category": "path",
        "id": PLUGIN_ID + ".states.shortcut_path_5",
        "type": "text",
        "desc": "Path of the shortcut 5",
        "default": ""
    }
}

TP_PLUGIN_EVENTS = {
    "shortcut_icon":{
        "id": PLUGIN_ID + ".events.shortcut_icon",
        "name": "Keep Buttons Icon same as Shortcut",
        "format": "Keep Buttons Icon same as $val",
        "type": "communicate",
        "valueType": "choice",
        "valueChoices": [
            PLUGIN_ID + ".states.shortcut_icon_0",
            PLUGIN_ID + ".states.shortcut_icon_1",
            PLUGIN_ID + ".states.shortcut_icon_2",
            PLUGIN_ID + ".states.shortcut_icon_3",
            PLUGIN_ID + ".states.shortcut_icon_4",
            PLUGIN_ID + ".states.shortcut_icon_5",
        ],
        "valueStateId": "icon",
        "category": "main"
        }
}