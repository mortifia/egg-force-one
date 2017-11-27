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

class Usb(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        self.tempTxt = b''
        Thread.__init__(self)
        pass

    def bugCom(self):
        self.sysVar.usbConnect.close()
        self.sysVar.usbConnect = False
        self.com = False
        with self.sysVar.lockInput:
            self.sysVar.gcodeInput = []
        with self.sysVar.lockOutput:
            self.sysVar.gcodeOutput = []
        pass

    def ecriture(self):
        if (self.sysVar.gcodeCom == True):
            if (len(self.sysVar.gcodeOutput) > 0):
                try:
                    with self.sysVar.lockOutput:
                        self.sysVar.usbSerial.write(self.sysVar.gcodeOutput[0].encode('utf-8'))
                        pass
                    pass
                except:
                    self.bugCom()
                    pass
                else:
                    with self.sysVar.lockOutput:
                        del self.sysVar.gcodeOutput[0]
                        pass
                    pass
                pass
            pass
        pass

    def lecture(self):
        try:
            self.tempTxt += self.sysVar.usbSerial.read(self.sysVar.usbSerial.inWaiting())
            pass
        except:
            self.bugCom()
            pass
        else:
            pass
        pass

    def addLine(self):
        nb = len(self.tempTxt)
        if (nb > 0):
            self.sysVar.gcodeCom = True
            pos = self.tempTxt.find(b'\n')
            if (pos != -1):
                with self.sysVar.lockInput:
                    self.sysVar.gcodeInput.append(str(self.tempTxt[0:pos], 'utf-8'))
                    pass
                self.tempTxt = self.tempTxt[pos + 1: nb]
                pass
            else:
                pass
            pass
        pass

    def recherche(self):
        self.sysVar.usbAllPort = serial.tools.list_ports.comports()
        for element in self.sysVar.usbAllPort:
            self.sysVar.threadControl.msgTerminal(element)
            pass
        pass

    def connection(self):
        time.sleep(1/2)
        self.sysVar.usbSerial = serial.Serial()
        self.sysVar.usbSerial.timeout  = 0
        self.sysVar.usbSerial.baudrate = self.sysVar.usbBauderate
        if (self.sysVar.usbPort == False):
            self.recherche()
            for port in self.sysVar.usbAllPort:
                self.sysVar.usbSerial.port = port.device
                try:
                    self.sysVar.usbSerial.open()
                    print(port.device)
                    pass
                except:
                    self.sysVar.threadControl.msgTerminal("connect error")
                    self.sysVar.threadControl.msgTerminal(self.sysVar.usbSerial.port)
                    pass
                else:
                    self.sysVar.usbConnect = True
                    self.sysVar.usbPort = port.device
                    self.sysVar.threadControl.msgTerminal("USB connecté")
                    self.sysVar.threadWebUser.inprimanteConnecterUsb() # previent les utilisateur
                    try:
                        self.sysVar.threadControl.startGcode() #lance le start gcode
                        pass
                    except:
                        self.sysVar.threadControl.msgTerminal("start gcode error")
                        pass
                    pass
                pass
            pass
        else:
            self.sysVar.usbSerial.port = self.sysVar.usbPort
            try:
                self.sysVar.usbSerial.open()
                pass
            except:
                #self.sysVar.threadControl.msgTerminal("connect error")
                #self.sysVar.threadControl.msgTerminal(self.sysVar.usbSerial.port)
                pass
            else:
                self.sysVar.usbConnect = True
                self.sysVar.threadControl.msgTerminal("USB connecté")
                self.sysVar.threadWebUser.inprimanteConnecterUsb() # previent les utilisateur
                try:
                    self.sysVar.threadControl.startGcode() #lance le start gcode
                    pass
                except:
                    self.sysVar.threadControl.msgTerminal("start gcode error")
                    pass
                pass
            pass
        pass

    def update(self):
        """
        permet la connection, la reception de donner, et l'envoi d'information
        au controlleur
        """
        if (self.sysVar.usbConnect == False):
            self.connection()
            pass
        if (self.sysVar.usbConnect == True):
            try:
                self.lecture()
                self.ecriture()
                self.addLine()
                pass
            except:
                self.sysVar.usbConnect = False
                self.sysVar.usbSerial.close()
                self.sysVar.threadWebUser.inprimanteConnecterUsb() # previent les utilisateur
                pass
            pass
        pass

    def boucle(self):
        """
        elle permet de mainteneir le thread en vie
        """
        hz = 1/120 # optimisation
        hzSleep = 1/10 # optimisation
        while (self.sysVar.alive == True):
            time.sleep(hzSleep)
            while (self.sysVar.connectType == "USB" and self.sysVar.alive == True): # fait fonctionner la communication usb
                time.sleep(hz)
                self.sysVar.usbRun = True
                self.update()
                pass
            self.sysVar.usbRun = False # previent qu'il ne tourne pas
            pass
        pass
    def run(self):
        self.boucle()
        pass
    pass

if __name__ == "__main__":
    pass