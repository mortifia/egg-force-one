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
        try:
            self.sysVar.usbConnect.close()
            pass
        except:
            pass
        self.sysVar.usbConnect = False
        self.sysVar.usbBug = True
        self.tempTxt = b''
        #self.com = False

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
            try:
                pos = self.tempTxt.find(b'\n')
                pass
            except:
                #test provisoire
                pos = -1
                print("USB : BUG : addLine : 0")
                pass
            if (pos != -1):
                with self.sysVar.lockInput:
                    try:
                        self.sysVar.gcodeInput.append(str(self.tempTxt[0:pos], 'utf-8'))
                        pass
                    except:
                        print("USB : BUG : addLine : 1")
                        pass
                    pass
                self.tempTxt = self.tempTxt[pos + 1: nb]
                pass
            else:
                pass
            pass
        pass

    def recherche(self):
        self.sysVar.usbAllPort = serial.tools.list_ports.comports()
        #for element in self.sysVar.usbAllPort:
        #    self.sysVar.threadControl.msgTerminal(element)
        #    pass
        pass

    def testConnect(self):
        time.sleep(1)
        print("test connect : " + str(self.sysVar.usbSerial.port) + " : " + str(self.sysVar.usbSerial.baudrate))
        try:
            self.lecture()
            pass
        except:
            #print("USB : INFO : testConnect : EXIT 0")
            raise Exception('BAD BAUD')
            pass
        try:
            pos = self.tempTxt.find(b'\n')
            if (pos == -1):
                raise Exception('BAD BAUD')
                pass
            pass
        except:
            #print("USB : INFO : testConnect : EXIT 1")
            self.tempTxt = b''
            raise Exception('BAD BAUD')
            pass
        try:
            self.addLine()
            pass
        except:
            #print("USB : INFO : testConnect : EXIT 2")
            raise Exception('BAD BAUD')
            pass
        pass

    def sucessConnect(self):
        self.sysVar.usbConnect = True
        self.sysVar.usbBug = False
        self.sysVar.usbPort = str(self.sysVar.usbSerial.port)
        self.sysVar.usbBauderate = str(self.sysVar.usbSerial.baudrate)
        print("USB connecté : " + str(self.sysVar.usbPort) + " : " + str(self.sysVar.usbSerial.baudrate))
        try:
            self.sysVar.threadControl.startGcode() #lance le start gcode
            pass
        except:
            print("start gcode error")
            pass
        pass

    def autoBaud(self):
        for baud in self.sysVar.allBauderate:
            self.sysVar.usbSerial.baudrate = baud
            try:
                if (self.sysVar.usbSerial.isOpen() == True):
                    self.sysVar.usbSerial.close()
                    time.sleep(1/4)
                    pass
                if (self.sysVar.usbSerial.isOpen() == False):
                    self.sysVar.usbSerial.open()
                    self.testConnect()
                    pass
                else:
                    raise Exception("fermeture imposible")
                    pass
                pass
            except Exception as e:
                #print(e)
                #print("close")
                self.sysVar.usbSerial.close()
                time.sleep(1/4)
                pass
            else:
                # connection reussie
                self.sucessConnect()
                return True
            pass
        return False

    def connection(self):
        print("USB : start connect")
        try:
            #clean connection
            self.sysVar.usbSerial.close()
            pass
        except:
            pass
        #initialisation connection
        self.sysVar.usbSerial = serial.Serial()
        self.sysVar.usbSerial.timeout  = 0
        self.sysVar.usbSerial.baudrate = self.sysVar.usbBauderate
        #self.sysVar.usbSerial.setDTR(False)
        if (self.sysVar.usbPort == False):
            self.recherche()
            for port in self.sysVar.usbAllPort:
                # test tout les port com
                self.sysVar.usbSerial.port = port.device
                if (self.sysVar.autoBaud == True):
                    if (self.autoBaud() == True):
                        break
                    pass
                else:
                    try:
                        time.sleep(1/4)
                        self.sysVar.usbSerial.open()
                        self.testConnect()
                        pass
                    except:
                        # echec connection
                        self.sysVar.usbSerial.close()
                        pass
                    else:
                        # connection reussie
                        self.sucessConnect()
                        break
                        pass
                    pass
                pass
            if (self.sysVar.usbBug == False and self.sysVar.usbConnect == False):
                # tout a échouer
                print("0 : connect usb error")
                self.sysVar.usbBug = True
                pass
            pass
        else:
            self.sysVar.usbSerial.port = self.sysVar.usbPort
            if (self.sysVar.autoBaud == True):
                self.autoBaud()
                pass
            else:
                try:
                    self.sysVar.usbSerial.open()
                    self.testConnect()
                    pass
                except:
                    self.sysVar.usbSerial.close()
                    if (self.sysVar.usbBug == False):
                        print("1 : connect usb error")
                        pass
                    self.bugCom()
                    pass
                else:
                    # connection reussie
                    self.sucessConnect()
                    pass
                pass
            pass
        pass

    def update(self):
        """
        permet la connection, la reception de donner, et l'envoi d'information
        au controlleur
        """
        if (self.sysVar.usbConnect == False and self.sysVar.usbBug == False):
            self.connection()
            pass
        if (self.sysVar.usbConnect == True):
            try:
                #print("2 : connect usb error")
                self.lecture()
                self.ecriture()
                pass
            except:
                print("3 : connect usb error")
                self.bugCom()
                pass
            try:
                self.addLine()
                pass
            except:
                print("4 : connect usb error")
                self.bugCom()
                pass
            pass
        pass

    def boucle(self):
        """
        elle permet de mainteneir le thread en vie
        """
        hz = 1/120 # optimisation
        hzSleep = 1/10 # optimisation
        while (self.sysVar.alive == 0):
            time.sleep(hzSleep)
            while (self.sysVar.connectType == "USB" and self.sysVar.alive == 0): # fait fonctionner la communication usb
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