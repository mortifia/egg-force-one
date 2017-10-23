# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Tue Sep 26 16:05:05 2017

@author: CASAL Guillaume
"""

#import externe
import os
import time
from threading import Thread

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
            tmp = 0
            while (tmp < len(self.sysVar.gcodeOnConnect)):
                self.sysVar.threadControl.addGcode(self.sysVar.gcodeOnConnect[tmp])
                tmp += 1
                pass                
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
        self.folder = False
        self.countOut = 0
        self.countIn = 0
        Thread.__init__(self)
        pass
    def msgTerminal(self, msg=""):
        """
        envoi communication terminal 
        (permet de communiquer avec tout les terminal)
        
        lvl 0 = info
        lvl 1 = erreur
        lvl 2 = debug
        
        """
        print(msg)
        try:
            self.sysVar.threadWebUser.msgTerminal(msg)
            pass
        except:
            print("bug to send online msg")
            pass
        pass
    
    def initPrint(self, src):
        self.sysVar.threadControl.msgTerminal("start init print :" + src)
        try:
            self.folder = open(src, "r", encoding="utf-8")
            pass
        except:
            self.sysVar.threadControl.msgTerminal("init print : bug open folder")
            pass
        else:
            n = 0
            while self.folder.readline():
                n += 1
                pass
            self.sysVar.threadControl.msgTerminal("#####test :"+ str(self.folder.readline()))
            self.sysVar.printNbLine = n
            self.sysVar.threadControl.msgTerminal("print nb ligne : " + str(self.sysVar.printNbLine))
            self.folder.close()
            self.folder = open(src, "r", encoding="utf-8")
            self.countIn = 0
            self.countOut = 0
            self.sysVar.printPosLine = 0
            self.sysVar.printStatut = 1
            pass
        pass
    
    def onPrint(self):
        if (self.sysVar.printStatut == 1):
            if (self.countIn == self.countOut):
                tmp = self.folder.readline()
                self.sysVar.printPosLine += 1
                if (tmp == ""):
                    self.sysVar.threadControl.msgTerminal("impression terminer I/O :" + 
                                                          str(self.countIn) + 
                                                          str(self.countOut))
                    self.sysVar.printStatut = 2
                    pass
                elif (tmp[0] != ";"):
                    self.sysVar.threadControl.addGcode(tmp)
                    pass
                elif (tmp[0] == ";"):
                    self.countIn  += 1
                    self.countOut += 1
                    pass
                pass
            pass
        pass
    
    def endPrint(self):
        self.folder.close()
        self.sysVar.printStatut = 2
        pass
    
    def startGcode(self):
        if (self.sysVar.addStart == False):
            self.sysVar.addStart = True
            threadOnStart = OnStart(self.sysVar)
            threadOnStart.setDaemon(True)
            threadOnStart.start()
            pass
        pass
    
    def addGcode(self, gcode):
        with self.sysVar.lockOutput:
            self.sysVar.gcodeOutput.append(gcode)
            pass 
        self.countOut += 1
        self.msgTerminal("out :" + gcode)
        self.msgTerminal("count I/O :" + str(self.countIn) + " / " + str(self.countOut))
        pass
    
    def analyseGcode(self):
        with self.sysVar.lockInput:
            if (len(self.sysVar.gcodeInput) != 0):
                if (len(self.sysVar.gcodeInput[0]) > 1):
                    if (self.sysVar.gcodeInput[0][0] == 'T' or self.sysVar.gcodeInput[0][1] == 'T'):
                        self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        self.sysVar.temp = [self.sysVar.gcodeInput[0]]
                        pass
                    elif (self.sysVar.gcodeInput[0] == "start"):
                        self.startGcode()
                        self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        pass
                    elif (self.sysVar.gcodeInput[0] == "ok"):
                        self.countIn += 1
                        self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        self.msgTerminal("count I/O :" + str(self.countIn) + " / " + str(self.countOut))
                        pass
                    else:
                        self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
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
            self.analyseGcode()
            self.onPrint()
            pass
        pass

    def run(self):
        self.update()
        pass
    pass
