from tkinter import *
from main import dash_frame
from main import upload_frame
from main import manage_frame
from db import connection

class MainFrame:
    def __init__(self, db, root, height, width, border, color):
        self.frame = Frame(root, height=height, width=width, borderwidth=border, bg=color)
        self.frame.pack(expand=TRUE, fill=BOTH)
        
        self.database_connection = connection.Connection(db)

        self.dash_frame = dash_frame.DashFrame(self.frame, self.database_connection)
        self.upload_frame = upload_frame.UploadFrame(self.frame, self.database_connection)
        self.manage_frame = manage_frame.ManageFrame(self.frame, self.database_connection)

        self.load_dash_frame()

    def load_dash_frame(self):
        self.dash_frame.render_dash_frame()

    def load_upload_frame(self):
        self.upload_frame.render_upload_frame()

    def load_manage_frame(self):
        self.manage_frame.render_manage_frame()

    

    
        
