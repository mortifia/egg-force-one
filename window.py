# -*- coding: utf-8 -*-
#!/usr/bin/python3
from threading import Thread

#lancement de l'interface graphique

class window(Thread):
    def __init__(self, sysVar):
        self.sysVar = sysVar
        Thread.__init__(self)

    def lineInfo(self):
        from tkinter import Button, PhotoImage

        f = self.sysVar.f

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

        f = self.sysVar.f

        self.clean()
        self.sysVar.fPath = 'control'

        self.lineInfo()
        
        self.controlButton0 = Button(f, text = "X+")
        self.controlButton0.place(x=50,y=100)
        self.controlButton1 = Button(f, text = "X-")
        self.controlButton1.place(x=100,y=100)
        self.controlButton2 = Button(f, text = "Y+")
        self.controlButton2.place(x=50,y=150)
        self.controlButton3 = Button(f, text = "Y-")
        self.controlButton3.place(x=100,y=150)
        self.controlButton4 = Button(f, text = "Z+")
        self.controlButton4.place(x=50,y=200)
        self.controlButton5 = Button(f, text = "Z-")
        self.controlButton5.place(x=100,y=200)

    def option(self):
        from tkinter import Button, PhotoImage

        f = self.sysVar.f

        self.clean()
        self.sysVar.fPath = 'option'

        self.lineInfo()

        self.optionButton0 = Button(f, text = 'wifi', 
            font = (None, 18), 
            height = 1, width = 28)
        self.optionButton0.place(x = 15, y = 80)


    def home(self):
        from tkinter import Button, PhotoImage

        f = self.sysVar.f

        self.clean()
        self.sysVar.fPath = 'home'

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
        print("win[EVENT] Start clean")
        temp = self.sysVar.fPath.split("/")
        print(temp[0])
        if temp[0] == 'home':
            self.homeButton0.destroy()
            self.homeButton1.destroy()
        if temp[0] == 'option':
            self.optionButton0.destroy()
        if temp[0] == 'control':
            self.controlButton0.destroy()
            self.controlButton1.destroy()
            self.controlButton2.destroy()
            self.controlButton3.destroy()
            self.controlButton4.destroy()
            self.controlButton5.destroy()

    def initialisation(self):
        from tkinter import Tk
        
        self.sysVar.f = Tk()
        f = self.sysVar.f
        f.geometry('480x800+0+0')
        f.overrideredirect(1)
        self.lineHome = 0
        self.home()
        f.mainloop()
        sys.exit('win[EVENT] widows stop')
        os._exit('0')

    def run(self):
        self.initialisation()