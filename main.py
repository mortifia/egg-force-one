# -*- coding: utf-8 -*-
#!/usr/bin/python3

import sys
import os
import time
import logging
from threading import Thread

#ne pas toucher
version = 0.0010
version = float(version)
urlSer = 'http://ipr-3d.com:8080'

if os.path.exists("/var/egg-force-one"):
    os.chdir("/var/egg-force-one")

# partage de données entre threads (ne pas modifier)
stopAll = 0# ne pas toucher
gcode = []# liste de comande a envoyer au controlleur
ser = "" # serial connection
socketio = ""#p ermet d'encoyer des requetes au clients web
temp0 = ""# extrudeur 1
temp1 = ""# extrudeur 2
tempBed = ""# plateau chauffant

startPrint = 0# impression lancé
posPrint = 0# position impression
fPrint = ""# pointeur sur fichier en cour d'impression
finPrint = 0
pathPrint = "" # emplacement fichier
tempPrintFolder = "" #
countOut= 0 # nombre de commande envoyer
countIn= 0 # nomdre de commande accepté

#modifier dans 
printerTempMemory = 26 #valeur temporaire 

f= ''#main fenetre NE PAS TOUCHER
fPath=''#position dans la fenetre 

#lancement de l'interface graphique
class window(Thread):
    def __init__(self):
        Thread.__init__(self)

    def lineInfo(self):
        from tkinter import Button, PhotoImage

        global f

        if self.lineHome == 0:
            pass
            
        self.lineHome = 1
        self.infoImg1 = PhotoImage(file='img/home.png')
        self.infoButton0 = Button(f, 
            image = self.infoImg1,
            command = self.home)
        self.infoButton0.place(x = 0, y = 0)

    def control(self):
        from tkinter import Button, PhotoImage

        global f
        global fPath

        self.clean()
        fPath = 'control'

        self.lineInfo()
        

    def option(self):
        from tkinter import Button, PhotoImage

        global f
        global fPath

        self.clean()
        fPath = 'option'

        self.lineInfo()

        self.optionButton0 = Button(f, text = 'wifi', 
            font = (None, 18), 
            height = 1, width = 28)
        self.optionButton0.place(x = 15, y = 80)


    def home(self):
        from tkinter import Button, PhotoImage

        global f
        global fPath

        self.clean()
        fPath = 'home'

        # met a jour la ligne d'info en haut 
        if self.lineHome == 1:
            self.infoButton0.destroy()

        #
        self.homeButton0 = Button(f, text='control', 
            command = self.control, 
            height = 10, width = 10)
        self.homeButton0.place(x = 20, y = 575)

        self.homeImg1 = PhotoImage(file='img/option.png')
        self.homeButton1 = Button(f, 
            image = self.homeImg1,
            command = self.option)
        self.homeButton1.place(x = 250, y = 575)

    def clean(self):
        global fPath

        print("win[EVENT] Start clean")
        temp = fPath.split("/")
        print(temp[0])
        if temp[0] == 'home':
            self.homeButton0.destroy()
            self.homeButton1.destroy()
        if temp[0] == 'option':
            self.optionButton0.destroy()


        pass

    def initialisation(self):
        from tkinter import Tk
        global f
        global fPath
        f = Tk()
        f.geometry('480x800+0+0')
        f.overrideredirect(1)
        self.lineHome = 0
        self.home()
        f.mainloop()
        sys.exit('win[EVENT] widows stop')
        os._exit('0')

    def run(self):
        self.initialisation()
        
