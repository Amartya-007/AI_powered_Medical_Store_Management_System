from tkinter import *
import tkinter as tk
import Database as db
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import messagebox
from tkinter import ttk as ttk
from customtkinter import *
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
import pandas as pd



def reports(self):


    

    def show_daily_sales(txt_from, txt_to):
        
        
        start_date = txt_from.get_date().strftime('%Y-%m-%d')
        end_date = txt_to.get_date().strftime('%Y-%m-%d')
        
        try:
            # Fetch sales data for the specified date range
            sales_data = db.fetch_sales_data(start_date, end_date)
            
            # Calculate total sales
            if sales_data is not None:
                # Adjust the key to match the field name in the database table
                total_sales = sum(sale['total_amount'] for sale in sales_data)
            else:
                total_sales = 0

            # Update the text of the label widget with the total sales value
            net_sales_value.configure(text=f"Net Sales: {total_sales}")

        except Exception as e:
            # Handle any potential exceptions gracefully
            print(f"An error occurred: {e}")

    def plot_daily_sales(txt_from, txt_to):
        for widget in visualization_frame.winfo_children():
            widget.destroy()
        
        start_date = txt_from.get_date().strftime('%Y-%m-%d')
        end_date = txt_to.get_date().strftime('%Y-%m-%d')

        daily_sales = db.fetch_daily_sales(start_date, end_date)

        if daily_sales is not None and not daily_sales.empty:
            # Extract dates and sales from the daily_sales data
            dates = daily_sales.iloc[:, 1]  # Assuming the date column is at index 1
            sales = daily_sales.iloc[:, 2]  # Assuming the sale column is at index 2

            plt.figure(figsize=(10, 6))
            plt.plot(dates, sales, marker='o', linestyle='-')
            plt.title('Daily Sales')
            plt.xlabel('Date')
            plt.ylabel('Sales')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()

            # Convert the matplotlib figure to a Tkinter canvas
            canvas = FigureCanvasTkAgg(plt.gcf(), master=visualization_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # Add a toolbar for navigation
            toolbar = NavigationToolbar2Tk(canvas, visualization_frame)
            toolbar.update()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        else:
            messagebox.showinfo("No Data", "No daily sales data available for the selected date range.")


    def show_monthly_sales():
        
                # Clear the plot
        for widget in visualization_frame.winfo_children():
            widget.destroy()
        
        visualization_frame.get_tk_widget().pack_forget()
        
        # Clear the net sales value
        net_sales_value.configure(text="Net Sales: ")
        
        selected_month = month_combo.get()
        selected_year = year_combobox.get()

        # Convert month name to month number
        month_number = months.index(selected_month) + 1
        
        # Calculate the first and last day of the selected month and year
        first_day = datetime.strptime(f"{selected_year}-{month_number}-01", "%Y-%m-%d")
        last_day = (first_day + relativedelta(months=1) - timedelta(days=1))

        # Fetch monthly sales data
        monthly_sales_data = db.fetch_monthly_sales(first_day, last_day)

        # Display the fetched data
        if monthly_sales_data:
            # Extract total sales values from the fetched data
            total_sales_values = [sale['total_sales'] for sale in monthly_sales_data]
            total_sales = sum(total_sales_values)
            
            # Update the text of the label widget with the total sales value
            net_sales_value.configure(text=f"Net Sales: {total_sales}")
            
        else:
            messagebox.showinfo("No Data", "No monthly sales data available for the selected month and year.")

    def clear_month_year():
            # Remove the plot canvas from the visualization_frame
        for widget in visualization_frame.winfo_children():
            widget.destroy()
        
        # Clear the net sales value
        net_sales_value.configure(text="Net Sales: ")
        # Clear the selected month in the combo box
        month_combo.set('')

        # Clear the selected year in the combo box
        year_combobox.set('')

    def reset_date_entry():
        # Clear the plot
        for widget in visualization_frame.winfo_children():
                    widget.destroy()
        
        # Clear the net sales value
        net_sales_value.configure(text="Net Sales: ")
        # Clear the text in the date entry fields
        txt_from.delete(0, 'end')
        txt_to.delete(0, 'end')


    if self.f1:
        self.f1.destroy()
    self.f2 = CTkFrame(self.w, width=self.win_width, height=self.win_height, bg_color='transparent')
    self.f2.place(x=0, y=45)

    # ******* LABLE ********************************
    dataframetop = Frame(self.f2,bd=10,bg="#262626")
    dataframetop.place(x=0,y=0,width=self.win_width,height=60)
    customer_lable = CTkLabel(self.f2,text="SALES REPORTS AND DATA",
                                font=("Times new roman", 25,"underline","bold"),
                                bg_color="#262626",
                                fg_color="transparent",
                                text_color="white")
    customer_lable.place(x=590,y=5)
    
        # !================ MAIN DATAFRAME ====================
    
    # *------------ left side data frame ---------------------*
    
    detailsframe = Frame(self.f2,bd=0,relief="solid",padx=20,background="#262626")
    detailsframe.place(x=0,y=59,width=self.win_width,height=820)
    
    dataframeleft= CTkFrame(detailsframe,bg_color="#262626",border_width=2,height=300,width=450,border_color="light blue")
    dataframeleft.place(x=10,y=20)

    
    # #*lables for MEDICINE INFORMARION Information
    
        #! ============ ITEM CODE ==========
        
    range_label = CTkLabel(dataframeleft, text="Daily Sales", font=("Malgun Gothic", 25,"bold","underline"))
    range_label.place(x=155,y=10)

    # Label and Entry for Date
    from_label = CTkLabel(dataframeleft, text="From :- ", font=("Microsoft Tai Le", 25), fg_color="transparent", bg_color="transparent")
    from_label.place(x=50, y=70)
    txt_from = DateEntry(dataframeleft, selectmode="day", date_pattern='dd-mm-yyyy', width=20)
    txt_from.place(x=250, y=95)
    txt_from.config(font=("Arial", 15))
    
    
    # # Label and Entry for date
    to_label = CTkLabel(dataframeleft, text="To :- ", font=("Microsoft Tai Le", 25), fg_color="transparent", bg_color="transparent")
    to_label.place(x=80, y=135)
    txt_to = DateEntry(dataframeleft, selectmode="day", date_pattern='dd-mm-yyyy', width=20)
    txt_to.place(x=250, y=180)
    txt_to.config(font=("Arial", 15))
    
    
    show_btn= CTkButton(dataframeleft,text="S H O W",width=100,height=40,font=("Malgun Gothic",15,"bold"),command=lambda: show_daily_sales(txt_from, txt_to))
    show_btn.place(x=25,y=230)
    
    plot_btn= CTkButton(dataframeleft,text="P L O T",width=100,height=40,font=("Malgun Gothic",15,"bold"),command=lambda: plot_daily_sales(txt_from, txt_to))
    plot_btn.place(x=180,y=230)
    
    clear_btn = CTkButton(dataframeleft,text="R E S E T",width=100,height=40,font=("Malgun Gothic",15,"bold"),command = reset_date_entry)
    clear_btn.place(x=326,y=230)
      
    
    # !========================= BUTTOM FRAME =========================
    
    dataframeButtom = CTkFrame(detailsframe,bg_color="#262626",border_width=2,height=300,width=450,border_color="light blue")
    dataframeButtom.place(x=10,y=340)
    
    # * bottom frame lable 
    labels =CTkLabel(dataframeButtom, text="Monthly Sales", font=("Malgun Gothic", 25, "bold","underline"),bg_color="transparent",text_color="white")
    labels.place(x=155,y=10)
    
    month_label = CTkLabel(dataframeButtom, text="Month: ", font=("Microsoft Tai Le", 25),bg_color="transparent")
    month_label.place(x=50, y=70)
    # Dropdown menu for selecting month
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    month_combo = CTkComboBox(dataframeButtom, values=months, width=150,height=40,bg_color="transparent",fg_color="#262626")
    month_combo.place(x=190, y=70)
    month_combo.configure(font=("Arial", 20))
    
    year_label = CTkLabel(dataframeButtom, text="Year: ", font=("Microsoft Tai Le", 25),bg_color="transparent")
    year_label.place(x=50, y=130)
    
    # Current year for sensible default
    current_year = datetime.now().year
    years = list(map(str, range(1995, current_year + 1)))  # Include the current year
    year_combobox = CTkComboBox(dataframeButtom, values=years, state='readonly',width=150,height=40,bg_color="transparent",fg_color="#262626")
    
    # Find the index of the current year in the list of years
    current_year_index = years.index(str(current_year))

    # Set the current selection of the combo box
    year_combobox.set(years[current_year_index])
    year_combobox.configure(font=("Arial", 20))
    year_combobox.place(x=190, y=130)
    
    
    show_btn= CTkButton(dataframeButtom,text="S H O W",width=100,height=40,font=("Malgun Gothic",15,"bold"),command=show_monthly_sales)
    show_btn.place(x=25,y=230)
    
    forecast_btn= CTkButton(dataframeButtom,text="F O R E C A S T",width=100,height=40,font=("Malgun Gothic",15,"bold"))
    forecast_btn.place(x=160,y=230)
    
    clear_btn = CTkButton(dataframeButtom,text="C L E A R",width=100,height=40,font=("Malgun Gothic",15,"bold"),command=clear_month_year)
    clear_btn.place(x=326,y=230)
                
    # !======================================================================================================================
    # *------------ right side data frame ---------------------*
    
    
    
    dataframeright= CTkFrame(detailsframe,bg_color="transparent",fg_color="grey",border_width=2,height=620,width=840,border_color="light blue")
    dataframeright.place(x=510,y=20)

    # Create a label to display the net sales value
    net_sales_value = CTkLabel(dataframeright, text="", font=("Microsoft Tai Le", 25), fg_color="grey", bg_color="transparent",text_color="Red")
    net_sales_value.place(x=100, y=30)

    # Create a separate frame for data visualization
    visualization_frame = CTkFrame(dataframeright, bg_color="white", border_width=2, height=500, width=800, border_color="light blue")
    visualization_frame.place(x=20, y=90)
    
    # Create a button to plot net sales 
    