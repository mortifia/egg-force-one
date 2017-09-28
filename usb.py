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

    def ecriture(self):
        pass

    def lecture(self):
        try:
            self.tempTxt += self.sysVar.usbSerial.read(self.sysVar.usbSerial.inWaiting())
            #print(self.sysVar.usbSerial.read(self.sysVar.usbSerial.inWaiting()))
            #print(self.tempTxt)
            #print("wow")
            pass
        except:
            #print("merde")
            self.sysVar.usbConnect.close()
            self.sysVar.usbConnect = False
            pass
        else:
            pass
        pass

    def addLine(self):
        pos = len(self.tempTxt)
        tmp = 0
        stop = 0
        if (pos > 0):
            while (stop == 0):
                time.sleep(1/2)
                if (self.tempTxt[tmp] == 10 ):
                    stop = 1
                    pass
                tmp += 1
                if (tmp == pos):
                    stop = 1
                    pass
                pass
            pass
        #print("tmp : {}".format(tmp))
        #time.sleep(5)
        pass

    def recherche(self):
        self.sysVar.usbAllPort = serial.tools.list_ports.comports()
        #for element in self.sysVar.usbAllPort:
        #    print(element)
        #    pass
        pass

    def connection(self):
        self.sysVar.usbSerial = serial.Serial()
        self.sysVar.usbSerial.timeout  = 0
        self.sysVar.usbSerial.baudrate = self.sysVar.usbBauderate
        if (self.sysVar.usbPort == False):
            self.recherche()
            for port in self.sysVar.usbAllPort:
                self.sysVar.usbSerial.port = port.device
                try:
                    self.sysVar.usbSerial.open()
                    pass
                except:
                    #print("connect error")
                    #print(self.sysVar.usbSerial.port)
                    pass
                else:
                    self.sysVar.usbConnect = True
                    print("USB connecté")
                    pass
                pass
            pass
        else:
            self.sysVar.usbSerial.port = self.sysVar.usbPort
            try:
                self.sysVar.usbSerial.open()
                pass
            except:
                #print("connect error")
                #print(self.sysVar.usbSerial.port)
                pass
            else:
                self.sysVar.usbConnect = True
                print("USB connecté")
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
                self.sysVar.usbConnect == False
                pass
            pass
        pass

    def boucle(self):
        """
        elle permet de mainteneir le thread en vie
        """
        while (1):
            while (self.sysVar.connectType == "USB"): # fait fonctionner la communication usb
                time.sleep(1/120)
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