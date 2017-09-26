# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 16:05:05 2017

@author: 54386
"""

#import externe
import os
import sys
from threading import Thread

os.chdir(os.path.dirname(os.path.realpath(__file__))) # nous place dans le dossier de l'executable
#print(os.path.dirname(os.path.realpath(__file__)))

class usb(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)
        pass
    def run(self):        
        pass
    
    pass
