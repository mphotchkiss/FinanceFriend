from tkinter import *
import main.header_frame as header_frame
import main.main_frame as main_frame
from resources import root_frame

class Finance_App:
    def __init__(self):
        self.root = root_frame.RootFrame("Finance Friend")

        #create permanent navigation frame for the application links
        self.navigation_frame = Frame(self.root.root, height=self.root.height, width=50, borderwidth=1, bg="GREEN")
        self.render_navigation()

        #create permanent header frame for the application title and such
        self.header_frame = header_frame.HeaderFrame(self.root.root, 50, self.root.width-50, 1, "RED")

        #create the main frame that'll display the different pages
        self.main_frame = main_frame.MainFrame("db/transaction_cache2.db", self.root.root, self.root.height-50, self.root.width-50, 1, "BLUE")

        self.root.root.mainloop()

    def render_navigation(self):
        #add the navigation buttons
        dash_btn = Button(self.navigation_frame, text="Dashboard", command=self.load_dash_frame)
        dash_btn.grid(row=0,column=0)
        upload_btn = Button(self.navigation_frame, text="Upload Records", command=self.load_upload_frame)
        upload_btn.grid(row=1,column=0)
        manage_btn =  Button(self.navigation_frame, text="Manage Records", command=self.load_manage_frame)
        manage_btn.grid(row=2,column=0)

        self.navigation_frame.pack(fill=Y, side=RIGHT)

    def load_dash_frame(self):
        self.main_frame.load_dash_frame()

    def load_upload_frame(self):
        self.main_frame.load_upload_frame()

    def load_manage_frame(self):
        self.main_frame.load_manage_frame()

    