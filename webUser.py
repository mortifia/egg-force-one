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
import signal
import shutil
from threading import Thread

import git

import logging
from flask import Flask, Response, request
#from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

#from camera import Camera

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
        #fichier = open("socket.io.js", "r")
        #self.socketIO = fichier.read()
        #fichier.close()

        fichier = open("jquery.min.js", "r")
        self.jquery = fichier.read()
        fichier.close()
        pass

    def shutdown_server(self):
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    def init(self):
        if sys.platform.startswith('win'):
            self.pathCut = "\\"
            pass
        else:
            self.pathCut = "/"
            pass
        app = Flask(__name__)
        #socketio = SocketIO(app)

        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        self.app = app
        self.log = log
        #self.socketio = socketio

        @app.route('/shutdown')
        def shutdown():
            self.shutdown_server()
            return 'Server shutting down...'

        @app.route('/')
        def home():
            return Response(self.html(), content_type='charset=utf-8')

        @app.route('/css.css')
        def css():
            return Response(self.css(), mimetype='text/css')
        @app.route('/font/<name>')
        def font(name):
            #print("name : " + str(name))
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
                print("PrintSrc : " + self.sysVar.path + " ::: "+ path)
                if (path[0] == "\\" or path[0] == "/"):
                    path = path[1:]
                    print("test path : " + self.sysVar.path + " :and: " + path)
                    pass
                if sys.platform.startswith('win'):
                    pass
                if (self.sysVar.printStatut == 0 or self.sysVar.printStatut == 2 or self.sysVar.printStatut == 4):
                    print("test")
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
                                try:
                                    dictTemp[test] = int(request.form[test])
                                    #print("type int")
                                    pass
                                except:
                                    dictTemp[test] = request.form[test]
                                    pass
                                print(test + " : change by : " + str(request.form[test]))
                                pass
                            pass
                        except:
                            #print(test + " :            not found")
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
                            dataReturn += element[0] + ","
                            pass
                        dataReturn = dataReturn[:-1]
                        dataReturn += "]"
                        dataReturn += "&"
                        pass
                    elif tmp2 is str:
                        #print(type(dictTemp[tmp]))
                        dataReturn += tmp + ":" + dictTemp[tmp] + "&"
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

        @app.route('/createDir',methods=['POST'])
        def createDir():
            path = request.form["path"]
            name = request.form["name"]
            os.mkdir(self.sysVar.FolderPrint + path + name)
            return "end"

        @app.route('/deletePathDir', methods=['POST'])
        def deletePathDir():
            path = request.form["path"]
            shutil.rmtree(self.sysVar.FolderPrint + path)
            return "end"

        @app.route('/deletePathFolder', methods=['POST'])
        def deletePathFolder():
            path = request.form["path"]
            os.remove(self.sysVar.FolderPrint + path)
            return "end"

        @app.route('/renameDirFolder', methods=['POST'])
        def renameDirFolder():
            path = request.form["path"]
            pathRename = request.form["pathRename"]
            os.rename(self.sysVar.FolderPrint + path, self.sysVar.FolderPrint + pathRename)
            return "end"

        @app.route('/changeUsb', methods=['POST'])
        def changeUsb():
            port = request.form["port"]
            bauderate = request.form["bauderate"]

            if (port == "auto"):
                port = False
                pass
            try:
                self.sysVar.usbSerial.close()
                pass
            except:
                print("serial not close")
                pass
            self.sysVar.usbPort = port
            if (bauderate == "auto"):
                self.sysVar.autoBaud = True
                pass
            else:
                self.sysVar.usbBauderate = int(bauderate)
                pass
            self.sysVar.usbBug = False
            self.sysVar.usbRun = False
            self.sysVar.usbConnect = False
            return "ok"


        def gen(camera):
            """Video streaming generator function."""
            while True:
                frame = camera.get_frame()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

        @app.route('/video_feed')
        def video_feed():
            """Video streaming route. Put this in the src attribute of an img tag."""
            return "off"
            #return Response(gen(Camera()),
            #               mimetype='multipart/x-mixed-replace; boundary=frame')



    def startWeb(self):
        self.app.run(host = self.sysVar.webHost, port = self.sysVar.webPort, threaded=True)
        #self.socketio.run(self.app, host = self.sysVar.webHost, port = self.sysVar.webPort)
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
