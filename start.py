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
import get

#import egg force one
import  sysVar

usb     = sysVar.usb
control = sysVar.control
webUser = sysVar.webUser

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
    startControl(sysVar)
    startUsb (sysVar)
    pass

def alwaysAlive(sysVar):
    hz = 1/10 #optimisation
    while (sysVar.alive == 0):
        time.sleep(hz)
        if (sysVar.threadUsb.isAlive() == False):
            if (sysVar.alive == 0):
                print("bug usb:" + str(sysVar.alive))
                startUsb(sysVar)
                sysVar.alive = 2
                pass
            pass
        if (sysVar.threadControl.isAlive() == False):
            if (sysVar.alive == 0):
                print("bug control:" + str(sysVar.alive))
                startControl(sysVar)
                sysVar.alive = 3
                pass
            pass
        if (sysVar.threadWebUser.isAlive() == False):
            if (sysVar.alive == 0):
                print("bug web user:" + str(sysVar.alive))
                startWebUser(sysVar)
                sysVar.alive = 4
                pass
            pass
        pass
    try:
        while (True):
            get('http://' + str(sysVar.webHost) + ":"+ str(sysVar.webPort) + '/shutdown')
            pass
        pass
    except:
        pass
    pass

def start():
    startAll(sysVar)
    alwaysAlive(sysVar)
    return sysVar.alive

if __name__ == "__main__":
    #cProfile.run("start()")
    start()
    pass