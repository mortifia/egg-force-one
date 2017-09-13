# -*- coding: utf-8 -*-
#!/usr/bin/python3
from threading import Thread

#lancement de l'interface graphique

class window(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)

    def initialisation(self):
        """
            lancement de l'interface graphique 
        """
        import sys
        from PyQt5.QtCore import QUrl
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtQuick import QQuickView

        myApp = QApplication(sys.argv)
        appLabel = QQuickView()
        appLabel.setSource(QUrl('main.qml'))
        appLabel.show()
        myApp.exec_()
        sys.exit()

    def run(self):
        self.initialisation()