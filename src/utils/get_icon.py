import configparser
import shutil
import win32api
import win32ui
import win32gui
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
            return icon
    else:
        return None

def get_lnk_icon(file_path, output_path):
    target = get_target_path(file_path)
    extension = get_extension(target)
    if extension == ".exe":
        icon = get_exe_icon(target, output_path)
        return icon

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