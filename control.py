# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
    This file is part of egg-force-one.

    egg-force-one is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with egg-force-one.  If not, see <http://www.gnu.org/licenses/>. 2

    ############################################################################

    Created on Mon Sep 25 16:24:39 2017
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
        print("test : " + str(self.sysVar.usbBug))
        if (self.sysVar.usbBug == False):
            print("add start #################")
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
    pass

"""
class rafrechisementFichierPrint(Thread):
    def __init__(self,sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass

    def run(self):
        hz = 1/4
        while (self.sysVar.printLoad == 1):
            time.sleep(hz)
            #try:
            #    self.sysVar.threadWebUser.updatePrint()
            #    pass
            #except:
            #    print("bug dans updatePrint")
            #    pass
            pass
        #try:
        #    self.sysVar.threadWebUser.updatePrint()
        #    pass
        #except:
        #    print("bug dans updatePrint")
        #    pass
        pass
    pass
"""

class analyseFichierPrint(Thread):
    def __init__(self,sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass

    #def updateThread(self):
    #    threadTime = rafrechisementFichierPrint(self.sysVar)
    #    threadTime.setDaemon(True)
    #    threadTime.start()
    #    pass

    def initialisation(self):
        if (self.sysVar.printSrc[0] == "/" or self.sysVar.printSrc[0] == "\\"):
            self.src = self.sysVar.printSrc
            pass
        else:
            self.src = self.sysVar.FolderPrint + self.sysVar.printSrc
            pass
        self.folder = open(self.src, "r", encoding="utf-8")
        self.tmpTxt = self.folder.readline()
        self.nbLigne = 1
        self.sysVar.printLoad = 1
        #self.updateThread()
        pass

    def analyse(self, tmpTxt):
        if (tmpTxt[0] == "G" and tmpTxt[2] == " "):
            if (tmpTxt[1] != "4"):
                tmpCode = tmpTxt.split(" ")
                tmpPos = 0
                lenTmpCode = len(tmpCode)
                while (tmpPos < lenTmpCode):
                    if (tmpCode[tmpPos][0] == "Z"):
                        #print("found z")
                        self.sysVar.printPosLayer.append(self.sysVar.printNbLine)
                        self.sysVar.printNbLayer += 1
                        pass
                    tmpPos += 1
                    pass
                pass
            pass
        pass

    def lectureFicher(self):
        while (self.tmpTxt and self.sysVar.printStatut != -2):
            self.analyse(self.tmpTxt)
            self.sysVar.printNbLine += 1
            self.tmpTxt = self.folder.readline()
            pass
        pass

    def fin(self):
        self.folder.close()
        if (self.sysVar.printStatut != -2):
            self.sysVar.printPosLayer.append(self.sysVar.printNbLine)
            self.sysVar.printNbLine
            pass
        self.sysVar.printLoad = 0
        print("###FIN Experimental###")
        pass

    def run(self):
        self.initialisation()
        self.lectureFicher()
        self.fin()
        pass
    pass

###############################################################################
class Control (Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
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

    def analyseFichier(self):
        threadAnalyseFichierPrint = analyseFichierPrint(self.sysVar)
        threadAnalyseFichierPrint.setDaemon(True)
        threadAnalyseFichierPrint.start()
        pass

    def initPrint(self, src):
        print("test print")
        self.sysVar.threadControl.msgTerminal("start init print :" + src)
        self.sysVar.printStatut     = 5
        self.sysVar.printSrc        = ""
        self.sysVar.printNbLine     = 1
        self.sysVar.printNbLayer    = 1
        self.sysVar.printLayer      = 0
        self.sysVar.printOldLayer   = 0
        self.sysVar.printPosLayer   = [0]
        self.sysVar.printPosLine    = 1
        with self.sysVar.printSafe:
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
                    self.folder.readline()
                    self.folder.close()
                    self.folder = open(self.tmpSrc, "r", encoding="utf-8")
                    pass
                except:
                    print("imposible d'aceder au fichier")
                    self.sysVar.printStatut = 0
                    try:
                        self.sysVar.threadWebUser.statutImpression()
                        pass
                    except:
                        print("bug to update statut not found start print")
                        pass
                    pass
                else:
                    if (self.sysVar.printStatut == 5):
                        self.countIn = 0
                        self.countOut = 0
                        self.sysVar.printSrc = src
                        self.sysVar.printStatut = 1
                        self.analyseFichier()
                        #try:
                        #    self.sysVar.threadWebUser.statutImpression()
                        #    self.sysVar.threadWebUser.srcImpression()
                        #    pass
                        #except:
                        #    print("bug to update start print")
                        #    pass
                        print("end init print 2")
                        pass
                    pass
                pass
            pass
        pass

    def onPrint(self):
        if (self.sysVar.printStatut == 1):
            if (self.countIn == self.countOut):
                tmp = self.folder.readline()
                try:
                    tmp2 = tmp.split()
                    lentmp2 = len(tmp2)
                    a = 0
                    end = 0
                    while (lentmp2 > a and end == 0):
                        if (tmp2[a][0] == ";"):
                            end = 1
                            b = 0
                            tmp = ""
                            while (b < a):
                                tmp += tmp2[b]
                                tmp += " "
                                b += 1
                                pass
                            tmp += "\n"
                            pass
                        a += 1
                        pass
                    pass
                except:
                    pass
                #try:
                #    self.sysVar.threadWebUser.posPrint();
                #    pass
                #except:
                #    print("bug to send posPrint")
                #    pass
                if (tmp == ""):
                    self.sysVar.printStatut = 2
                    #self.sysVar.threadWebUser.statutImpression()
                    self.sysVar.threadControl.msgTerminal("impression terminer I/O :" +
                                                          str(self.countIn) + " / " +
                                                          str(self.countOut))
                    pass
                elif (tmp[0] == ";" or tmp[0] == "\n"):
                    self.sysVar.printPosLine += 1
                    self.countIn  += 1
                    self.countOut += 1
                    pass
                else:
                    self.sysVar.printPosLine += 1
                    self.sysVar.threadControl.addGcode(tmp)
                    pass
                if (len(self.sysVar.printPosLayer) > 2 and self.sysVar.printStatut == 1):
                    if (self.countOut >= self.sysVar.printPosLayer[self.sysVar.printLayer]):
                        self.sysVar.printOldLayer = self.sysVar.printPosLayer[self.sysVar.printLayer]
                        self.sysVar.printLayer += 1
                        #self.sysVar.threadWebUser.layerPrint()
                        #try:
                        #    self.sysVar.threadWebUser.layer()
                        #    pass
                        #except:
                        #    print("bug to send layer")
                        #    pass
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
                        self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
                        self.sysVar.temp = [self.sysVar.gcodeInput[0]]
                        pass
                    elif (self.sysVar.gcodeInput[0] == "start"):
                        self.startGcode()
                        #self.msgTerminal("in : " + self.sysVar.gcodeInput[0])
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
        while (self.sysVar.alive == 0):
            time.sleep(hz)
            self.analyseGcode()
            self.onPrint()
            pass
        pass

    def run(self):
        self.update()
        pass
    pass
