# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 11:37:23 2017

@author: casal guillaume
"""

import os
from threading import Thread

import logging
from flask import Flask, Response
from flask_socketio import SocketIO

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

    #def initPrint(self):
    #    self.socketio.emit('print', str(self.sysVar.printNbLine), broadcast=True)
    #    pass

    def statutImpression(self):
        self.socketio.emit('statutImpression', self.sysVar.printStatut, broadcast=True)
        pass

    def srcImpression(self):
        self.socketio.emit('srcImpression', self.sysVar.printSrc, broadcast=True)
        pass

    def posPrint(self):
        self.socketio.emit('posPrint', self.sysVar.printPosLine, broadcast=True)
        pass

    def layerPrint(self):
        self.socketio.emit('layerPrint', self.sysVar.printLayer, broadcast=True)
        pass

    def nbLinesPrint(self):
        self.socketio.emit('nbLinesPrint', self.sysVar.printNbLine, broadcast=True)
        pass

    def nbLayerPrint(self):
        self.socketio.emit('nbLayerPrint', self.sysVar.printNbLayer, broadcast=True)
        pass

    def layer(self):
        try:
            self.socketio.emit('progressLayer', str(self.sysVar.printPosLayer[self.sysVar.printLayer]) +
                               " " + str(self.sysVar.printOldLayer), broadcast=True)
            pass
        except:
            print("bug to send end layer")
            pass
        pass

    def posEndPrint(self):
        try:
            self.socketio.emit('posEndPrint', self.sysVar.printNbLine, broadcast=True)
            pass
        except:
            print("bug to send end pos print")
            pass
        pass
    
    def updatePrint(self):
        self.statutImpression()
        self.srcImpression()
        self.posEndPrint()
        self.posPrint()
        self.layer()
        self.layerPrint()
        self.nbLinesPrint()
        self.nbLayerPrint()
        pass

    def inprimanteConnecterUsb(self):
        self.sysVar.threadControl.msgTerminal("usbConnect : " + str(self.sysVar.usbConnect))
        try:
            self.sysVar.threadControl.msgTerminal(self.sysVar.usbSerial.port)
            pass
        except:
            pass
        if (self.sysVar.usbConnect == False):
            self.socketio.emit('inprimanteConnecterUsb', "False", broadcast=True)
            pass
        else:
            self.socketio.emit('inprimanteConnecterUsb', "True", broadcast=True)
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

    def cssCharac(self):
        tmp = open("charac.css", "r")
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
        @app.route('/charac.css')
        def charac():
            return Response(self.cssCharac(), mimetype='text/css')

        @app.route('/socket.io.js')
        def routeSocketIO():
            return self.socketIO

        @app.route('/jquery.min.js')
        def routeJquery():
            return self.jquery

        @socketio.on('new user')
        def newUser(data):
            if (self.sysVar.threadControl.isAlive() == True):
                self.sysVar.threadControl.msgTerminal("utilisateur connecté")
                self.inprimanteConnecterUsb()
                if (self.sysVar.printStatut != 0):
                    self.statutImpression()
                    self.srcImpression()
                    self.posEndPrint()
                    self.posPrint()
                    self.layer()
                    self.layerPrint()
                    self.nbLinesPrint()
                    self.nbLayerPrint()
                    pass
                pass
            pass

        @socketio.on('msglvl')
        def msglvl(data):
            tmp = int(data)
            if (tmp >= 0 and tmp <= 2):
                self.sysVar.lvlMsg = tmp
                pass
            pass

        @socketio.on('STOP')
        def stop(data):
            self.sysVar.alive = False
            pass

        @socketio.on('gcode')
        def gcode(data):
            self.sysVar.threadControl.addGcode(str(data))
            pass
        @socketio.on('printSrc')
        def printSrc(data):
            try:
                if (self.sysVar.printStatut == 5):
                    self.sysVar.printStatut == -2
                    pass
                self.sysVar.threadControl.initPrint(data)
                pass
            except:
                self.socketio.emit('ALERT', "bug a printSrc")
                pass
            pass
        @socketio.on('statutPrint')
        def statutPrint(data):
            if ((data == 1 or data == 3)
            and (self.sysVar.printStatut == 2 or self.sysVar.printStatut == 4
                 or self.sysVar.printStatut == 0)):
                pass
            elif (data == 4 and self.sysVar.printStatut == 0):
                pass
            else:
                self.sysVar.printStatut = int(data)
                self.statutImpression()
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