import tkinter
import pygame as pg
from pygame.locals import *
from tkinter.constants import *

class Tile:

    def __init__(self,answer,i,j,window):
        self.answer = answer
        self.guess = ""
        self.i = i
        self.j = j
        self.window = window
        photo = tkinter.PhotoImage(master=self.window,file='Letters/Blank.gif')
        label = tkinter.Label(master=self.window,image=photo)
        label.image = photo
        self.button = tkinter.Button(
            master=self.window,
            command=self.change_tile,
            image=photo
        )
        pg.init()

    def change_tile(self):
        event = pg.event.wait()
        if ((event.type == KEYDOWN) or (event.type == KEYUP)):
            key = pg.key.name(event.key)
            try:
                photo_url = 'Letters/'
                if key == 'space':
                    self.guess = ""
                    photo_url += 'Blank.gif'
                else:
                    filename = key.upper()+'.gif'
                    photo_url += filename
                    self.guess = key.upper()
                photo = tkinter.PhotoImage(master=self.window,file=photo_url)
                label = tkinter.Label(master=self.window,image=photo)
                label.image = photo
                self.button.config(image=photo)
            except tkinter.TclError:
                pass


    def mark_correct(self):
        if (self.guess != ""):
            photo = tkinter.PhotoImage(master=self.window,file="Letters/Correct/"+self.guess+'.gif')
            label = tkinter.Label(master=self.window,image=photo)
            label.image = photo
            self.button.config(image=photo)

    def lay_down_tile(self):
        self.button.grid(row=self.i+1,column=self.j+1)

    def check(self):
        if (self.guess != ""):
            return (self.guess==self.answer)
        else:
            return True
