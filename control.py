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
        self.sysVar.threadControl.msgTerminal(2, "add start #################")
        with self.sysVar.lockOutput:
            #time.sleep(2)
            self.sysVar.gcodeOutput.extend(self.sysVar.gcodeOnConnect)
            pass
        self.sysVar.addStart = False
        pass
    pass

###############################################################################

class Control (Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        self.com = False
        self.ok = False
        Thread.__init__(self)
        pass
    def msgTerminal(self, lvl=0, msg=""):
        """
        envoi communication terminal 
        (permet de communiquer avec tout les terminal)
        
        lvl 0 = info
        lvl 1 = erreur
        lvl 2 = debug
        
        """
        if (lvl <= self.sysVar.lvlMsg):
            print(msg)
            if(self.sysVar.threadWebUser.isAlive() == True):
                self.sysVar.threadWebUser.msgTerminal(msg)
                pass
            pass
        pass
    
    def initPrint(self, src):
        self.sysVar.threadControl.msgTerminal(2, "start init print :" + src)
        pass
    
    def startGcode(self):
        if (self.sysVar.addStart == False):
            self.sysVar.addStart = True
            threadOnStart = OnStart(self.sysVar)
            threadOnStart.setDaemon(True)
            threadOnStart.start()
            pass
        pass
    
    def analyseGcode(self):
        with self.sysVar.lockInput:
            if (len(self.sysVar.gcodeInput) != 0):
                if (len(self.sysVar.gcodeInput[0]) > 1):
                    if (self.sysVar.gcodeInput[0][0] == 'T' or self.sysVar.gcodeInput[0][1] == 'T'):
                        self.msgTerminal(2, "TEMP : " + self.sysVar.gcodeInput[0])
                        tmp = [self.sysVar.gcodeInput[0]]
                        self.sysVar.temp = tmp
                        #if (self.sysVar.threadWin.isAlive() == True):
                        #    self.sysVar.threadWin.updateTemp()
                    elif (self.sysVar.gcodeInput[0] == "start"):
                        self.startGcode()
                        pass
                    else:
                        self.msgTerminal(2, "???? : " + self.sysVar.gcodeInput[0])
                        pass
                    pass
                del self.sysVar.gcodeInput[0]
                pass
            pass
        pass

    def update(self):
        hz = 1/120 # optimisation
        while (self.sysVar.alive == True):
            time.sleep(hz)
            #self.startGcode()
            self.analyseGcode()
            pass
        pass

    def run(self):
        self.update()
        pass
    pass
