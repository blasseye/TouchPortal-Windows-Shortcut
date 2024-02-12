from argparse import ArgumentParser
import os
import TouchPortalAPI as TP
from TouchPortalAPI.logger import Logger
from TPPEntry import TP_PLUGIN_INFO, TP_PLUGIN_SETTINGS
import sys
import configparser
import shutil
import win32api
import win32ui
import win32gui
import win32com.client
import win32con
from threading import Thread
from time import sleep
import pythoncom


# Setup callbacks and connection
TPClient = TP.Client(TP_PLUGIN_INFO["id"])
g_log = Logger(TP_PLUGIN_INFO["id"])


def get_extension(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension


def get_target_path(file_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(file_path)
    target_path = shortcut.TargetPath
    return target_path


def get_url_icon(file_path, output_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    if "InternetShortcut" in config:
        icon_file = config["InternetShortcut"].get("IconFile")
        extension = get_extension(icon_file)
        if extension == ".ico":
            shutil.copy(icon_file, output_path)
        elif extension == ".exe":
            get_exe_icon(icon_file, output_path)
    return


def get_lnk_icon(file_path, output_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(file_path)
    icon_location = shortcut.IconLocation.split(",")
    icon_file = icon_location[0].strip('"')
    extension = get_extension(icon_file)
    if extension == ".ico":
        shutil.copy(icon_file, output_path)
    else:
        target = get_target_path(file_path)
        extension = get_extension(target)
        if extension == ".exe":
            get_exe_icon(target, output_path)
    return


def get_exe_icon(file_path, output_path):
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
    large, small = win32gui.ExtractIconEx(file_path, 0)
    win32gui.DestroyIcon(small[0])
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap(hdc, ico_x, ico_y)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject(hbmp)
    hdc.DrawIcon((0, 0), large[0])
    hbmp.SaveBitmapFile(hdc, output_path)


def get_icon(file, nb):
    output_ico = f"{directory_icon}shortcut_icon_{nb}.ico"
    file_path = file
    extension = get_extension(file_path)
    if extension == ".url":
        get_url_icon(file_path, output_ico)
    elif extension == ".lnk":
        get_lnk_icon(file_path, output_ico)
    elif extension == ".exe":
        get_exe_icon(file_path, output_ico)


def reset_icon(nb):
    tp_plugin_folder = os.path.dirname(os.path.abspath(sys.argv[0]))
    output_ico = f"{directory_icon}shortcut_icon_{nb}.ico"
    icon_file = f"{tp_plugin_folder}\shortcut_icon_default.ico"
    shutil.copy(icon_file, output_ico)


def update_shortcuts_list(directory):
    # Check if directory exists
    if not os.path.exists(directory):
        g_log.debug(f"The directory '{directory}' does not exist.")
        return []

    # Check if the path points to a directory
    if not os.path.isdir(directory):
        g_log.debug(f"'{directory}' is not a valid directory.")
        return []

    # List files in the directory
    files = os.listdir(directory)

    # Return the list of files
    return files


def state_update():
    pythoncom.CoInitialize()
    try:
        while TPClient.isConnected():
            time = 0
            if time == 0:
                list_file = update_shortcuts_list(directory_shortcuts)
                nb_shortcut = len(list_file)
                if nb_shortcut >= 20:
                    nb_shortcut = 20
                    for i in range(nb_shortcut):
                        TPClient.stateUpdate(
                            TP_PLUGIN_INFO["id"] + f".states.shortcut_path_{i}",
                            directory_shortcuts + list_file[i],
                        )
                        get_icon(
                            directory_shortcuts + list_file[i],
                            i,
                        )
                else:
                    for i in range(nb_shortcut):
                        TPClient.stateUpdate(
                            TP_PLUGIN_INFO["id"] + f".states.shortcut_path_{i}",
                            directory_shortcuts + list_file[i],
                        )
                        get_icon(
                            directory_shortcuts + list_file[i],
                            i,
                        )
                    for i in range(nb_shortcut, 20):
                        TPClient.stateUpdate(
                            TP_PLUGIN_INFO["id"] + f".states.shortcut_path_{i}",
                            "",
                        )
                        reset_icon(i)
                time = +1
                sleep(1)
                if time == timer:
                    time = 0
    except Exception:
        from traceback import format_exc

        g_log.info(f"ERRO : {format_exc()}")
    pythoncom.CoUninitialize()


def handle_settings(settings, on_connect=False):
    global directory_shortcuts
    global directory_icon

    global timer

    settings = {
        list(settings[i])[0]: list(settings[i].values())[0]
        for i in range(len(settings))
    }

    if (
        value := settings.get(TP_PLUGIN_SETTINGS["Shortcut directory"]["name"])
    ) is not None:
        TP_PLUGIN_SETTINGS["Shortcut directory"]["value"] = value
        directory_shortcuts = value
    else:
        TPClient.showNotification(
            notificationId="blasseye.TP.Plugins.Update_Check",
            title="TouchPortal-Windows-Shortcut : Folder path not configured",
            msg="Go to setting, Setting...>Plug-ins>Windows-Shortcut, and set the parameter.",
            options=[{"id": "test", "title": "Go to parametre"}],
        )

    if (
        value := settings.get(TP_PLUGIN_SETTINGS["Icon directory"]["name"])
    ) is not None:
        TP_PLUGIN_SETTINGS["Icon directory"]["value"] = value
        directory_icon = value

    if (
        value := settings.get(TP_PLUGIN_SETTINGS["Refresh shortcut"]["name"])
    ) is not None:
        TP_PLUGIN_SETTINGS["Refresh shortcut"]["value"] = value
        timer = int(value)


def check_update(data):
    """Checking if Plugin needs updated"""
    github_check = TP.Tools.updateCheck(
        "blasseye", "TouchPortal-Windows-Shortcut"
    )
    plugin_version = str(data["pluginVersion"])
    plugin_version = plugin_version[:1] + "." + plugin_version[1:]
    if github_check[1:4] != plugin_version[0:3]:
        TPClient.showNotification(
            notificationId="blasseye.TP.Plugins.Update_Check",
            title="TouchPortal-Windows-Shortcut: The shortcut folder path is invalid",
            msg="A new TouchPortal-Windows-Shortcut Version is available and ready to Download. This may include Bug Fixes and or New Features.",
            options=[
                {"id": "Download Update", "title": "Click here to Update"}
            ],
        )


@TPClient.on(TP.TYPES.onConnect)
def onConnect(data):
    g_log.info(
        f"""Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}."""
    )
    g_log.debug(f"Connection: {data}")
    TPClient.settingUpdate("Is Running", "True")

    if settings := data.get("settings"):
        handle_settings(settings, True)

    Thread(target=state_update).start()


@TPClient.on(TP.TYPES.onSettingUpdate)
def onSettingUpdate(data):
    g_log.debug(f"Settings: {data}")
    if settings := data.get("settings"):
        handle_settings(settings, False)


@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    g_log.debug(f"Connection: {data}")
    try:
        TPClient.settingUpdate("Is Running", "False")
    except ConnectionResetError:
        pass
    g_log.info("Received shutdown event from TP Client.")


@TPClient.on(TP.TYPES.onError)
def onError(exc):
    g_log.error(f"Error in TP Client event handler: {repr(exc)}")


def main():
    global TPClient, g_log

    # Handle CLI arguments
    parser = ArgumentParser()
    parser.add_argument("-d", action="store_true", help="Use debug logging.")
    parser.add_argument(
        "-w", action="store_true", help="Only log warnings and errors."
    )
    parser.add_argument(
        "-q", action="store_true", help="Disable all logging (quiet)."
    )
    parser.add_argument(
        "-l", metavar="<logfile>", help="Log to this file (default is stdout)."
    )
    parser.add_argument(
        "-s",
        action="store_true",
        help="If logging to file, also output to stdout.",
    )

    # His processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # Trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else "none"
    opts.s = opts.s.strip().lower() if opts.s else "stdout"
    print(opts)

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q:
        logLevel = None
    elif opts.d:
        logLevel = "DEBUG"
    elif opts.w:
        logLevel = "WARNING"

    # Set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # Set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr":
            logStream = sys.stderr
        elif opts.s == "stdout":
            logStream = sys.stdout
        else:
            logStream = None

    # Configure the Client logging based on command line arguments.
    # Since the Client uses the "root" logger by default,
    # this also sets all default logging options for any added child loggers,
    # such as our g_log instance we created earlier.
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(
        f"Starting {TP_PLUGIN_INFO['name']} v{TP_PLUGIN_INFO['version']} on {sys.platform}."
    )
    ret = 1
    try:
        TPClient.connect()
        g_log.info("TP Client closed.")
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc

        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient

    g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret


if __name__ == "__main__":
    main()
