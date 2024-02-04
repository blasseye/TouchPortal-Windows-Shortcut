import configparser
import os
import win32com.client

def get_url(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    if 'InternetShortcut' in config:
        url = config['InternetShortcut'].get('URL')
        return url
    else:
        return None

def get_extension(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    return extension

def get_target_path(file_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(file_path)
    target_path = shortcut.TargetPath
    return target_path