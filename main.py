# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
import os
#import time
#import logging
#from threading import Thread

#nous place dans le dossier de l'executable
os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(sys.argv[0])
print(os.path.dirname(os.path.realpath(__file__)))


#lance les thread
def startAll():
    import sysVar   # intercomunication entre thread systeme
    import window   # lancement de l'interface graphique
    import usb      # comunication avec l'imprimante
    import web      # lancement et gestion serveur web
    
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
    