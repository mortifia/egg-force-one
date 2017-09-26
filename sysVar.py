# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:24:39 2017

@author: 54386
"""
import sys
import os

paramPath = "" # emplacement du fichier de paramettre de l'utilisateur
alive = True # ferme l'application

# liste des thread
threadWin = False # interface graphique
threadUsb = False # comunication usb avec le controlleur

# variable information threadWin

# variable information threadUsb
usbStart = False # previent si il est en fonctionnement
usbConnect = False # dit si on est connecter au controlleur
usbBauderate = 9600 # frequence de communication
usbPort = False # port de communication

if sys.platform.startswith('win'):
    print("windows")
    import ctypes.wintypes
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    paramPath = buf.value + "\\egg force one"
    del CSIDL_PERSONAL
    del SHGFP_TYPE_CURRENT
    del buf
    del ctypes
    if (os.path.exists(paramPath) == False):
        os.makedirs(paramPath)
        pass
    paramPath += "\\option.py"
    if (os.path.exists(paramPath + "\\option.py") == False):
        temp = open(paramPath, "w")
        temp.close()
        del temp
        pass
    pass

elif sys.platform.startswith('linux'):
    print("linux")
    paramPath = os.path.expanduser("~") + "/egg force one"
    if (os.path.exists(paramPath) == False):
        print("egg force one exist")
        os.makedirs(paramPath)
        pass
    os.makedirs(paramPath)
    paramPath += "/option.py"
    if (os.path.exists(paramPath) == False):
        temp = open(paramPath, "w")
        temp.close()
        del temp
        pass
    pass

del sys
del os

if __name__ == "__main__":
    pass