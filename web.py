# -*- coding: utf-8 -*-
#!/usr/bin/python3

import logging
from threading import Thread


#lancement et gestion serveur web

from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename

class web(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
    def run(self):
        
        #precharge html
        fichier = open("web.html", "r")
        html = fichier.read()
        fichier.close()

        fichier = open("lib/socket.io.js", "r")
        fSocketIO = fichier.read()
        fichier.close()

        fichier = open("lib/jquery.min.js", "r")
        fJquery = fichier.read()
        fichier.close()

        app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        socketio = SocketIO(app)
        self.sysVar.socketio = socketio
        @app.route('/')
        def home():
            return html
        @app.route('/socket.io.js')
        def routeSocketIO():
            return fSocketIO
        @app.route('/jquery.min.js')
        def routeJquery():
            return fJquery
        @app.route('/upload', methods=['POST'])
        def upload():
            print('web[EVENT] upload')
            f = request.files['uploadFile']
            try:
                f.save('groupe/' + request.form['groupe'] + '/' + secure_filename(f.filename))
            except:
                try:
                    os.mkdir('groupe/' + request.form['groupe'])
                    print("web[EVENT] dir create")
                except:
                    print("web[ERROR] can not create dir for upload file")
                try:
                    f.save('groupe/' + request.form['groupe'] + '/' + secure_filename(f.filename))
                except:
                    print("web[ERROR] can not upload file")
            return "OK"

        @socketio.on('connect')
        def connect():
            print('il y a eu une connection')    
        @socketio.on('message')
        def test(message):
            print('message recu : ' + message)
        #permet d'ajouté une commande gcode a la liste d'envoi
        @socketio.on('gcode')
        def gcodeData(data):
            if data != "" :
                if data[0:3] == 'SYS':
                    dataCut = data.split()
                    if dataCut[0] == 'SYS0':
                        print('web[EVENT] start Cut of the launched software')
                        self.sysVar.stopAll = 1
                        f.destroy()
                        print('win[EVENT] widows stop')
                        socketio.stop()
                        #print('web[EVENT] web stop')
                        sys.exit('web[EVENT] web stop')
                        os._exit('0')
                else:
                    self.sysVar.gcode.append(data + '\n')
            else:
                print("web[WARNING] received empty gcode")
        #permet de lancer une impression
        @socketio.on('print')
        def runprint(data):
            if self.sysVar.startPrint != 0:
                self.sysVar.fPrint.close()
                tempPrintFolder.close()
                self.sysVar.startPrint = 0
            self.sysVar.posPrint = 0
            try:
                self.sysVar.fPrint = open(data, "r")
            except:
                print("web[ERROR]file not found :" + data)
            else:
                try:
                    tempPrintFolder = open(".restart.txt","w")
                    print("dev[_VAR_] data :" + data + '$')
                    tempPrintFolder.write(str(data))
                    tempPrintFolder.close()
                except:
                    print("web[ERROR] for restart print please delete \".restart.txt\"" 
                        + "\n im not the right acess for overwrite the file")
                self.sysVar.pathPrint = data
                self.sysVar.startPrint = 1
                self.sysVar.countOut = 0
                self.sysvar.countIn = 0
                print("web[EVENT] start print")
                socketio.emit('startPrint', data, broadcast= True)
        socketio.run(app, host='0.0.0.0', port= '8080')
