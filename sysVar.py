# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:24:39 2017

@author: 54386
"""
import sys

paramPath = "" # emplacement du fichier de paramettre de l'utilisateur 
alive = True # ferme l'application

# liste des thread
thread1 = "" # comunication graphique avec l'utilisateur




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
    del sys
    pass
elif sys.platform.startswith('linux'):
    del sys
    pass

if __name__ == "__main__":
    pass