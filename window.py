# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#import externe
import os
import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class getVar(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.engine = False
        pass

    @pyqtSlot(result = str)
    def test(self):
        print("getVar : test")
        return "sucess(getvar)"

# lancement de l'interface graphique
class Window(Thread):
    def __init__(self, sysVar, parent=None):
        self.sysVar = sysVar
        super().__init__(parent)
        Thread.__init__(self)
        pass

######################################
#   fonction externe
###############################
    def updateTemp(self):
        print("updateTemp #################")
        if (self.engine != False):
            self.engine.rootContext().setContextProperty("test", self.sysVar.temp)
            #self.engine.rootContext().text1.text = "test"
            pass
        pass
#######################################
#   ne pas toucher
##############################################

    def initialisation(self):
        app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.engine.quit.connect(app.quit)

        self.engine.load("main.qml")

        # definit les variable controller par l'exterieur
        self.engine.rootContext().setContextProperty("test", ['test1', 'test2'])

        # envoie la variable demander
        self.engine.rootContext().setContextProperty("getVar", getVar())

        app.exec_()
        pass

    def run(self):
        self.initialisation()
        pass
    pass

if __name__ == "__main__":
    pass