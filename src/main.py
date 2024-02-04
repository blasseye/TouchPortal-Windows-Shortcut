from utils.get_icon import *
from PIL import Image
import os

folder_path = 'C:\\Users\\benja\\Jeux\\'
folder_output_icon = 'D:\\Project\\TouchPortal\\Plugin\\Shortcut\\Test-plugin\\temp\\'
files = os.listdir(folder_path)
i = 0
for file in files:
    output_ico= folder_output_icon+str(i)+'.ico'
    file_path=folder_path+file
    extension = get_extension(file_path)
    if extension == '.url':
        get_url_icon(file_path, output_ico)
    elif extension == '.lnk':
        get_lnk_icon(file_path, output_ico)
    elif extension == '.exe':
        get_exe_icon(file_path, output_ico)
    i+=1