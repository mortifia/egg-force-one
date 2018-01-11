# -*- coding: utf-8 -*-
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

import os
import sys
from threading import Thread

import logging
from flask import Flask, Response, request
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

import git

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class WebUser(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass

    def msgTerminal(self, msg=""):
        try:
            #self.socketio.emit('MsgTerm', msg, broadcast=True)
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
            if (len(self.sysVar.printPosLayer) > 0):
                self.socketio.emit('progressLayer', str(self.sysVar.printPosLayer[self.sysVar.printLayer]) +
                                   " " + str(self.sysVar.printOldLayer) + " "
                                   + str(self.sysVar.printPosLine), broadcast=True)
                pass
            else:
                self.socketio.emit('progressLayer', "0" + " " + "0" + " " + "0", broadcast=True)
                pass

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

    def script(self):
        tmp = open("script.js", "r", encoding="utf-8")
        data = tmp.read()
        tmp.close()
        return data

    def css(self):
        tmp = open("css.css", "r")
        data = tmp.read()
        tmp.close()
        return data

    def font(self,name):
        tmp = open("font/" + name, "rb") # lecture byte a byte
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

        if sys.platform.startswith('win'):
            self.pathCut = "\\"
            pass
        else:
            self.pathCut = "/"
            pass
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
        @app.route('/font/<name>')
        def font(name):
            print("name : " + str(name))
            return Response(self.font(name), mimetype='application/woff2')

        #@app.route('/socket.io.js')
        #def routeSocketIO():
        #    return self.socketIO

        @app.route('/jquery.min.js')
        def routeJquery():
            return self.jquery

        @app.route('/script.js')
        def routeScript():
            return Response(self.script(), mimetype='application/javascript')

        @app.route('/upload', methods=['POST'])
        def upload():
            print('web[EVENT] upload')
            f = request.files['uploadFile']
            try:
                f.save(self.sysVar.FolderPrint + request.form['groupe'] + self.pathCut + secure_filename(f.filename))
                pass
            except:
                try:
                    os.mkdir(self.sysVar.FolderPrint + request.form['groupe'])
                    print("web[EVENT] dir create")
                except:
                    print("web[ERROR] can not create dir for upload file")
                    return "BUG UPLOAD 1"
                try:
                    f.save(self.sysVar.FolderPrint + request.form['groupe'] + self.pathCut + secure_filename(f.filename))
                    pass
                except:
                    print("web[ERROR] can not upload file")
                    return "BUG UPLOAD 2"
                else:
                    return "OK"
            else:
                return "OK"
            pass

        @app.route('/dirPrint', methods=['POST'])
        def dirPrint():
            try:
                path = str(request.form['path'])
                path = path[1:]
                #print("chemin : " + path)
                pass
            except:
                path = ''
                pass
            listElements = os.listdir(self.sysVar.FolderPrint + path) #list tout les element du dossier

            nbelement = len(listElements)
            a = 0
            anser = ""
            while (a < nbelement):
                if a != 0:
                    anser += ";"
                    pass
                anser += listElements[a] + '|' + str(os.path.isdir(self.sysVar.FolderPrint + path + listElements[a]))
                a += 1
                pass

            try:
                return anser
            except:
                return "TEMP"
            pass

        @app.route('/update', methods=['POST'])
        def update():
            try:
                tmp = git.Git().pull()
                if (tmp == "Already up-to-date."):
                    return "0"      # deja a jour
                else:
                    return "1"      # mise a jour effectuer
            except:
                return "2"          # mise a jour impossible
                pass
            return "bug /update"

        @app.route('/printSrc', methods=['POST'])
        def printSrc():
            try:
                path = str(request.form['path'])
                if (path[0] == "\\" or path[0] == "/"):
                    path = path[1:]
                    print("test path : " + path)
                    pass
                if sys.platform.startswith('win'):
                    pass
                if (self.sysVar.printStatut == 0 or self.sysVar.printStatut == 2 or self.sysVar.printStatut == 4):
                    self.sysVar.threadControl.initPrint(path)
                    return "1"      # impression en cour
                else:
                    return "2"      # impossible impression en cour
                pass
            except:
                return "bugPrintSrc"
            pass

        @app.route('/paramChange', methods=['POST'])
        def paramChange():
            dictTemp = self.sysVar.allVarDict
            #print("test : " + str(request.form['test']))
            try:
                for test in dictTemp:
                    if test[0] != '_':
                        #print(str(test) + " : " + str(dictTemp[test]))
                        try:
                            if (request.form[test]):
                                dictTemp[test] = request.form[test]
                                print(test + " : change by : " + str(request.form[test]))
                                pass
                            pass
                        except:
                            print(test + " :            not found")
                            pass
                        #print(test + " : " + str(dictTemp[test]))
                        pass
                    pass
                pass
            except:
                pass
            return "end"

        @app.route('/paramGetAll', methods=['GET','POST'])
        def paramGetAll():
            self.sysVar.threadUsb.recherche()
            #print(self.sysVar.usbAllPort)

            dataReturn = ""
            dictTemp = self.sysVar.allVarDict
            for tmp in dictTemp:
                if tmp[0] != '_' and tmp != "allVarDict":
                    tmp2 = type(dictTemp[tmp])
                    if tmp == "usbAllPort":
                        dataReturn += tmp + ":" + "["
                        for element in self.sysVar.usbAllPort:
                            dataReturn += str(element[0]) + ","
                            pass
                        dataReturn += "]"
                        dataReturn += "&"
                        pass
                    elif tmp2 is str:
                        #print(type(dictTemp[tmp]))
                        dataReturn += tmp + ":'" + str(dictTemp[tmp]) + "'&"
                        pass
                    elif tmp2 is bool or tmp2 is list or tmp2 is int:
                        #print(type(dictTemp[tmp]))
                        dataReturn += tmp + ":" + str(dictTemp[tmp]) + "&"
                        pass
                    else:
                        #print("no add : " + str(type(dictTemp[tmp])))
                        pass
                    pass
                pass
            return dataReturn[:len(dataReturn)-1]

        @socketio.on('new user')
        def newUser(data):
            if (self.sysVar.threadControl.isAlive() == True):
                self.sysVar.threadControl.msgTerminal("utilisateur connecté")
                self.inprimanteConnecterUsb()
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
        def printSrcSocketIO(data):
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
        self.socketio.run(self.app, host = self.sysVar.webHost, port = self.sysVar.webPort)
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
