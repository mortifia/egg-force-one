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
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

# lancement de l'interface graphique
class Window(Thread, QObject):
    def __init__(self, sysVar, parent=None):
        self.sysVar = sysVar
        super().__init__(parent)
        Thread.__init__(self)
        pass
    
    def initialisation(self):
        self.app = QApplication(sys.argv)
        self.engine = QQmlApplicationEngine()
        self.engine.quit.connect(self.app.quit)
        
        # definit les variable controller par l'exterieur
        self.engine.rootContext().setContextProperty("test", "ouiiiiii")        
        self.engine.load("main.qml")
        self.app.exec_()
        pass

    def run(self):
        self.initialisation()
        pass
    pass

if __name__ == "__main__":
    pass