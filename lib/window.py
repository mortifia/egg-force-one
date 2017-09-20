# -*- coding: utf-8 -*-
#!/usr/bin/python3
"""
Created on Sat Sep 16 01:15:39 2017

@author: mortifia
"""
import os

os.chdir(os.path.dirname(os.path.realpath(__file__)))
#print(os.path.dirname(os.path.realpath(__file__)))

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
        from PyQt5.QtCore import QUrl, Qt
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtQuick import QQuickView

        myApp = QApplication(sys.argv)
        appLabel = QQuickView()
        appLabel.setSource(QUrl('main.qml'))
        appLabel.setGeometry(0, 0, 480, 800)
        appLabel.setFlags(Qt.FramelessWindowHint)
        appLabel.show()
        myApp.exec_()
        sys.exit()

    def run(self):
        self.initialisation()