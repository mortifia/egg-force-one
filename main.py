# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Mon Sep 25 16:24:39 2017

@author: CASAL Guillaume
"""
#import externe
import os
import time

#import egg force one
import sysVar

import window
import usb
import control

import utils

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

def startWin (sysVar):
    threadWin = window.Window(sysVar)
    sysVar.threadWin = threadWin
    threadWin.setDaemon(True)
    threadWin.setName("windows egg force one")
    threadWin.start()
    pass

def startUsb (sysVar):
    threadUsb = usb.Usb(sysVar)
    sysVar.threadUsb = threadUsb
    threadUsb.setDaemon(True)
    threadUsb.setName("usb egg force one")
    threadUsb.start()
    pass

def startControl(sysVar):
    threadControl = control.Control(sysVar)
    sysVar.threadControl = threadControl
    threadControl.setDaemon(True)
    threadControl.setName("control egg force one")
    threadControl.start()
    pass

def startAll(sysVar):
    startWin(sysVar)
    startUsb (sysVar)
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