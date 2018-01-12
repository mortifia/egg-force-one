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
import requests

#import egg force one
import start

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

def analyseStart ():
    errorCode = -1
    while (errorCode == -1):
        #import egg force one
        print("start")
        errorCode = start.start()
        errorCode = int(errorCode)
        time.sleep(2)
        if (errorCode == -1):
            print("restart")

            try:
                print("reload 0-1 test")
                import importlib
                importlib.reload(start.sysVar.usb)
                importlib.reload(start.sysVar.control)
                importlib.reload(start.sysVar.webUser)
                importlib.reload(start.sysVar.utils)
                importlib.reload(start.sysVar)
                importlib.reload(start)
                print("reload 0-1 finish successful")
                pass
            except:
                print("reload 0-2 test")
                try:
                    import imp
                    imp.reload(start.sysVar.usb)
                    imp.reload(start.sysVar.control)
                    imp.reload(start.sysVar.webUser)
                    imp.reload(start.sysVar.utils)
                    imp.reload(start.sysVar)
                    imp.reload(start)
                    print("reload 0-2 finish successful")
                    pass
                except:
                    print("all test bug")
                    pass
                pass
            pass
        else:
            print("stop : " + str(errorCode))
            pass

if __name__ == "__main__":
    #cProfile.run("start()")
    analyseStart()
    pass