# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:37:23 2017

@author: casal guillaume
"""

import os
import time
from threading import Thread, RLock

import logging
from flask import Flask
from flask_socketio import SocketIO

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class WebUser(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass

    def html(self):
        tmp = open("html.html", "r")
        data = tmp.read()
        tmp.close()
        return data

    def initData(self):
        fichier = open("socket.io.js", "r")
        self.socketIO = fichier.read()
        fichier.close()

        fichier = open("jquery.min.js", "r")
        self.jquery = fichier.read()
        fichier.close()
        pass

    def init(self):
        app = Flask(__name__)
        socketio = SocketIO(app)

        #log = logging.getLogger('werkzeug')
        #log.setLevel(logging.ERROR)

        self.app = app
        #self.log = log
        self.socketio = socketio

        @app.route('/')
        def home():
            return self.html()
        @app.route('/socket.io.js')
        def routeSocketIO():
            return self.socketIO
        @app.route('/jquery.min.js')
        def routeJquery():
            return self.jquery
        pass

    def startWeb(self):
        #self.app.run(host='127.0.0.2', port=8080)
        self.socketio.run(self.app, host='127.0.0.2', port='8080')
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