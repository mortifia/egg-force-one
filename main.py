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
import usb

import utils

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
print(os.path.dirname(os.path.realpath(__file__)))

def startWin (sysVar):
    threadWin = window.window(sysVar)
    sysVar.threadWin = threadWin
    threadWin.setDaemon(True)
    threadWin.setName("windows egg force one")
    threadWin.start()
    
    #thread1.join()
    pass
def startUsb (sysVar):
    threadUsb = usb.usb(sysVar)
    sysVar.threadUsb = threadUsb
    threadUsb.setDaemon(True)
    threadUsb.setName("usb egg force one")
    threadUsb.start()
    pass


def startAll(sysVar):
    startWin(sysVar)
    pass

def alwaysAlive(sysVar):
    while (sysVar.alive == True):
        time.sleep(1/60)
        if (sysVar.threadWin.isAlive() == False):
            sysVar.alive = False
            pass
        if (sysVar.threadUsb.isAlive() == False):
            startUsb(sysVar)
            pass
        pass
    pass

if __name__ == "__main__":
    startAll(sysVar)
    alwaysAlive(sysVar)
    pass