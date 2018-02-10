# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
    This file is part of egg-force-one.

    egg-force-one is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with egg-force-one.  If not, see <http://www.gnu.org/licenses/>. 2

    ############################################################################

    Created on Mon Sep 25 16:24:39 2017
    @author: CASAL Guillaume
"""
import sys
import os
from threading import RLock

import usb
import control
import webUser
import utils

# nous place dans le dossier de l'executable
os.chdir(os.path.dirname(os.path.realpath(__file__)))
#print(os.path.dirname(os.path.realpath(__file__)))

# variable system application
path            = False             # emplacement du dossier egg force one log
paramPath       = False             # emplacement du fichier de paramettre de l'utilisateur
FolderPrint     = False             # emplacement du dossier d'impression
alive           = 0                 # matien l'application en vie et sert de code d'erreur
connectType     = "USB"             # permet de choisir le moyen de communication avec le controlleur
temp            = ['0']             # liste toutes les temperatures de l'imprimante 3D
lvlMsg          = 2                 # niveau max des message aficher
                                    # lvl = 0 "info" | lvl = 1 "erreur" | lvl = 2 "debug"
                                    # attention plus le niveau est élevé plus ca consome
allVarDict      = globals()         # permet de modifier et lire les veriables plus rapidement
autoBaud        = True              # recherche automatique du baud
allBauderate    = [1000000, 500000, 250000, 115200, 57600, 38400, 19200, 9600, 2400]
                                    # liste toutes les frequences possible
                                    # pour un future "full auto connect"

#information a afficher
logDev          = True
logPrint        = False
logError        = True
logInfo         = True

#variable impression
printStatut     = 0                 # 0 = aucune impression
                                    # 1 = impression en cour
                                    # 2 = impression terminer
printSafe       = RLock()           # permet deviter le lancement de plusieur
                                    # impression en meme temp
printLoad       = 0                 # analyse du ficher en cour
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

# variable thread Usb
usbRun          = False             # previent si il tourne
usbConnect      = False             # dit si on est connecter au controlleur
usbBug          = False             # dit si il est imposible d'etablir la connection
usbBauderate    = 250000            # frequence de communication
usbPort         = False             # port de communication si false il se connectera au premier port posible
                                    #"COM3" windown | "/dev/ttyUSB0" linux
usbAllPort      = False             # liste tout les port disponible depuis la derniere recherche
                                    # si False aucune recherche lancé si [] il y a pas de port disponible

# variable thread web
webHost            = '0.0.0.0'         # 0.0.0.0 tout le monde peut se connecté
webPort            = 8080              # port de connection 8080 est authoriser sur tout les systeme

# variable information threadControl
addStart        = False             # permet de detecté si un startGcode est deja lancé

test = "tototo" ###############################################################

# auto configuration de paramPath
if sys.platform.startswith('win'):
    print("windows")
    #usbPort = "COM3"
    paramPath = os.path.dirname(os.path.realpath(__file__))
    FolderPrint = paramPath + "\\print\\"
    if (os.path.exists(FolderPrint) == False):
        os.makedirs(FolderPrint)
        pass
    paramPath += "\\option.py"
    if (os.path.exists(paramPath) == False):
        temp = open(paramPath, "w")
        temp.close()
        del temp
        pass
    pass

elif sys.platform.startswith('linux'):
    print("linux")
    #usbPort = "/dev/ttyUSB0"
    paramPath = os.path.dirname(os.path.realpath(__file__))
    FolderPrint = paramPath + "/print/"
    if (os.path.exists(FolderPrint) == False):
        os.makedirs(FolderPrint)
        pass
    paramPath += "/option.py"
    if (os.path.exists(paramPath) == False):
        temp = open(paramPath, "w")
        temp.close()
        del temp
        pass
    pass

#del sys
#del os
#del RLock

# attention cette partie sert a prendre en compte les modification faite par l'utilisateur
import option
for tmp in utils.allVarModule(option):
    allVarDict[tmp[0]] = tmp[1]
    print("option : " + str(tmp[0]) + " = " + str(tmp[1]))
    pass


#from camera import Camera
#Camera()


if __name__ == "__main__":
    pass