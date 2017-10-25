# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Mon Sep 25 16:24:39 2017

@author: CASAL Guillaume
"""
import sys
import os
from threading import RLock

# variable system application
path            = False             # emplacement du dossier egg force one log
paramPath       = False             # emplacement du fichier de paramettre de l'utilisateur
FolderPrint     = False             # emplacement du dossier d'impression
alive           = True              # ferme l'application
connectType     = "USB"             # permet de choisir le moyen de communication avec le controlleur
temp            = ['0']             # liste toutes les temperatures de l'imprimante 3D
lvlMsg          = 2                 # niveau max des message aficher
                                    # lvl = 0 "info" | lvl = 1 "erreur" | lvl = 2 "debug"
                                    # attention plus le niveau est élevé plus ca consome

#variable impression
printStatut     = 0                 # 0 = aucune impression
                                    # 1 = impression en cour
                                    # 2 = impression terminer
printSrc        = ""                # emplacement du fichier
printNbLine     = 0                 # nombre de ligne dans le fichier
printNbLayer    = 0                 # nombre de couches
printLayer      = 0                 # couche actuel du layer
printOldLayer   = 0                 # position de l'ancien layer
printPosLayer   = []                # position de la fin de la couche
printPosLine    = 0                 # position dans le fichier


# list de communication entre thread
lockInput       = RLock()           # gere l'acées a gcodeInput
lockOutput      = RLock()           # gere l'acées a gcodeOutput
gcodeInput      = []                # liste des commande recu
gcodeOutput     = []                # liste de commande a envoyer
gcodeOnConnect  = ['M155 S1\n']     # liste d'instruction a envoyer a la connection
gcodeCom        = False             # devient true des que du texte est recu du controlleur
                                    # pour commencer a envoyer des commande

# liste des thread
threadWin       = False             # interface graphique
threadUsb       = False             # comunication usb avec le controlleur
threadControl   = False             # comunication entre l'utilisateur et le controlleur
threadWebUser   = False             # interface utilisateur

# variable information threadUsb
usbRun          = False             # previent si il tourne
usbConnect      = False             # dit si on est connecter au controlleur
usbBauderate    = 115200            # frequence de communication
usbPort         = False             # port de communication si false il se connectera au premier port posible
                                    #"COM3" windown | "/dev/ttyUSB0" linux
usbAllPort      = False             # liste tout les port disponible depuis la derniere recherche
                                    # si False aucune recherche lancé si [] il y a pas de port disponible

# variable information threadControl
addStart        = False             # permet de detecté si un startGcode est deja lancé


# auto configuration de paramPath
if sys.platform.startswith('win'):
    print("windows")
    usbPort = "COM3"
    import ctypes.wintypes
    CSIDL_PERSONAL = 5
    SHGFP_TYPE_CURRENT = 0
    buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    paramPath = buf.value + "\\egg force one"
    FolderPrint = paramPath + "\\"
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
    usbPort = "/dev/ttyUSB0"
    paramPath = os.path.expanduser("~") + "/egg force one"
    if (os.path.exists(paramPath) == False):
        os.makedirs(paramPath)
        pass
    FolderPrint = paramPath + "/"
    paramPath += "/option.py"
    if (os.path.exists(paramPath) == False):
        temp = open(paramPath, "w")
        temp.close()
        del temp
        pass
    pass

del sys
del os
del RLock

if __name__ == "__main__":
    pass