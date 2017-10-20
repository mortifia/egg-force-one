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

import usb
import control
import webUser

import utils

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

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

def startWebUser(sysVar):
    threadWebUser = webUser.WebUser(sysVar)
    sysVar.threadWebUser = threadWebUser
    threadWebUser.setDaemon(True)
    threadWebUser.setName("web user egg force one")
    threadWebUser.start()
    pass

def startAll(sysVar):
    startWebUser(sysVar)
    startUsb (sysVar)
    startControl(sysVar)
    pass

def alwaysAlive(sysVar):
    hz = 1/10 #optimisation
    while (sysVar.alive == True):
        time.sleep(hz)
        if (sysVar.threadUsb.isAlive() == False):
            print("bug usb")
            startUsb(sysVar)
            pass
        if (sysVar.threadControl.isAlive() == False):
            print("bug control")
            startControl(sysVar)
            pass
        if (sysVar.threadWebUser.isAlive() == False):
            print("bug web user")
            startWebUser(sysVar)
            pass
        pass
    pass

if __name__ == "__main__":
    startAll(sysVar)
    alwaysAlive(sysVar)
    pass