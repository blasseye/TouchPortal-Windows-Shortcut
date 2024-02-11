from argparse import ArgumentParser
import os
import TouchPortalAPI as TP
from TouchPortalAPI.logger import Logger
from TPPEntry import *
import sys
from utils import getIcon

directory_icons = "%TP_PLUGIN_FOLDER%TPWinShortcut"
nb_shortcut = 6

# Setup callbacks and connection
TPClient = TP.Client(TP_PLUGIN_INFO["id"])
g_log = Logger(TP_PLUGIN_INFO["id"])

def updateShortcutList(directory):
    # Check if directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return []
    
    # Check if the path points to a directory
    if not os.path.isdir(directory):
        print(f"'{directory}' is not a valid directory.")
        return []

    # List files in the directory
    files = os.listdir(directory)

    # Return the list of files
    return files

def stateUpdate():
    list_file = updateShortcutList(directory_shortcuts)
    for i in range(nb_shortcut):
        TPClient.stateUpdate(f"TP.Plugins.win_shortcut.states.shortcut_path_{i}",list_file[i])
        getIcon.updateIcon(directory_shortcuts,directory_icons,list_file[i],i)


def handleSettings(settings, on_connect=False):
    global directory_shortcuts

    settings = { list(settings[i])[0] : list(settings[i].values())[0] for i in range(len(settings)) }

    if (value := settings.get(TP_PLUGIN_SETTINGS['Shortcut directory']['name'])) is not None:
        TP_PLUGIN_SETTINGS['Shortcut directory']['value'] = value
    else :
        TPClient.showNotification(
            notificationId="blasseye.TP.Plugins.Update_Check",
            title=f"TouchPortal-Windows-Shortcut : Folder path not configured",
            msg="Go to setting, Setting...>Plug-ins>Windows-Shortcut, and set the parameter.",
            options= [
                {
                    "id":"",
                    "title":"Go to parametre"
                }
            ]
        )

def checkUpdate(data):
    """Checking if Plugin needs updated"""
    github_check = TP.Tools.updateCheck("blasseye", "TouchPortal-Windows-Shortcut")
    plugin_version = str(data['pluginVersion'])
    plugin_version = plugin_version[:1] + "." + plugin_version[1:]
    if github_check[1:4] != plugin_version[0:3]:
        TPClient.showNotification(
                notificationId="blasseye.TP.Plugins.Update_Check",
                title=f"TouchPortal-Windows-Shortcut: The shortcut folder path is invalid.",
                msg="A new TouchPortal-Windows-Shortcut Version is available and ready to Download. This may include Bug Fixes and or New Features",
                options= [
                    {
                        "id":"Download Update",
                        "title":"Click here to Update"
                    }
                ])


# This event handler will run once when the client connects to Touch Portal
@TPClient.on(TP.TYPES.onConnect)
def onStart(data):
    global running
    checkUpdate(data)
    g_log.info(f"Connected to TP v{data.get('tpVersionString', '?')}, plugin v{data.get('pluginVersion', '?')}.")
    g_log.debug(f"Connection: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, True)
    running = True



    print("Connected!", data)
    # Update a state value in TouchPortal
    TPClient.stateUpdate()

@TPClient.on(TP.TYPES.onSettingUpdate)
def settingHandler(data):
    g_log.debug(f"Settings: {data}")
    if settings := data.get('settings'):
        handleSettings(settings, False)

# Shutdown handler, called when Touch Portal wants to stop your plugin.
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    print("Got Shutdown Message! Shutting Down the Plugin!")
    # Terminates the connection and returns from connect()
    TPClient.disconnect()


# main
    

def main():
    global TPClient, g_log, running
    ret = 0

    # Default log file destination
    logFile = f"./{PLUGIN_ID}.log"
    # Default log stream destination
    logStream = sys.stdout

    # Set up and handle CLI arguments. These all relate to logging options.
    # The plugin can be run with "-h" option to show available argument options.
    # Addtionally, a file constaining any of these arguments can be specified on the command line
    # with the `@` prefix. For example: `plugin-example.py @config.txt`
    # The file must contain one valid argument per line, including the `-` or `--` prefixes.
    # See the plugin-example-conf.txt file for an example config file.
    parser = ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument("-d", action='store_true',
                        help="Use debug logging.")
    parser.add_argument("-w", action='store_true',
                        help="Only log warnings and errors.")
    parser.add_argument("-q", action='store_true',
                        help="Disable all logging (quiet).")
    parser.add_argument("-l", metavar="<logfile>", 
                        help=f"Log file name (default is '{logFile}'). Use 'none' to disable file logging.")
    parser.add_argument("-s", metavar="<stream>",
                        help="Log to output stream: 'stdout' (default), 'stderr', or 'none'.")
    
    # His processes the actual command line and populates the `opts` dict.
    opts = parser.parse_args()
    del parser

    # Trim option string (they may contain spaces if read from config file)
    opts.l = opts.l.strip() if opts.l else 'none'
    opts.s = opts.s.strip().lower() if opts.s else 'stdout'
    print(opts)

    # Set minimum logging level based on passed arguments
    logLevel = "INFO"
    if opts.q: logLevel = None
    elif opts.d: logLevel = "DEBUG"
    elif opts.w: logLevel = "WARNING"

    # Set log file if -l argument was passed
    if opts.l:
        logFile = None if opts.l.lower() == "none" else opts.l
    # Set console logging if -s argument was passed
    if opts.s:
        if opts.s == "stderr": logStream = sys.stderr
        elif opts.s == "stdout": logStream = sys.stdout
        else: logStream = None   

    # Configure the Client logging based on command line arguments.
    # Since the Client uses the "root" logger by default,
    # this also sets all default logging options for any added child loggers, such as our g_log instance we created earlier.
    TPClient.setLogFile(logFile)
    TPClient.setLogStream(logStream)
    TPClient.setLogLevel(logLevel)

    # ready to go
    g_log.info(f"Starting {TP_PLUGIN_INFO['name']} v{TP_PLUGIN_INFO['version']} on {sys.platform}.") 

    try:
        TPClient.connect()
        g_log.info('TP Client closed.')
    except KeyboardInterrupt:
        g_log.warning("Caught keyboard interrupt, exiting.")
    except Exception:
        from traceback import format_exc
        g_log.error(f"Exception in TP Client:\n{format_exc()}")
        ret = -1
    finally:
        TPClient.disconnect()

    del TPClient
    running = False

    g_log.info(f"{TP_PLUGIN_INFO['name']} stopped.")
    return ret

if __name__ == "__main__":
    sys.exit(main())