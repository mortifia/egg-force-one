# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:37:23 2017

@author: casal guillaume
"""

import os
import time
from threading import Thread, RLock

import logging
from flask import Flask, Response
from flask_socketio import SocketIO, send, emit

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class WebUser(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass
    def msgTerminal(self, msg=""):
        try:
            self.socketio.emit('MsgTerm', msg, broadcast=True)
            pass
        except:
            print("WEB[ERROR] msgTerm not work")
            pass
        pass
    
    def html(self):
        tmp = open("html.html", "r", encoding="utf-8")
        data = tmp.read()
        tmp.close()
        
        return data
    def css(self):
        tmp = open("css.css", "r")
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

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self.app = app
        self.log = log
        self.socketio = socketio

        @app.route('/')
        def home():
            return Response(self.html(), content_type='charset=utf-8')
        
        @app.route('/css.css')
        def css():
            return Response(self.css(), mimetype='text/css')
        
        @app.route('/socket.io.js')
        def routeSocketIO():
            return self.socketIO
        
        @app.route('/jquery.min.js')
        def routeJquery():
            return self.jquery
        
        @socketio.on('new user')
        def newUser(data):
            if (self.sysVar.threadControl.isAlive() == True):
                self.sysVar.threadControl.msgTerminal(0, "utilisateur connecté")
                pass
            pass
        
        @socketio.on('msglvl')
        def msglvl(data):
            tmp = int(data)
            if (tmp >= 0 and tmp <= 2):
                self.sysVar.lvlMsg = tmp
                pass
            pass
        
        pass
    

    def startWeb(self):
        #self.app.run(host='127.0.0.2', port=8080)
        self.socketio.run(self.app, host='0.0.0.0', port='8080')
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