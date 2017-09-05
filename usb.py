# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
import os
import time
from threading import Thread

#comunication avec l'imprimante

import serial

class usb(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
    #va se connecter a la premiere carte possible 
    def reprise(self):
        try:
            self.sysVar.tempPrintFolder = open('.restart.txt', 'r')
        except:
            print("usb[ERROR] relancement non possible possible manque de droit")
        else:
            print('usb[EVENT] all green :3 relancement possible')
            a = 1
            b = 1
            while a != "":
                c = b
                b = a
                a = self.sysVar.tempPrintFolder.readline()
            #print("dev[_var_] c :" + c)
            self.sysVar.tempPrintFolder.close()
            self.sysVar.tempPrintFolder = open('.restart.txt', 'r')
            temp = self.sysVar.tempPrintFolder.readline()
            self.sysVar.tempPrintFolder.close()
            self.sysVar.pathPrint = temp[:-2]
            try:
                self.sysVar.fPrint = open(pathPrint, 'r')
            except:
                print('usb[ERROR] Fichier a imprimer introuvable :' + pathPrint + '$')
            else :
                self.sysVar.startPrint = 1
                self.sysVar.posPrint = int(c) - self.sysVar.printerTempMemory - 1
                a = self.sysVar.posPrint
                while a < self.sysVar.posPrint:
                    self.sysVar.fPrint.readline()
                self.sysVar.gcode.append("G28 Z\n")
                self.sysVar.gcode.append("G28 XY\n")
                
    def search(self):
        path = "/dev/serial/by-id/"
        test = 0
        self.sysVar.ser = serial.Serial()
        self.sysVar.ser.baudrate = 115200
        self.sysVar.ser.timeout  = 0
        # tant qu'il n'aura pas reussi a se connecter
        while test == 0 and self.sysVar.stopAll == 0:
            try:
                list = os.listdir("/dev/serial/by-id")
            except:
                time.sleep(1)
                print('usb[ERROR] aucune carte connecté')
            else:
                #teste si il peut se connecté a un des usb connecter
                while len(list) != 0 and test == 0:
                    try:
                        self.sysVar.ser.port = path + str(list[0])
                        self.sysVar.ser.open()
                    except:
                        print('usb[ERROR] connection impossible a', path, list[0])
                        del list[0]
                        if len(list) == 0:
                            time.sleep(1)
                    else:
                        test = 1
                        print('usb[EVENT] carte connecté')
                        if os.path.exists(".restart.txt"):
                            print('usb[EVENT] coupure non voulue, reprise lancé')
                            self.reprise()

    #lire les retour de la carte et ecrire dans les bonnes variables 
    def analyseGcode(self, txt):
        a = 0
        lentxt = len(txt) - 1
        if a < lentxt:
            #print("usb[EVENT] debug analyse gcode :", txt)
            if txt[a] == "o" and txt[a + 1] == "k":
                self.sysVar.countIn += 1
                if lentxt > 2:
                    print("usb[ok txt]" + txt)
                else:
                    #print("usb[ok]")
                    pass
            elif txt == "echo:busy: processing":
                #print('woooooooooooooooooooooooooo')
                time.sleep(1)
            #test si on a recu les température
            elif txt[a + 1] == 'T' and txt[a + 2] == ":":
                data = txt.split()
                if len(data) == 3:
                    temp = data[0].split(":")
                    self.sysVar.temp0 = temp[1]
                    temp = data[1].split("/")
                    self.sysVar.temp1 = temp[1]
                    if len(data[2]) >= 3:
                        temp = data[2].split(":")
                        self.sysVar.tempBed = temp[1]
                    #print("usb[TEMP]\t1 = " + self.sysVar.temp0 +
                    #      "C°\t2 = " + self.sysVar.temp1 +
                    #      "C°\tp = " + self.sysVar.tempBed + "C°")
                    self.sysVar.socketio.emit('temp', self.sysVar.temp0 + '/' 
                        + self.sysVar.temp1 + '/' 
                        + self.sysVar.tempBed, broadcast= True)
            else:
                print("usb[EVENT]" + txt)
                pass

    def lancement(self):
        endLine = 0
        oldLine = None

        line = ""
        time.sleep(2)
        self.sysVar.gcode.append("M155 S1\n")

        while self.sysVar.stopAll == 0:
            time.sleep(1/120)
            try:
                posL = self.sysVar.ser.inWaiting()
                if posL > 0:
                    if oldLine != None:
                        #print("pass2:", oldLine)
                        line = oldLine + self.sysVar.ser.read(posL)
                        #print("pass3:", line)
                    else:
                        line = self.sysVar.ser.read(posL)
                    posL = len(line)
                    #time.sleep(1)
                    #posEnd = posL
                    #print(line)
                    if len(line) != 0:
                        if line[posL -1] == 10:
                            oldLine = None
                        else:
                            oldLine = line
                            line = ""
            except:
                print("usb[ERROR] read serial 1")
                line = ""
                oldLine = None
                self.search()
                #permet de reprendre l'inpression en cour
                time.sleep(2)
                self.sysVar.gcode.insert(0, 'M114')
                self.sysVar.countOut = 0
                self.sysVar.countIn = 0
                self.sysVar.gcode.append("M155 S1\n")
            else:
                #lit ce que la carte a envoyer 
                if len(line) != 0:
                    line = str(line, 'utf-8')
                    txt = line.splitlines()
                    line = ""
                    a = 0
                    while a < len(txt):
                        usb.analyseGcode(self, txt[a])
                        a += 1
                #ajoute le code du fichier a imprimer dans la liste d'envoi
                if self.sysVar.startPrint == 1:
                    if (self.sysVar.countOut - self.sysVar.countIn) <= 2  :
                        tempLine = self.sysVar.fPrint.readline()
                        if len(tempLine) == 0:
                            self.sysVar.startPrint = 0
                            print("print[EVENT]impression terminer")
                            self.sysVar.tempPrintFolder.close()
                            os.remove(".restart.txt")
                        else:
                            posTempLine = len(tempLine)
                            a = 0
                            #while pos
                            if tempLine[0] != ';' and tempLine[0] != ' ' and tempLine[0] != '\n':
                                #print(tempLine)
                                #print(self.sysVar.posPrint) # position dans le fichier 
                                self.sysVar.gcode.append(tempLine)
                            else:
                                #print(tempLine)
                                #print(self.sysVar.posPrint)
                                pass
                            #print("dev[_var_] posPrint :" + str(self.sysVar.posPrint))
                            self.sysVar.tempPrintFolder = open('.restart.txt', 'a')
                            self.sysVar.tempPrintFolder.write(str(self.sysVar.posPrint) + "\n")
                            self.sysVar.tempPrintFolder.close()
                            self.sysVar.posPrint += 1
                #envoi le gcode a la carte
                if len(self.sysVar.gcode) > 0:
                    print("usb[WRITE] " + self.sysVar.gcode[0][:len(self.sysVar.gcode[0])-1])
                    try:
                        #print("I/O:" + str(countIn) + "/" + str(countOut))
                        self.sysVar.ser.write(self.sysVar.gcode[0].encode('utf-8'))
                        self.sysVar.countOut += 1
                    except:
                        print("usb[ERROR] carte déconnecter")
                        #print("I/O:" + str(countIn) + "/" + str(countOut))
                        self.search()
                        #permet de reprendre l'impression en cour
                        time.sleep(2)
                        self.sysVar.gcode.insert(0, 'M114')
                        self.sysVar.countOut = 0
                        self.sysVar.countIn = 0
                        #print("I/O:" + str(countIn) + "/" + str(countOut))

                    else:
                        del self.sysVar.gcode[0]
        print("usb[EVENT] usb stop")
        sys.exit('usb[EVENT] usb stop')
        os._exit('0')

    #lancement du module usb
    def run(self):
        self.search()
        self.lancement()
