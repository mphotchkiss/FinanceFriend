from tkinter import *
import resources.calendar_filter as calendar_filter
from datetime import date
from data.selections import months, years, days, options, options2, months2, years2
from db import connection
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class DashFrame:
    def __init__(self, main_frame, db):
        self.frame = main_frame

        self.connection = db
        
        self.pie_from_filter = "Select"
        self.pie_to_filter = "Select"

        self.graph_filter_year_var = StringVar()
        self.graph_filter_year_var.set("Select")
        self.graph_filter_month_var = StringVar()
        self.graph_filter_month_var.set("Select")

        self.pie_from_cal = None
        self.pie_to_cal = None

        self.no_records_lbl = None
        self.pie_totals = None

        self.filter_from_btn = None
        self.filter_to_btn = None

        self.pie = None
        self.graph = None

    def render_dash_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.generate_pie_filter_btns()
        Button(self.frame, text="Clear", command=self.clear_pie_filter).grid(row=2,column=0)

        OptionMenu(self.frame, self.graph_filter_year_var, *years2).grid(row=0,column=2)
        OptionMenu(self.frame, self.graph_filter_month_var, *months2).grid(row=1, column=2)
        Button(self.frame, text="Submit", command=self.render_graph).grid(row=2, column=2)
            
        self.render_graph()
        self.render_pie()

    def generate_pie_filter_btns(self):
        self.filter_from_btn = Button(self.frame, text="From: " + self.pie_from_filter, command=self.create_pie_from_cal).grid(row=0,column=0)
        self.filter_to_btn = Button(self.frame, text="To: " + self.pie_to_filter, command=self.create_pie_to_cal).grid(row=1,column=0)

    def create_pie_from_cal(self):
        self.pie_from_cal = calendar_filter.CalendarFilter("Filter Pie Chart From", "From")
        Button(self.pie_from_cal.frame, text="Submit", command=self.filter_pie_from).grid(row=2,column=0)

    def create_pie_to_cal(self):
        self.pie_to_cal = calendar_filter.CalendarFilter("Filter Pie Chart To", "To")
        Button(self.pie_to_cal.frame, text="Submit", command=self.filter_pie_to).grid(row=2,column=0)

    def filter_pie_from(self):
        self.pie_from_filter = self.pie_from_cal.cal.get_date()
        self.generate_pie_filter_btns()
        self.render_pie()
    
    def filter_pie_to(self):
        self.pie_to_filter = self.pie_to_cal.cal.get_date()
        self.generate_pie_filter_btns()
        self.render_pie()

    def clear_pie_filter(self):
        self.pie_from_filter = "Select"
        self.pie_to_filter = "Select"

    def render_pie(self):
        if self.pie and self.pie.axes:
            self.pie.delaxes(self.pie.axes[0])
        if self.no_records_lbl:
            self.no_records_lbl.destroy()
        if self.pie_totals:
            for total in self.pie_totals:
                total.destroy()
        #create list to store the total price values of each category
        totals = list()
        display_options = list()
        
        #for each category, SELECT all transactions and sum their total value
        #open connection
        self.connection.connect()
        num = 0
        for cat in options:
            self.connection.execute("SELECT * FROM transactions WHERE category=(:cat)", {
                'cat': cat
            })
            transactions_of_cat = self.connection.c.fetchall()
            total = 0
            for transaction in transactions_of_cat:
                add_this_one = TRUE
                trans_date = int(transaction[2]+transaction[1]+transaction[0])
                
                #if we have a from filter set
                if (self.pie_from_filter != "Select"):
                    #get the dates in a comparison format
                    from_date_split = self.pie_from_filter.split('/')
                    from_date = int(from_date_split[2] + from_date_split[0] + from_date_split[1])
                    add_this_one = add_this_one and from_date <= trans_date
                
                #if we have a to filter set
                if (self.pie_to_filter != "Select"):
                    #get the dates in a comparison format
                    to_date_split = self.pie_to_filter.split('/')
                    to_date = int(to_date_split[2] + to_date_split[0] + to_date_split[1])
                    add_this_one = add_this_one and to_date >= trans_date
                
                #if this one is included by our filters, add the price total to our categorical total
                if (add_this_one):
                    total+=transaction[4]
            
            #display the totals for the time frame we're looking at        
            if (total>0):
                display_options.append(cat)
                totals.append(total)
                self.pie_totals = list()
                label = Label(self.frame, text="Total spent on " + cat + ": " + str(total))
                label.grid(row=num+3, column=0)
                self.pie_totals.append(label)
                num+=1
        
        #close connection
        self.connection.disconnect()
        #load pie chart
        if (num>0):
            pie_chart_text = "Pie chart for categorical expenses"
            if (self.pie_from_filter != "Select"):
                pie_chart_text = pie_chart_text + " from " + self.pie_from_filter
            if (self.pie_to_filter != "Select"):
                pie_chart_text = pie_chart_text + " to " + self.pie_to_filter
            Label(self.frame, text=pie_chart_text).grid(row=0, column=1)
            fig = Figure(figsize= (5,5),dpi=100)
            plt = fig.add_subplot(111)
            plt.pie(totals, labels=display_options)
            canvas = FigureCanvasTkAgg(fig,master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2,column=1)
        else:
            self.no_records_lbl = Label(self.frame, text="No financial transaction data found. Return to this page for financial analysis tools once transactions are in the management system")
            self.no_records_lbl.grid(row=0,column=0)

    def render_graph(self):
        if self.graph and self.graph.axes:
            self.graph.delaxes(self.pie.axes[0])
        self.connection.connect()
        if (self.graph_filter_year_var.get() == "Select"):
            transactions = list(list())
            for cat in options:
                values_of_cat = list()
                for year in years:
                    if(self.graph_filter_month_var.get() != "Select"):
                        self.connection.execute("SELECT value FROM transactions WHERE year=(:year) AND category=(:cat) AND month=(:month)", {
                            'year': year,
                            'cat': cat,
                            'month': self.graph_filter_month_var.get()
                        })
                    else:
                        self.connection.execute("SELECT value FROM transactions WHERE year=(:year) AND category=(:cat)", {
                            'year': year,
                            'cat': cat
                        })
                    transactions_of_year = self.connection.c.fetchall()
                    sum = 0
                    for transaction in transactions_of_year:
                        sum = sum + transaction[0]
                    values_of_cat.append(sum)
                transactions.append(values_of_cat)

            #load graph
            fig = Figure(figsize=(5, 5), dpi=100)
            plt = fig.add_subplot(111)
            plt.set_ylabel('Dollars spent ($)')
            plt.set_xlabel('Year')
            plt.plot(years, transactions[0], label="Food")
            plt.plot(years, transactions[1], label="Transportation")
            plt.plot(years, transactions[2], label="Education")
            plt.plot(years, transactions[3], label="Entertainment")
            plt.plot(years, transactions[4], label="Housing")
            plt.plot(years, transactions[5], label="Misc.")
            plt.legend()
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=3)

        #year
        elif (self.graph_filter_month_var.get() == "Select" and self.graph_filter_year_var.get() != "Select"):
            transactions = list(list())
            for cat in options:
                values_of_cat = list()
                for month in months:
                    self.connection.execute("SELECT value FROM transactions WHERE month=(:month) AND category=(:cat) AND year=(:year)", {
                        'month': month,
                        'cat': cat,
                        'year': self.graph_filter_year_var.get()
                    })
                    transactions_of_month = self.connection.c.fetchall()
                    sum = 0
                    for transaction in transactions_of_month:
                        sum = sum + transaction[0]
                    values_of_cat.append(sum)
                transactions.append(values_of_cat)

            #load graph
            fig = Figure(figsize=(5, 5), dpi=100)
            plt = fig.add_subplot(111)
            plt.set_ylabel('Dollars spent ($)')
            plt.set_xlabel('Month')
            plt.plot(months, transactions[0], label="Food")
            plt.plot(months, transactions[1], label="Transportation")
            plt.plot(months, transactions[2], label="Education")
            plt.plot(months, transactions[3], label="Entertainment")
            plt.plot(months, transactions[4], label="Housing")
            plt.plot(months, transactions[5], label="Misc.")
            plt.legend()
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=3)

        #both
        else:
            transactions = list()
            idx = int(self.graph_filter_month_var.get())-1
            for day in days[idx]:
                self.connection.execute("SELECT value FROM transactions WHERE month=(:month) AND year=(:year) AND day=(:day)", {
                    'day': day,
                    'month': self.graph_filter_month_var.get(),
                    'year': self.graph_filter_year_var.get()
                })
                transactions_of_day = self.connection.c.fetchall()
                sum = 0
                for transaction in transactions_of_day:
                    sum = sum + transaction[0]
                transactions.append(sum)

            #load graph
            fig = Figure(figsize=(5, 5), dpi=100)
            plt = fig.add_subplot(111)
            plt.set_ylabel('Dollars spent ($)')
            plt.set_xlabel('Day')
            plt.plot(days[idx], transactions)
            canvas = FigureCanvasTkAgg(fig, master=self.frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row=2, column=3)
        #close connection
        self.connection.disconnect()
