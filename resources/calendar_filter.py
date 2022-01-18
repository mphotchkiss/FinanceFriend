from tkinter import Label


from tkinter import *
import tkcalendar

class CalendarFilter:
    def __init__(self, title, label):
        self.frame = Toplevel()
        self.frame.title(title)
        Label(self.frame, text=label).grid(row=0,column=0)
        self.cal = tkcalendar.Calendar(self.frame, selectmode='day', date_pattern="MM/dd/yyyy")
        self.cal.grid(row=1,column=0)