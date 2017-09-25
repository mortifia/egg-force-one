# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#import externe
import os
import sys
import time

#import egg force one
import sysVar

import window

import utils

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
print(os.path.dirname(os.path.realpath(__file__)))

def startWin (sysVar):
    thread1 = window.window(sysVar)
    sysVar.thread1 = thread1
    thread1.setDaemon(True)
    thread1.setName("windows egg force one")
    thread1.start()
    
    #thread1.join()
    pass

def startAll(sysVar):
    startWin(sysVar)
    pass

def alwaysAlive(sysVar):
    while (sysVar.alive == True):
        time.sleep(1/60)
        if (sysVar.thread1.isAlive() == False):
            sysVar.alive = False
            pass
        pass
    pass

if __name__ == "__main__":
    startAll(sysVar)
    alwaysAlive(sysVar)
    pass