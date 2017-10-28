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
        self.sysVar.threadControl.msgTerminal("add start #################")
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
        isConnect = 0
        if (self.sysVar.connectType == "USB"):
            isConnect = 1
            pass
        if (src[0] == "/" or src[0] == "\\"):
            self.tmpSrc = src
            pass
        else:
            self.tmpSrc = self.sysVar.FolderPrint + src
            pass
        if (isConnect == 1):
            try:
                self.folder = open(self.tmpSrc, "r", encoding="utf-8")
                pass
            except:
                self.sysVar.threadControl.msgTerminal("init print : bug open folder")
                pass
            else:
                self.sysVar.posLayer = []
                self.sysVar.printNbLayer = 0
                n = 1
                tmpTxt = tmpTxt = self.folder.readline()
                while (tmpTxt):
                    #print(n)
                    if (tmpTxt[0] == "G" and tmpTxt[2] == " "):
                        if (tmpTxt[1] != "4"):
                            tmpCode = tmpTxt.split(" ")
                            tmpPos = 0
                            lenTmpCode = len(tmpCode)
                            while (tmpPos < lenTmpCode):
                                if (tmpCode[tmpPos][0] == "Z"):
                                    #print("found z")
                                    self.sysVar.printPosLayer.append(n)
                                    self.sysVar.printNbLayer += 1
                                    pass
                                tmpPos += 1
                                pass
                            pass
                        pass
                    n += 1
                    tmpTxt = self.folder.readline()
                    pass
                self.sysVar.printPosLayer.append(n)
                print("end init print 1")
                self.sysVar.threadControl.msgTerminal("#####test :"+ str(self.folder.readline()))
                self.sysVar.printNbLine = n
                self.sysVar.threadControl.msgTerminal("print nb ligne : " + str(self.sysVar.printNbLine))
                self.sysVar.threadControl.msgTerminal("print nb layer : " + str(self.sysVar.printNbLayer))
                self.folder.close()
                self.folder = open(self.tmpSrc, "r", encoding="utf-8")
                self.countIn = 0
                self.countOut = 0
                self.sysVar.printPosLine = 0
                self.sysVar.printLayer = 0
                self.sysVar.printOldLayer = 0
                self.sysVar.printStatut = 1
                self.sysVar.printSrc = src
                self.sysVar.threadWebUser.statutImpression()
                self.sysVar.threadWebUser.srcImpression()
                self.sysVar.threadWebUser.layerPrint()
                self.sysVar.threadWebUser.nbLinesPrint()
                self.sysVar.threadWebUser.nbLayerPrint()
                try:
                    self.sysVar.threadWebUser.posEndPrint()
                    pass
                except:
                    print("bug to update start print")
                    pass
                print("end init print 2")
                pass
            pass
        pass

    def onPrint(self):
        if (self.sysVar.printStatut == 1):
            if (self.countIn == self.countOut):
                tmp = self.folder.readline()
                self.sysVar.printPosLine += 1
                try:
                    self.sysVar.threadWebUser.posPrint();
                    pass
                except:
                    print("bug to send posPrint")
                    pass
                if (tmp == ""):
                    self.sysVar.printStatut = 2
                    self.sysVar.threadWebUser.statutImpression()
                    self.sysVar.threadControl.msgTerminal("impression terminer I/O :" +
                                                          str(self.countIn) + " / " +
                                                          str(self.countOut))
                    pass
                elif (tmp[0] == ";" or tmp[0] == "\n"):
                    self.countIn  += 1
                    self.countOut += 1
                    pass
                else:
                    self.sysVar.threadControl.addGcode(tmp)
                    pass
                if (self.countOut >= self.sysVar.printPosLayer[self.sysVar.printLayer]):
                    self.sysVar.printOldLayer = self.sysVar.printPosLayer[self.sysVar.printLayer]
                    self.sysVar.printLayer += 1
                    self.sysVar.threadWebUser.layerPrint()
                    try:
                        self.sysVar.threadWebUser.layer()
                        pass
                    except:
                        print("bug to send layer")
                        pass
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
        ####################################
        #self.msgTerminal("out :" + gcode)
        #self.msgTerminal("count I/O :" + str(self.countIn) + " / " + str(self.countOut))
        pass

    def analyseGcode(self):
        with self.sysVar.lockInput:
            if (len(self.sysVar.gcodeInput) != 0):
                if (len(self.sysVar.gcodeInput[0]) > 1):
                    if (self.sysVar.gcodeInput[0][0] == 'T' or self.sysVar.gcodeInput[0][1] == 'T'):
                        #self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        self.sysVar.temp = [self.sysVar.gcodeInput[0]]
                        pass
                    elif (self.sysVar.gcodeInput[0] == "start"):
                        self.startGcode()
                        self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        pass
                    elif (self.sysVar.gcodeInput[0] == "ok"):
                        self.countIn += 1
                        #self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        #self.msgTerminal("count I/O :" + str(self.countIn) + " / " + str(self.countOut))
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
