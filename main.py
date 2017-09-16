# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Sat Sep 16 01:15:39 2017

@author: mortifia
"""
import os

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__))) 

def startAll():     # lance les thread
    from lib import sysVar   # intercomunication entre thread systeme
    
    from lib import window   # lancement de l'interface graphique
    thread1 = window.window(sysVar)
    thread1.start()
    
    from lib import usb      # comunication avec l'imprimante
    thread2 = usb.usb(sysVar)
    thread2.start()

    from lib import web      # lancement et gestion serveur web
    thread3 = web.web(sysVar)
    thread3.start()

# mise a jour provisoire
import git
try:
    git.Git().pull()
except:
	print("start[ERROR] update imposible")
	startAll()
else:
    startAll()

#startAll()
