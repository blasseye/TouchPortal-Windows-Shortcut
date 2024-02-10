import TouchPortalAPI as TP
import os
from utils import getIcon

directory_shortcuts = '...'
directory_icons = '...'
nb_shortcut = 5

# Setup callbacks and connection
TPClient = TP.Client("TP_WIN_SHORTCUT")    

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

    
# This event handler will run once when the client connects to Touch Portal
@TPClient.on(TP.TYPES.onConnect)
def onStart(data):
    global running
    """Checking if Plugin needs updated"""
    github_check = TP.Tools.updateCheck("blasseye", "TouchPortal-Windows-Shortcut")
    plugin_version = str(data['pluginVersion'])
    plugin_version = plugin_version[:1] + "." + plugin_version[1:]
    if github_check[1:4] != plugin_version[0:3]:
        TPClient.showNotification(
                notificationId="blasseye.TP.Plugins.Update_Check",
                title=f"TouchPortal-Windows-Shortcut v{github_check[1:4]} is available",
                msg="A new TouchPortal-Windows-Shortcut Version is available and ready to Download. This may include Bug Fixes and or New Features",
                options= [
                    {
                        "id":"Download Update",
                        "title":"Click here to Update"
                    }
                ])

    running = True
    print("Connected!", data)
    # Update a state value in TouchPortal
    TPClient.stateUpdate("ExampleState", "Connected!")

@TPClient.on(TP.TYPES.onSettingUpdate)
def settingHandler(data):
    global folder_shortcut

    folder_shortcut = data['values'][6]['Audio State Exemption List']
    if audio_exempt_list == "Enter '.exe' name seperated by a comma for more than 1": audio_exempt_list = []

# Shutdown handler, called when Touch Portal wants to stop your plugin.
@TPClient.on(TP.TYPES.onShutdown)
def onShutdown(data):
    print("Got Shutdown Message! Shutting Down the Plugin!")
    # Terminates the connection and returns from connect()
    TPClient.disconnect()

# After callback setup like we did then we can connect.
# Note that `connect()` blocks further execution until
# `disconnect()` is called in an event handler, or an
# internal error occurs.
TPClient.connect()