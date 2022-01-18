from tkinter import *

class RootFrame:
    def __init__(self, name):
        self.root = Tk()
        
        #grab the screen width and height
        self.width=self.root.winfo_screenwidth()
        self.height=self.root.winfo_screenheight()

        if not self.width or not self.height:
            print("Aborting root frame. Width and height error")
            self.root.destroy()

        #fill screen and add title
        self.root.geometry("%dx%d" % (self.width,self.height))
        self.root.title(name)