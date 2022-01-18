from tkinter import *

class ContentFrame:
    def __init__(self, parent, r, c):
        self.frame = Frame(parent)
        self.r = r
        self.c = c

    def grid(self):
        self.frame.grid(row=self.r, column=self.c)

    def clear(self):
        for widget in self.frame.winfo_children():
            widget.destroy()    
    


