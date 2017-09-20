#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 01:15:39 2017

@author: mortifia
test param sys
"""

bauderate = 115200      # usb connection

stopAll = 0             # ne pas toucher
gcode = []              # liste de comande a envoyer au controlleur
ser = ""                # serial connection
socketio = ""           # permet d'encoyer des requetes au clients web
temp0 = ""              # extrudeur 1
temp1 = ""              # extrudeur 2
tempBed = ""            # plateau chauffant

startPrint = 0          # impression lancé
posPrint = 0            # position impression
fPrint = ""             # pointeur sur fichier en cour d'impression
finPrint = 0
pathPrint = ""          # emplacement fichier
tempPrintFolder = ""    #
countOut = 0            # nombre de commande envoyer
countIn = 0             # nomdre de commande accepté

printerTempMemory = 26  # valeur temporaire 

f = ""                  # main fenetre NE PAS TOUCHER
fPath = ""              # position dans la fenetre 


