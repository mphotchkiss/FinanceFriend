from tkinter import *
from db import connection
from PIL import ImageTk,Image
from data.selections import months, years, days, options, options2, months2, years2
from tkinter import messagebox
import tkcalendar
import resources.calendar_filter as calendar_filter
from resources import content_frame

class ManageFrame:
    def __init__(self, main_frame, db):
        self.frame = main_frame
        self.records_frame = None
        self.filter_frame = None

        self.edit_btn_img = ImageTk.PhotoImage(Image.open("images/edit.png"))
        self.delete_btn_img = ImageTk.PhotoImage(Image.open("images/delete.png"))

        self.connection = db

        self.filter_btn = None

        self.edit_entry_cal = None
        self.edit_window = None

        self.index = 0

        self.page_multiplier = 1
        self.to_print = None

        self.from_date_filter_temp = ""
        self.to_date_filter_temp = ""
        self.from_date_filter = "Select"
        self.to_date_filter = "Select"
        self.name_manage_filter_var = ""
        self.val_manage_filter_var = ""

        self.cat_manage_filter_var=StringVar()
        self.mng_filter_from_btn_var = StringVar()
        self.mng_filter_to_btn_var = StringVar()
        self.cat_manage_filter_var.set("Select")

    def render_manage_frame(self):

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.filter_frame = content_frame.ContentFrame(self.frame, 0, 0)
        self.filter_frame.grid()

        self.records_frame = content_frame.ContentFrame(self.frame, 1, 0)
        self.records_frame.grid()

        self.mng_filter_from_btn_var.set("From: " + self.from_date_filter)
        self.mng_filter_to_btn_var.set("To: " + self.to_date_filter)
        Button(self.filter_frame.frame, textvariable=self.mng_filter_from_btn_var, command=self.filter_manage_from_window).grid(row=0,column=0)
        Button(self.filter_frame.frame, textvariable=self.mng_filter_to_btn_var, command=self.filter_manage_to_window).grid(row=0,column=1)

        #create a filter for the name
        name_manage_filter = Entry(self.filter_frame.frame)
        name_manage_filter.grid(row=0,column=2)
        name_manage_filter.insert(0, self.name_manage_filter_var)

        #create a filter for the value/price
        val_manage_filter = Entry(self.filter_frame.frame)
        val_manage_filter.grid(row=0,column=3)
        val_manage_filter.insert(0, self.val_manage_filter_var)
            
        #create a filter for the category
        cat_manage_filter = OptionMenu(self.filter_frame.frame, self.cat_manage_filter_var, *options2)
        cat_manage_filter.grid(row=0,column=4)

        #create filter button
        filter_btn = Button(self.filter_frame.frame, text="Filter", command=lambda: self.enforce_mng_filter(name_manage_filter, val_manage_filter))
        filter_btn.grid(row=0,column=5)

        #create clear filter button
        clear_mng_filter_btn = Button(self.filter_frame.frame, text="Clear", command=self.clear_manage_filter)
        clear_mng_filter_btn.grid(row=0,column=6)

        #create column labels
        col_date_lbl = Label(self.filter_frame.frame, text="Date")
        col_date_lbl.grid(row=1,column=0)
        col_blank_lbl = Label(self.filter_frame.frame, text="    ")
        col_blank_lbl.grid(row=1,column=1)
        col_name_lbl = Label(self.filter_frame.frame, text="Name")
        col_name_lbl.grid(row=1,column=2)
        col_val_lbl = Label(self.filter_frame.frame, text="Value")
        col_val_lbl.grid(row=1,column=3)
        col_cat_lbl = Label(self.filter_frame.frame, text="Category")
        col_cat_lbl.grid(row=1,column=4)

        #open database
        self.connection.connect()
        
        #get all transactions in our database
        self.connection.c.execute("SELECT *, oid FROM transactions")

        #print all the transactions and their buttons
        records = self.connection.c.fetchall()

        #commit changes and close DB connection
        self.connection.disconnect()

        #initialize an empty list of records that we want to print
        self.to_print = list()

        #for each record we have, we want to filter them with our filters
        for record in records:
            print_this_one = TRUE
            record_date = int(record[2]+record[1]+record[0])

            #perform checks on our filters
            if (self.name_manage_filter_var != ""):
                print_this_one = print_this_one and self.name_manage_filter_var.lower() in str(record[3].lower())
                    
            if (self.val_manage_filter_var != ""):
                print_this_one = print_this_one and float(self.val_manage_filter_var) < float(record[4])
                    
            if (self.cat_manage_filter_var.get() != "Select"):
                print_this_one = print_this_one and self.cat_manage_filter_var.get() == record[5]
                    
            if (self.from_date_filter != "Select"):
                #get the dates in a comparison format
                from_date_split = self.from_date_filter.split('/')
                from_date = int(from_date_split[2] + from_date_split[0] + from_date_split[1])
                print_this_one = print_this_one and from_date <= record_date
                    
            if (self.to_date_filter != "Select"):
                #get the dates in a comparison format
                to_date_split = self.to_date_filter.split('/')
                to_date = int(to_date_split[2] + to_date_split[0] + to_date_split[1])
                print_this_one = print_this_one and to_date >= record_date
                    
            if (print_this_one):
                self.to_print.append(record)

        self.display_records()

    def display_records(self):
        #clear the frame
        self.records_frame.clear()

        row_val = 0
        backend = 0
        if (20*self.page_multiplier <= len(self.to_print)):
            backend = 20*self.page_multiplier
        else:
            backend = len(self.to_print)
        #for 20 records starting from our last index
        for i in range(0 + 20*(self.page_multiplier-1), backend):
            #grab our record we want to print
            record = self.to_print[i]

            #grab the 3 field values
            print_day = str(record[0])
            print_month = str(record[1])
            print_year = str(record[2])
            print_name= str(record[3])
            print_value = str(record[4])
            print_category = str(record[5])
                        
            #load the labels for all 3 in
            date_lbl = Label(self.records_frame.frame, text=print_month + "-" + print_day + "-" + print_year)
            date_lbl.grid(row=row_val,column=0)
            space_lbl = Label(self.records_frame.frame, text="    ")
            space_lbl.grid(row=row_val, column=1)
            name_lbl = Label(self.records_frame.frame, text=print_name)
            name_lbl.grid(row=row_val,column=2)
            value_lbl = Label(self.records_frame.frame, text="$" + print_value)
            value_lbl.grid(row=row_val,column=3)
            cat_lbl = Label(self.records_frame.frame, text=print_category)
            cat_lbl.grid(row=row_val,column=4)
                
            #create the delete and edit buttons
            delete_btn = Button(self.records_frame.frame, image=self.delete_btn_img, command=lambda oid=int(record[6]): self.delete_record(oid))
            delete_btn.grid(row=row_val,column=5)
            edit_btn = Button(self.records_frame.frame, image=self.edit_btn_img, command=lambda oid=int(record[6]): self.edit_record(oid))
            edit_btn.grid(row=row_val,column=6)
                        
            row_val = row_val + 1
        
        #navigation buttons - make sure we disable them when it's not possible
        next_mng_btn = Button(self.records_frame.frame, text="Next", command=self.next_page_mng)
        prev_mng_btn = Button(self.records_frame.frame, text="Prev", command=self.prev_page_mng)
        prev_mng_btn.grid(row=22, column=5) 
        next_mng_btn.grid(row=22, column=6)
    
        if (self.page_multiplier*20 >= len(self.to_print)):
            next_mng_btn.configure(state='disabled')
        if (self.page_multiplier == 1):
            prev_mng_btn.configure(state='disabled')

    def delete_record(self, oid):
        #connect to DB
        self.connection.connect()
        
        #grab the name of the transaction and value to display on question messagebox
        self.connection.execute("SELECT * FROM transactions WHERE oid=(:oid)",{
                'oid': oid
        })
        records=self.connection.c.fetchall()
        record = ''
        record = str(records[0][3]) + " for $" + str(records[0][4]) + " on " + str(records[0][0]) + "-" + str(records[0][1]) + "-" + str(records[0][2])

        #prompt user to confirm deletion
        response = messagebox.askyesno("Delete Confirmation", "Are you sure you wish to delete the transaction: " + record + "?")
        if (response == 0):
            #commit and close DB
            self.connection.disconnect()
            return

        #delete the record with id oid
        self.connection.execute("DELETE FROM transactions WHERE oid=(:oid)",{
                'oid': oid
        })

        #commit and close DB
        self.connection.disconnect()

        self.render_manage_frame()

    def update_record(self, oid, d, n, v, c):
        #get the values
        date_s = d
        comps = date_s.split("/")
        month = comps[0]
        day = comps[1]
        year = comps[2]
        name = n
        value = v
        category = c
        
        #clear the edit frame
        self.edit_window.destroy()

        #update the database for oid
        self.connection.connect()
        self.connection.execute("""UPDATE transactions SET
            day = :day,
            month = :month,
            year = :year,
            name = :name,
            value = :value,
            category = :category

            WHERE oid = :oid""", {
                'day': day,
                'month': month,
                'year': year,
                'name': name,
                'value': float(value),
                'category': category,
                'oid': oid
            }
        )
        
        #commit and close
        self.connection.disconnect()

        #reload the manage frame
        self.render_manage_frame()
    
    #edit the record with oid
    def edit_record(self, oid):
        #open new window for edits
        self.edit_window = Toplevel()
        self.edit_window.title("Edit Transaction")
        
        #open database
        self.connection.connect()
    
        #collect the current information on the transaction
        self.connection.execute("SELECT *, oid FROM transactions WHERE oid=(:oid)", {
            'oid': oid
        })
        records=self.connection.c.fetchall()
        day = int(records[0][0])
        month = int(records[0][1])
        year = int(records[0][2])
        name = str(records[0][3])
        value = str(records[0][4])
        category = str(records[0][5])

        #render in entries for all 3 fields with values preset to current values
        edit_entry_cal = tkcalendar.Calendar(self.edit_window, selectmode='day', day=day, month=month, year=year, date_pattern="MM/dd/yyyy")
        edit_entry_cal.grid(row=0,column=0)

        name_entry = Entry(self.edit_window)
        name_entry.insert(0,name)
        name_entry.grid(row=1,column=0)

        value_entry = Entry(self.edit_window)
        value_entry.insert(0,value)
        value_entry.grid(row=2,column=0)

        cat_entry_var = StringVar()
        cat_entry_var.set(category)
        cat_entry = OptionMenu(self.edit_window, cat_entry_var, *options)
        cat_entry.grid(row=3,column=0)

        update_btn = Button(self.edit_window, text="Update", command=lambda: self.update_record(oid, edit_entry_cal.get_date(), name_entry.get(), value_entry.get(), cat_entry_var.get()))
        update_btn.grid(row=4,column=0)

        #commit and close
        self.connection.disconnect()

    def filter_manage_from_window(self):
        cal = calendar_filter.CalendarFilter("Filter Manage Date: From", "From")
        submit_mng_filter_btn = Button(cal.frame, text="Submit", command=lambda: self.set_mng_date_from(cal))
        submit_mng_filter_btn.grid(row=2,column=0)

    def filter_manage_to_window(self):
        cal = calendar_filter.CalendarFilter("Filter Manage Date: To", "To")
        submit_mng_filter_btn = Button(cal.frame, text="Submit", command=lambda: self.set_mng_date_to(cal))
        submit_mng_filter_btn.grid(row=2,column=0)

    def enforce_mng_filter(self, name_filter, val_filter):
        self.name_manage_filter_var = name_filter.get()
        self.val_manage_filter_var = val_filter.get()
        if (self.from_date_filter_temp != ""):
            self.from_date_filter = self.from_date_filter_temp
        if (self.to_date_filter_temp != ""):
            self.to_date_filter = self.to_date_filter_temp
        self.render_manage_frame()

    def set_mng_date_from(self, cal):
        self.from_date_filter_temp = cal.cal.get_date()
        self.mng_filter_from_btn_var.set("From: " + self.from_date_filter_temp)
        cal.frame.destroy()

    def set_mng_date_to(self, cal):
        self.to_date_filter_temp = cal.cal.get_date()
        self.mng_filter_to_btn_var.set("To: " + self.to_date_filter_temp)
        cal.frame.destroy()

    def next_page_mng(self):
        self.page_multiplier = self.page_multiplier + 1
        self.display_records()
        
    def prev_page_mng(self):
        self.page_multiplier = self.page_multiplier - 1
        self.display_records()

    def clear_manage_filter(self):
        self.index = 0
        self.page_multiplier = 1
        self.from_date_filter_temp = ""
        self.to_date_filter_temp = ""
        self.from_date_filter = "Select"
        self.to_date_filter = "Select"
        self.name_manage_filter_var = ""
        self.val_manage_filter_var = ""
        self.cat_manage_filter_var.set("Select")
        self.render_manage_frame()

        
    
