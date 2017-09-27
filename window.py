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

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

#lancement de l'interface graphique

class Window(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass
    def initialisation(self):
        app = QApplication(sys.argv)
        engine = QQmlApplicationEngine()
        engine.quit.connect(app.quit)
        engine.load("main.qml")
        app.exec_()
        pass

    def run(self):
        self.initialisation()
        pass
    pass

if __name__ == "__main__":
    pass