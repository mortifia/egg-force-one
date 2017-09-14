# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
import os
import time
import logging
from threading import Thread

#ne pas toucher
version = 0.0010
version = float(version)
urlSer = 'http://ipr-3d.com:8080'

if os.path.exists("/etc/egg-force-one"):
    os.chdir("/etc/egg-force-one")
print(os.path.exists("/etc/egg-force-one"))
# partage de données entre threads (ne pas modifier)
class varsys:
    def __init__(self):
        pass

#gestionnaire variable systeme
sysVar = varsys()


#usb connection
sysVar.bauderate = 115200

sysVar.stopAll = 0# ne pas toucher
sysVar.gcode = []# liste de comande a envoyer au controlleur
sysVar.ser = "" # serial connection
sysVar.socketio = ""#p ermet d'encoyer des requetes au clients web
sysVar.temp0 = ""# extrudeur 1
sysVar.temp1 = ""# extrudeur 2
sysVar.tempBed = ""# plateau chauffant

sysVar.startPrint = 0# impression lancé
sysVar.posPrint = 0# position impression
sysVar.fPrint = ""# pointeur sur fichier en cour d'impression
sysVar.finPrint = 0
sysVar.pathPrint = "" # emplacement fichier
sysVar.tempPrintFolder = "" #
sysVar.countOut = 0 # nombre de commande envoyer
sysVar.countIn = 0 # nomdre de commande accepté

#modifier dans 
sysVar.printerTempMemory = 26 #valeur temporaire 

sysVar.f = ""#main fenetre NE PAS TOUCHER
sysVar.fPath = ""#position dans la fenetre 
#lancement de l'interface graphique
import window

#comunication avec l'imprimante
import usb

#lancement et gestion serveur web
import web

#lance les thread
def startAll():
    thread1 = window.window(sysVar)
    thread1.start()

    thread2 = usb.usb(sysVar)
    thread2.start()

    thread3 = web.web(sysVar)
    thread3.start()

#test mise a jour
import git
try:
    git.Git().pull()
except:
	print("start[ERROR] update imposible")
	startAll()
else:
    startAll()
#startAll()