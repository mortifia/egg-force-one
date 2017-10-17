# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:37:23 2017

@author: casal guillaume
"""

import os
import time
from threading import Thread, RLock

from flask import Flask
from flask_socketio import SocketIO

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class WebUser(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass
    
    def initData(self):
        pass
    
    def init(self):
        app = Flask(__name__)
        self.app = app

        @app.route('/')
        def home():
            return "bou"
            pass
        pass
    
    def startWeb(self):
        self.app.run(host='127.0.0.2', port=80)
        
        pass
    
    def run(self):
        self.initData()
        self.init()
        self.startWeb()
        pass        
    pass

if __name__ == "__main__":
    import sysVar
    threadWebUser = WebUser(sysVar)
    sysVar.threadWebUser = threadWebUser
    threadWebUser.setDaemon(True)
    threadWebUser.setName("web user egg force one")
    threadWebUser.start()
    pass