#comunication avec l'imprimante
import serial
class usb(Thread):
    def __init__(self):
        Thread.__init__(self)
    #va se connecter a la premiere carte possible 
    def reprise(self):
        try:
            tempPrintFolder = open('.restart.txt', 'r')
        except:
            print("usb[ERROR] relancement non possible possible manque de droit")
        else:
            print('usb[EVENT] all green :3 relancement possible')
            a = 1
            b = 1
            while a != "":
                c = b
                b = a
                a = tempPrintFolder.readline()
            print("dev[_var_] c :" + c)
            tempPrintFolder.close()
            tempPrintFolder = open('.restart.txt', 'r')
            global pathPrint
            temp = tempPrintFolder.readline()
            tempPrintFolder.close()
            pathPrint = temp[:-2]
            global fPrint
            try:
                fPrint = open(pathPrint, 'r')
            except:
                print('usb[ERROR] Fichier a imprimer introuvable :' + pathPrint + '$')
            else :
                global startPrint
                startPrint = 1
                global posPrint
                global printerTempMemory
                posPrint = int(c) - printerTempMemory - 1
                a = posPrint
                while a < posPrint:
                    fPrint.readline()
                global gcode
                gcode.append("G28 Z\n")
                gcode.append("G28 XY\n")

                #global countOut
                #global countIn
                #countOut = 0
                #countIn = 0

    def search(self):
        global ser
        global stopAll
        path = "/dev/serial/by-id/"
        test = 0
        ser = serial.Serial()
        ser.baudrate = 115200
        ser.timeout  = 0
        # tant qu'il n'aura pas reussi a se connecter
        while test == 0 and stopAll == 0:
            try:
                list = os.listdir("/dev/serial/by-id")
            except:
                time.sleep(1)
                print('usb[ERROR] aucune carte connecté')
            else:
                #teste si il peut se connecté a un des usb connecter
                while len(list) != 0 and test == 0:
                    try:
                        ser.port = path + str(list[0])
                        ser.open()
                    except:
                        print('usb[ERROR] connection impossible a', path, list[0])
                        del list[0]
                        if len(list) == 0:
                            time.sleep(1)
                    else:
                        test = 1
                        print('usb[EVENT] carte connecté')
                        if os.path.exists(".restart.txt"):
                            print('usb[EVENT] coupure non voulue, reprise lancé')
                            self.reprise()

    #lire les retour de la carte et ecrire dans les bonnes variables 
    def analyseGcode(txt):
        global countIn
        a = 0
        lentxt = len(txt) - 1
        if a < lentxt:
            if txt[a] == "o" and txt[a + 1] == "k":
                countIn += 1
                if lentxt > 2:
                    print("usb[ok txt]" + txt)
                else:
                    #print("usb[ok]")
                    pass
            elif txt == "echo:busy: processing":
                #print('woooooooooooooooooooooooooo')
                time.sleep(1)
            #test si on a recu les température
            elif txt[a + 1] == 'T' and txt[a + 2] == ":":
                data = txt.split()
                if len(data) == 3:
                    temp = data[0].split(":")
                    global temp0
                    temp0 = temp[1]
                    temp = data[1].split("/")
                    global temp1
                    temp1 = temp[1]
                    if len(data[2]) >= 3:
                        temp = data[2].split(":")
                        global tempBed
                        tempBed = temp[1]
                    global socketio
                    #print("usb[TEMP]\t1 = " + temp0 +
                    #      "C°\t2 = " + temp1 +
                    #      "C°\tp = " + tempBed + "C°")
                    socketio.emit('temp', temp0 + '/' + temp1 + '/' + tempBed, broadcast= True)
            else:
                print("usb[EVENT]" + txt)
                pass

    def lancement(self):
        global gcode
        global info
        global ser
        global stopAll
        global startPrint
        global posPrint
        global fPrint
        global tempPrintFolder
        global countOut
        global countIn
        endLine = 0
        oldLine = None

        line = ""
        time.sleep(2)
        gcode.append("M155 S1\n")

        while stopAll == 0:
            time.sleep(1/120)
            try:
                posL = ser.inWaiting()
                if posL > 0:
                    if oldLine != None:
                        #print("pass2:", oldLine)
                        line = oldLine + ser.read(posL)
                        #print("pass3:", line)
                    else:
                        line = ser.read(posL)
                    posL = len(line)
                    #time.sleep(1)
                    #posEnd = posL
                    #print(line)
                    if len(line) != 0:
                        if line[posL -1] == 10:
                            oldLine = None
                        else:
                            oldLine = line
                            line = ""
            except:
                print("usb[ERROR] read serial")
                line = ""
                oldLine = None
                self.search()
                #permet de reprendre l'inpression en cour
                time.sleep(2)
                gcode.insert(0, 'M114')
                countOut = 0
                countIn = 0
                gcode.append("M155 S1\n")
            else:
                #lit ce que la carte a envoyer 
                if len(line) != 0:
                    line = str(line, 'utf-8')
                    txt = line.splitlines()
                    line = ""
                    a = 0
                    #countIn += 1
                    while a < len(txt):
                        usb.analyseGcode(txt[a])
                        a += 1
                #ajoute le code du fichier a imprimer dans la liste d'envoi
                if startPrint == 1:
                    if (countOut - countIn) <= 2  :
                        tempLine = fPrint.readline()
                        if len(tempLine) == 0:
                            startPrint = 0
                            print("print[EVENT]impression terminer")
                            tempPrintFolder.close()
                            os.remove(".restart.txt")
                        else:
                            posTempLine = len(tempLine)
                            a = 0
                            #while pos
                            if tempLine[0] != ';' and tempLine[0] != ' ' and tempLine[0] != '\n':
                                #print(tempLine)
                                #print(posPrint) # position dans le fichier 
                                gcode.append(tempLine)
                            else:
                                #print(tempLine)
                                #print(posPrint)
                                pass
                            print("dev[_var_] posPrint :" + str(posPrint))
                            tempPrintFolder = open('.restart.txt', 'a')
                            tempPrintFolder.write(str(posPrint) + "\n")
                            tempPrintFolder.close()
                            posPrint += 1
                #envoi le gcode a la carte
                if len(gcode) > 0:
                    print("usb[WRITE] " + gcode[0][:len(gcode[0])-1])
                    try:
                        #print("I/O:" + str(countIn) + "/" + str(countOut))
                        ser.write(gcode[0].encode('utf-8'))
                        countOut += 1
                    except:
                        print("usb[ERROR] carte déconnecter")
                        #print("I/O:" + str(countIn) + "/" + str(countOut))
                        self.search()
                        #permet de reprendre l'impression en cour
                        time.sleep(2)
                        gcode.insert(0, 'M114')
                        countOut = 0
                        countIn = 0
                        #print("I/O:" + str(countIn) + "/" + str(countOut))

                    else:
                        del gcode[0]
        print("usb[EVENT] usb stop")
        sys.exit('usb[EVENT] usb stop')
        os._exit('0')

    #lancement du module usb
    def run(self):
        self.search()
        self.lancement()

