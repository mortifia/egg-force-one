# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Sat Sep 16 01:15:39 2017

@author: mortifia
"""

import os
import sys

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
print(os.path.dirname(os.path.realpath(__file__))) 

from lib import sysVar
from lib import window
from lib import usb
from lib import web


sysVar.argv = sys.argv
def startAll():             # lance les thread
   # from lib import sysVar  # intercomunication entre thread systeme
    
    #from lib import window  # lancement de l'interface graphique
    threadWindow = window.window(sysVar)
    threadWindow.setDaemon(True)
    threadWindow.setName("windows egg force one")
    threadWindow.start()
    
    #from lib import usb     # comunication avec l'imprimante
    thread2 = usb.usb(sysVar)
    thread2.setDaemon(True)
    thread2.start()

    #from lib import web     # lancement et gestion serveur web
    thread3 = web.web(sysVar)
    thread3.setDaemon(True)
    thread3.start()

# mise a jour provisoire
def updateOld():
    import git
    try:
        git.Git().pull()
    except:
        print("start[ERROR] update imposible")
    else:
        pass
#startAll()

if __name__ == "__main__":
    updateOld()
    startAll()
    