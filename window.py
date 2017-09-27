# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""
#import externe
import os
import sys
from threading import Thread

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

#lancement de l'interface graphique

class Window(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass

    def initialisation(self):
        """
            lancement de l'interface graphique
        """
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtQuick import QQuickView

        myApp = QApplication(sys.argv)
        appLabel = QQuickView()
        appLabel.setSource(QUrl('main.qml'))
        appLabel.setGeometry(0, 0, 480, 800)
        if (len(sys.argv) > 1):
            if (sys.argv[1] == "-nw"):
                appLabel.setFlags(Qt.FramelessWindowHint)
                pass
            pass
        appLabel.show()
        myApp.exec_()
        sys.exit()
        pass

    def run(self):
        self.initialisation()
        pass
    pass

if __name__ == "__main__":
    pass