#lancement et gestion serveur web
from flask import Flask, request
from flask_socketio import SocketIO, send, emit
from werkzeug.utils import secure_filename
class web(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        global socketio
        global gcode
        
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
                print("test:", data[0:3]) 
                if data[0:3] == 'SYS':
                    dataCut = data.split()
                    print("test2:", dataCut)
                    if dataCut[0] == 'SYS0':
                        print('web[EVENT] start Cut of the launched software')
                        global stopAll
                        stopAll = 1
                        f.destroy()
                        print('win[EVENT] widows stop')
                        socketio.stop()
                        #print('web[EVENT] web stop')
                        sys.exit('web[EVENT] web stop')
                        os._exit('0')
                else:
                    gcode.append(data + '\n')
            else:
                print("web[WARNING] received empty gcode")
        #permet de lancer une impression
        @socketio.on('print')
        def runprint(data):
            global fPrint
            global startPrint
            global posPrint
            if startPrint != 0:
                fPrint.close()
                tempPrintFolder.close()
                startPrint = 0
            posPrint = 0
            try:
                fPrint = open(data, "r")
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
                global pathPrint
                global countOut
                global countIn
                pathPrint = data
                startPrint = 1
                countOut = 0
                countIn = 0
                print("web[EVENT] start print")
                socketio.emit('startPrint', data, broadcast= True)
        socketio.run(app, host='0.0.0.0', port= '8080')

#lance les thread
def startAll():
    thread1 = window()
    thread1.start()

    thread2 = usb()
    thread2.start()

    thread3 = web()
    thread3.start()

#test mise a jour
import git

git.Git().pull()

#mise a jour
import requests
try:
    r = requests.get( urlSer + '/version', timeout=1)
    resp = r.text
except:
    print("web[EVENT] update imposible")
    startAll()
    pass
else:
    try:
        serSoftVer = float(resp)
        print("install version : " + str(serSoftVer))
        print("newest version : " + str(version))
    except:
        print('web[ERROR] wrong number maj')
        startAll()
    else:
        if version < serSoftVer:
            print('web[EVENT] dowload the newest version')
            try:
                r = requests.get(urlSer + '/version/download')
            except:
                print('web[EVENT] dowload the newest version')
                startAll()
            else:
                uploadFile = open("main.py",'w')
                uploadFile.write(r.text)
                uploadFile.close()
                os.system('python3 main.py')
        else:
            print ('sys[event] already in the newest version')
            startAll()
