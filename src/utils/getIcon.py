import configparser
import os
import shutil
import win32api
import win32ui
import win32gui
import win32com.client
import win32con

from utils.tools import get_target_path, get_extension

def get_url_icon(file_path, output_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    if 'InternetShortcut' in config:
        icon_file = config['InternetShortcut'].get('IconFile')
        extension = get_extension(icon_file)
        if extension == ".ico":
            shutil.copy(icon_file, output_path)
            return
        elif extension == ".exe":
            icon = get_exe_icon(icon_file, output_path)
            return 
    else:
        return

def get_lnk_icon(file_path, output_path):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(file_path)
    icon_location = shortcut.IconLocation.split(',')
    icon_file = icon_location[0].strip('"')
    extension = get_extension(icon_file)
    if extension == ".ico":
        shutil.copy(icon_file, output_path)
        return
    else : 
        target = get_target_path(file_path)
        extension = get_extension(target)
        if extension == ".exe":
            icon = get_exe_icon(target, output_path)
            return
    return

def get_exe_icon(file_path, output_path):
    ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
    ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)
    print(ico_x)
    print(ico_y)
    large, small = win32gui.ExtractIconEx(file_path, 0)
    win32gui.DestroyIcon(small[0])
    hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
    hbmp = win32ui.CreateBitmap()
    hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_x)
    hdc = hdc.CreateCompatibleDC()
    hdc.SelectObject( hbmp )
    hdc.DrawIcon( (0,0), large[0] )
    hbmp.SaveBitmapFile( hdc, output_path)    
    return

def updateIcon(folder_path,folder_output_icon,file,nb):
    output_ico = f"{folder_output_icon}shortcut_icon_{nb}.ico"
    file_path = f"{folder_path}{file}"
    extension = get_extension(file_path)
    if extension == '.url':
        get_url_icon(file_path, output_ico)
    elif extension == '.lnk':
        get_lnk_icon(file_path, output_ico)
    elif extension == '.exe':
        get_exe_icon(file_path, output_ico)