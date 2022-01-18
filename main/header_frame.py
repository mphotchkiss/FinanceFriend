from tkinter import *

class HeaderFrame:
    def __init__(self, root, height, width, border, color):
        self.frame = Frame(root, height=height, width=width, borderwidth=border, bg=color)
        
        #add the header label
        self.app_header_lbl = Label(self.frame, text="Finance Friend - a money management tool for students")
        self.app_header_lbl.grid(row=0, column=0, columnspan=10)

        self.frame.pack(fill=X)