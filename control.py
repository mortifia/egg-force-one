# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Tue Sep 26 16:05:05 2017

@author: CASAL Guillaume
"""

#import externe
import os
import time
from threading import Thread, RLock

import serial
import serial.tools.list_ports

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class OnStart (Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass

    def run(self):
        time.sleep(3)
        with self.sysVar.lockOutput:
            print("add start ####################")
            time.sleep(2)
            self.sysVar.gcodeOutput.extend(self.sysVar.gcodeOnConnect)
            pass
        pass
    pass

class Control (Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        self.com = False
        self.ok = False
        Thread.__init__(self)
        pass

    def startGcode(self):
        if (self.com == False):
            if (self.sysVar.gcodeCom == True):
                self.com = True
                threadOnStart = OnStart(self.sysVar)
                threadOnStart.setDaemon(True)
                threadOnStart.start()
                pass
            pass
        pass

    def analyseGcode(self):
        with self.sysVar.lockInput:
            if (len(self.sysVar.gcodeInput) != 0):
                if (len(self.sysVar.gcodeInput[0]) > 1):
                    if (self.sysVar.gcodeInput[0][0] == 'T' or self.sysVar.gcodeInput[0][1] == 'T'):
                        print("TEMP : " + self.sysVar.gcodeInput[0])
                        tmp = [self.sysVar.gcodeInput[0]]
                        self.sysVar.temp = tmp
                        #if (self.sysVar.threadWin.isAlive() == True):
                        #    self.sysVar.threadWin.updateTemp()
                    else:
                        print("???? : " + self.sysVar.gcodeInput[0])
                        pass
                    pass
                del self.sysVar.gcodeInput[0]
                pass
            pass
        pass

    def update(self):
        hz = 1/120 # optimisation
        while (1):
            time.sleep(hz)
            self.startGcode()
            self.analyseGcode()
            pass
        pass

    def run(self):
        self.update()
        pass
    pass
