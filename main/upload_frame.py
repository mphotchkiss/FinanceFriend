from tkinter import *
import tkcalendar
from data.selections import months, years, days, options, options2, months2, years2
import resources.ofx_parser as ofx_parser
from tkinter import messagebox
import resources.categorizer as categorizer
from db import connection
from tkinter import filedialog
from datetime import date
from resources import content_frame

class UploadFrame:
    def __init__(self, main_frame, db):
        self.frame = main_frame

        self.file_path = None
        self.clicked = list()
        self.selection = list()
        self.confirmation_window = None
        self.confirm_frame = None
        self.next_step_btn = None
        self.confirm_multiplier = 1

        self.categorizer = categorizer.Categorizer()
        self.connection = db

        self.dir_entry_cal = None
        self.direct_name_entry = None
        self.direct_value_entry = None
        self.direct_cat_entry_var = None

    def render_upload_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.dir_entry_cal = tkcalendar.Calendar(self.frame, selectmode = 'day', date_pattern="MM/dd/yyyy")
        self.direct_name_entry = Entry(self.frame)
        self.direct_value_entry = Entry(self.frame)
        self.direct_cat_entry_var = StringVar()

        selection_lbl = Label(self.frame, text="Upload:")
        selection_lbl.grid(row=0,column=0)
        
        select_file_btn = Button(self.frame, text="Select File", command=self.pick_file)
        select_file_btn.grid(row=0,column=1)
        file_submit_btn = Button(self.frame, text="Submit File", command=self.categorize_transactions)
        file_submit_btn.grid(row=1,column=0)
        
        #create labels and entries for direct submission
        direct_submit_lbl = Label(self.frame, text="Direct Submission form")
        direct_submit_lbl.grid(row=0,column=2)

        self.dir_entry_cal.grid(row=1,column=2)
        
        self.direct_name_entry.grid(row=2,column=2)
        
        self.direct_value_entry.grid(row=3,column=2)
        
        self.direct_cat_entry_var.set("Food")
        direct_cat_entry = OptionMenu(self.frame, self.direct_cat_entry_var, *options)
        direct_cat_entry.grid(row=4,column=2)

        #create submit button
        direct_sub_btn = Button(self.frame, text="Submit", command=self.direct_submission)
        direct_sub_btn.grid(row=5,column=2)

    #user has submitted the image, which will now be processed and categorized
    def categorize_transactions(self):
        
        #process the ofx_data
        parser = ofx_parser.OFX_Parser(self.file_path)
        parser.parse() 
        response = messagebox.showinfo("Submission recieved!", "Processing the bank data may take a couple minutes. Please stand by. You will be alerted when the process is complete.")

        #categorize the data
        self.categorizer.extract_data(parser) #dates, names, value, category
        
        response = messagebox.showinfo("Processing complete!", "You are now ready to proceed with the confirmation process.")
        
        #add check category button
        self.next_step_btn = Button(self.frame, text="Check Categorization", command=self.open_confirmation_window)
        self.next_step_btn.grid(row=2,column=0,columnspan=2)

    #user has proceeded to confirmation process. Display new window with drop-down menus
    def open_confirmation_window(self):
        #open new window
        self.confirmation_window = Toplevel()
        self.confirmation_window.title("Category Confirmation")
        self.render_confirmation_window()
    
    def render_confirmation_window(self):

        for widget in self.confirmation_window.winfo_children():
            widget.destroy()

        self.confirm_frame = content_frame.ContentFrame(self.confirmation_window, 0, 0)
        self.confirm_frame.grid()

        submit_frame = content_frame.ContentFrame(self.confirmation_window, 1, 0)
        submit_frame.grid()

        backend = 0
        if (10*self.confirm_multiplier <= len(self.categorizer.category)):
            backend = 10*self.confirm_multiplier
        else:
            backend = len(self.categorizer.category)

        for i in range(10*(self.confirm_multiplier-1), backend):
            #create an init var
            click = StringVar()
            self.clicked.append(click)

            #initialize the field to the auto-determined category
            self.clicked[i].set(self.categorizer.category[i])
    
            #display date for testing
            raw_date = self.categorizer.dates[i]
            data = raw_date.split("-")
            year = data[0]
            month = data[1]
            day = data[2]
            date = month + "-" + day + "-" + year
            date_lbl = Label(self.confirm_frame.frame, text=date)
            date_lbl.grid(row=i,column=0)

            name = self.categorizer.names[i]

            #display names and value of transactions
            name_lbl = Label(self.confirm_frame.frame, text=name)
            name_lbl.grid(row=i,column=1)

            value_lbl = Label(self.confirm_frame.frame, text=str(-1*self.categorizer.values[i]))
            value_lbl.grid(row=i, column=2)

            #create dropdown with choices of options
            select = OptionMenu(self.confirm_frame.frame, self.clicked[i], *options)
            select.grid(row = i, column = 3)
            
            #store select object in the array of drop downs (so we can access value at the end
            self.selection.append(select)

        #add submit button to push into database
        if (10*self.confirm_multiplier >= len(self.categorizer.category)):
            cat_submit_btn = Button(submit_frame.frame, text="Submit Categories", command=self.submit_categories)
            cat_submit_btn.grid(row=0,column=0, sticky=S)
        else:
            cat_next_btn = Button(submit_frame.frame, text="Next", command=self.next_categories)
            cat_next_btn.grid(row=0,column=0,sticky=S)
        cat_cancel_btn = Button(submit_frame.frame, text = "Cancel", command = self.refresh)
        cat_cancel_btn.grid(row=0, column=1, sticky=S)

    #user selects a file, and stores file path in global var file_path
    def pick_file(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a file")
        self.file_path = filename

    #pass the insertion to the database, send a success message, and clear the form
    def direct_submission(self):
        #connect to DB
        print("Connecting to db")
        self.connection.connect()
        
        #parse the date into pieces
        date_s = self.dir_entry_cal.get_date()
        comps = date_s.split("/")
        month = comps[0]
        day = comps[1]
        year = comps[2]
        print("Date:", month, "/", day, "/", year)

        #insert the transaction into the database
        self.connection.execute("INSERT INTO transactions VALUES (:day, :month, :year, :name, :value, :category)",{
            'day': day,
            'month': month,
            'year': year,
            'name': self.direct_name_entry.get(),
            'value': float(self.direct_value_entry.get()),
            'category': self.direct_cat_entry_var.get()
        })
        print("Execution complete")

        #commit and close
        self.connection.disconnect()
        print("Connection closed")

        #clear the form
        self.dir_entry_cal.selection_set(date.today())
        self.direct_name_entry.insert(0,"")
        self.direct_value_entry.insert(0,"")
        self.direct_cat_entry_var.set("Food")

        #alert the user of success
        response = messagebox.showinfo("Direct Submission Recieved", "Your direct submission has been recieved and processed. Thank you.")

        #reload frame
        self.refresh()

    def next_categories(self):
        self.confirm_multiplier = self.confirm_multiplier + 1
        self.render_confirmation_window()
    
    def submit_categories(self):
        #connect to DB
        self.connection.connect()
    
        #insert all the elements into the DB
        for i, name in enumerate(self.categorizer.names):
            #split up the date
            date_split = self.categorizer.dates[i].split("-")
            day = date_split[2]
            month = date_split[1]
            year = date_split[0]
                        
            self.connection.execute("INSERT INTO transactions VALUES (:day, :month, :year, :name, :value, :category)",{
                'day': day,
                'month': month,
                'year': year,
                'name': name,
                'value': float(-1*self.categorizer.values[i]),
                'category': self.clicked[i].get()
            })
        
        #commit changes and close DB connection
        self.connection.disconnect()
        
        #close the window
        self.confirmation_window.destroy()

    def refresh(self):
        self.file_path = None

        #delete the confirmation-related items
        if self.confirmation_window:
            self.confirmation_window.destroy()
        if self.next_step_btn:
            self.next_step_btn.destroy()
        
        #create a new categorizer
        self.categorizer = categorizer.Categorizer()
        self.clicked = list()
        self.selection = list()
        
        #clear the form
        self.dir_entry_cal.selection_set(date.today())
        self.direct_name_entry.insert(0,"")
        self.direct_value_entry.insert(0,"")
        self.direct_cat_entry_var.set("Food")

        self.render_upload_frame()