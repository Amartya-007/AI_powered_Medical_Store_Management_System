from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk as ttk
import tkinter as tk
from tkinter import StringVar
import customtkinter 
from customtkinter import *
from tkcalendar import Calendar
import random
from datetime import *
from mysql.connector import Error
import Database as db

def billing(self):
    if self.f1:
        self.f1.destroy()
    self.f2 = CTkFrame(self.w, width=self.win_width, height=self.win_height, bg_color='transparent')
    self.f2.place(x=0, y=45)

    # ******* LABLE ********************************
    dataframetop = Frame(self.f2, bd=10, bg="#262626")
    dataframetop.place(x=0, y=0, width=self.win_width, height=60)
    customer_label = CTkLabel(self.f2, text="BILLING",
                            font=("Times new roman", 30,"underline","bold"),
                            bg_color="#262626",
                            fg_color="transparent",
                            text_color="white")
    customer_label.place(x=660, y=5)

    # !******************************** FUNCTIONS ********************************

    # !====== variables
    c_name = StringVar()
    c_phone = StringVar()
    Medicine = StringVar()
    Price = StringVar()
    Quantity = StringVar()
    bill_no = StringVar()
    x = random.randint(1000, 99999)
    bill_no.set(str(x))
    global l
    l=[] 
    
    from tkinter import messagebox
    def display_initial_content():
        # Inserting store name and formatting
        textarea.insert(END, "\t\t   SHRI HARI MEDICAL STORE\n\n")
        
        # Display order ID, order date, customer name, and phone number
        order_id_text = f"Order ID: {txt_order_id.get()}"
        order_date_text = f"Order Date: {txt_order_date.get()}"
        customer_name_text = f"Customer Name: {c_name.get()}"
        customer_phone_text = f"Customer Phone: {c_phone.get():10}"
        
        # Insert the heading and customer information
        textarea.insert(END, f"{order_id_text}\t\t\t\t\t{order_date_text}\n\n{customer_name_text}\t\t\t\t\t{customer_phone_text}\n\n")

        # Insert column headers
        textarea.insert(END, '------------------------------------------------------------------\n')
        textarea.insert(END, '| ᴍᴇᴅɪᴄɪɴᴇ                      |    ᴘ.ᴘ.ᴜ.   |  ǫᴛʏ  |  ᴛᴏᴛᴀʟ   |\n')
        textarea.insert(END, '------------------------------------------------------------------\n')

        textarea.configure(font="courier 12")
        
    def generate_invoice():
        # Clear the bill area initially
        textarea.delete(1.0, END)
        
        # Display initial content and headings
        display_initial_content()
        
        # Check if customer name and phone number are entered
        if not c_name.get() or not c_phone.get():
            messagebox.showerror("Error", "Please enter customer name and phone number.")
            return
        
        # Check if at least one medicine detail is entered
        if not l:
            messagebox.showerror("Error", "Please add at least one medicine detail.")
            return
        
        # Proceed to generate the invoice
        total_medicine_costs = [med[3] for med in l]  # List to store total cost of each medicine
        
        # Display stored medicine details
        for index, med in enumerate(l, start=1):
            med_name, price_per_unit_str, quantity_str, med_total_cost = med
            formatted_output = f'| {med_name:<29} | {price_per_unit_str:^11} | {quantity_str:^5} | {med_total_cost:^8.1f} |\n'
            # Print formatted output in the textarea
            textarea.insert(END, formatted_output)
            textarea.configure(font='Courier 12')
        textarea.insert(END, '------------------------------------------------------------------\n')

        # Calculate total medicine cost
        total_medicine_cost = sum(total_medicine_costs)
        
        # Calculate total amount after applying discount
        discount_rate = 0.08  # 8% discount rate
        discount_amount = total_medicine_cost * discount_rate
        total_amount = total_medicine_cost - discount_amount
        
        # Insert total payment amount into the text area
        textarea.insert(END, f'\n==================================================================\n\n')
        textarea.insert(END, f"Your total Amount is :{total_medicine_cost:<.2f}Rs\n")
        textarea.insert(END, f"Your Total Payable Amount with 8% discount 😊 : {total_amount:<.2f} Rs\n")
        textarea.insert(END, "\nThank you for shopping! NAMASTE 🙏🏻\n")
        textarea.insert(END, "==================================================================")

        bill_date = datetime.now().strftime("%Y/%m/%D")  # Format: dd/mm/yyyy
        # Save the bill details in the database
        customer_name_text = c_name.get()
        customer_phone_text = c_phone.get()
        CustomerID = db.fetch_latest_CustomerID(customer_name_text, customer_phone_text)
        OrderID = txt_order_id.get()
        db.save_to_database(OrderID, customer_name_text, customer_phone_text, bill_date, total_amount, CustomerID)

        # Clear the variables
        c_name.set('')
        c_phone.set('')
        l.clear()
        Medicine.set('')
        
        # Show messagebox indicating successful save
        messagebox.showinfo("Success", "Bill details saved in database.")




    def add_med():
        # Get the selected medicine details from the GUI
        med_name = combobox.get()  # Get the selected medicine name
        
        quantity_str = txt_quantity.get()  # Get the quantity as string
                
        # Check if medicine name is empty
        if not med_name:
            messagebox.showerror("Error", "Please enter medicine name.")
            return
                
        # Check if quantity is empty or not a positive integer
        if not quantity_str or not quantity_str.isdigit() or int(quantity_str) <= 0:
            messagebox.showerror("Error", "Please enter a valid positive quantity.")
            return

        # Convert quantity to an integer
        quantity = int(quantity_str)

        # Call the fetch_details() function to fetch medicine details
        fetch_details()
        med_id = txt_med_id.get()  # Get the medicine ID
        price_per_unit_str = txt_ppu.get()  # Get the price per unit as string    
        
        price_per_unit = float(price_per_unit_str)  # Convert price per unit to a float
        # Calculate the total cost for this medicine
        total_cost = price_per_unit * quantity

        # Append the medicine details to the list as a tuple
        l.append((med_name, price_per_unit_str, quantity_str, total_cost))

        formatted_output = f'{med_name:<35}'  # Fixed width for medicine name
        formatted_output += f'{price_per_unit_str:^10} \t{quantity_str:^5}\t{total_cost:>10.2f}\n'  # Using fixed width for other fields
        # Print formatted output in the textarea
        textarea.insert(END, formatted_output)
        textarea.configure(font='Courier 12')

        
        
    def fetch_details():
    # Get the selected medicine name from the combobox
        selected_medicine = combobox.get()

        # Connect to the database
        connection = db.connect_to_database()

        if connection:
            try:
                # Creating a cursor object using the cursor() method
                cursor = connection.cursor()

                # Preparing query to fetch details of the selected medicine
                query = "SELECT ItemCode, PricePerUnit FROM inventoryitem WHERE ItemName = %s"

                # Executing the SQL query with the selected medicine name as parameter
                cursor.execute(query, (selected_medicine,))

                # Fetching the row from the result set
                row = cursor.fetchone()

                if row:
                    # Extracting details from the row
                    item_code, price_per_unit = row

                    # Display the details in the GUI
                    txt_med_id.delete(0, END)
                    txt_med_id.insert(0, item_code)
                    txt_ppu.delete(0, END)
                    txt_ppu.insert(0, price_per_unit)
                else:
                    messagebox.showinfo("Error", "Medicine details not found.")

            except Error as e:
                print(f"Error fetching medicine details: {e}")

            finally:
                # Closing the cursor and connection
                cursor.close()
                db.close_connection(connection)
        else:
            messagebox.showerror("Error", "Failed to connect to the database.")
            
    def clear():
            c_name.set('')
            c_phone.set('')
            Price.set('')
            Quantity.set('')
            Medicine.set('')
            textarea.delete(1.0, END)
            l.clear()
            display_initial_content()
    
  

        # !******************************** FUNCTIONS END ********************************

        # !================ MAIN DATAFRAME ====================

        # *------------ left side data frame ---------------------*

    detailsframe = Frame(self.f2, bd=0, relief="solid", padx=20, background="#262626")
    detailsframe.place(x=0, y=59, width=self.win_width, height=1000)
    dataframeleft = CTkFrame(detailsframe, bg_color="#262626", border_width=2, height=650, width=800,
                            border_color="light blue")
    dataframeleft.place(x=0, y=0)
    title = CTkLabel(dataframeleft, text="Customer details",
                    font=("Malgun Gothic", 25, "underline", "bold"),
                    bg_color="transparent",
                    fg_color="transparent",
                    text_color="white")
    title.place(x=290, y=10)

    # *============== ORDER ID =============

    order_id = CTkLabel(dataframeleft, text="Order ID", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent", bg_color="transparent")
    order_id.place(x=30, y=90)

    # Create the CTkEntry widget for order ID
    txt_order_id = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue")
    txt_order_id.place(x=165, y=90)

    # Get the next order ID
    next_order_id = db.get_next_order_id()

    # Place the next order ID in the CTkEntry widget
    txt_order_id.delete(0, END)
    txt_order_id.insert(0, next_order_id)

    
    # *============== ORDER DATE =============
    order_date = CTkLabel(dataframeleft, text="Order Date", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent", bg_color="transparent")
    order_date.place(x=420, y=90)

    # Get the current date
    current_date = datetime.now().strftime("%d/%m/%Y")  # Format: dd/mm/yyyy

    # Create the CTkEntry widget for order date
    txt_order_date = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue")
    txt_order_date.place(x=530, y=90)

    # Place the current date in the CTkEntry widget
    txt_order_date.delete(0, END)
    txt_order_date.insert(0, current_date)
    # *============== CUSTOMER ID =============

    customer_name = CTkLabel(dataframeleft, text="Cust. Name", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent",
                        bg_color="transparent")
    customer_name.place(x=30, y=160)
    txt_customer_name = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue",textvariable=c_name)
    txt_customer_name.place(x=165, y=160)

    # *============== PHONE NUMBER =============
    phone = CTkLabel(dataframeleft, text="Phone no.", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent",
                    bg_color="transparent")
    phone.place(x=420, y=160)
    txt_phone = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue",textvariable=c_phone)
    txt_phone.place(x=530, y=160)

    # !============================== SEPARATOR =======================
    separator = ttk.Separator(dataframeleft, orient='horizontal')
    separator.place(x=0, y=290, relx=0.1, relwidth=0.8)

    # *======================= MEDICINE INFO ======================

    product = CTkLabel(dataframeleft, text="Product Details",
                    font=("Malgun Gothic", 25, "underline", "bold"),
                    bg_color="transparent",
                    fg_color="transparent",
                    text_color="white")
    product.place(x=300, y=250)

    # !================================================================================================================================================
    med_name = CTkLabel(dataframeleft, text="Medicine", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent",
                        bg_color="transparent")
    med_name.place(x=30, y=320)

    medication_names = db.fetch_medicine_list()

    combobox = customtkinter.CTkComboBox(master=dataframeleft,
                                        values=medication_names,
                                        width=210,
                                        height=38,
                                        border_color="light blue",
                                        font=("Microsoft Tai Le", 15, "bold"),
                                        corner_radius=10,
                                        dropdown_text_color="white",
                                        dropdown_fg_color="#262626",
                                        border_width=2,
                                        dropdown_hover_color="light blue")
    combobox.set('')  # Set initial value to empty string
    combobox.place(x=140, y=320)
    # Set initial value to an empty string
    combobox.set('')


    # !================================================================================================================================================

    # *======================= MEDICINE ID ======================

    med_id = CTkLabel(dataframeleft, text="Medicine ID", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent",
                    bg_color="transparent")
    med_id.place(x=380, y=320)
    txt_med_id = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue")
    txt_med_id.place(x=530, y=320)

    # *======================= PRICE PER UNIT ======================

    ppu = CTkLabel(dataframeleft, text="P.P.U", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent",
                bg_color="transparent")
    ppu.place(x=30, y=390)

    txt_ppu = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue",
                    textvariable=Price)
    txt_ppu.place(x=140, y=390)


    # *======================= QUANTITY ======================

    quantity = CTkLabel(dataframeleft, text="Quantity", font=("Microsoft Tai Le", 20, "bold"), fg_color="transparent",
                        bg_color="transparent")
    quantity.place(x=380, y=390)
    txt_quantity = CTkEntry(dataframeleft, font=("Microsoft Tai Le", 18), width=210, height=38, border_color="light blue",
                            textvariable=Quantity)
    txt_quantity.place(x=530, y=390)

    # !================================= BUTTONS =================================================

    # **ADD MEDICINE button**
    btn_ADD = customtkinter.CTkButton(dataframeleft, text="ADD MEDICINE", cursor="hand2", font=("Malgun Gothic", 15),
                                    height=60, width=180, hover_color=("#00cc66"), text_color="white",command=add_med)
    btn_ADD.place(x=45, y=470)

    # ** CLEAR MEDICINE button
    clear_Button = customtkinter.CTkButton(dataframeleft, text="C L E A R", font=("Malgun Gothic", 15),cursor="hand2", height=60, width=180,command=clear)
    clear_Button.place(x=590, y=470)

    # ** GENERATE INVOICE button
    GENERATE_Button = customtkinter.CTkButton(dataframeleft, text="GENERATE INVOICE", font=("Malgun Gothic", 15),
                                            cursor="hand2", height=60, width=180,command=generate_invoice)
    GENERATE_Button.place(x=310, y=470)

    # ** PRINT button
    print_Button = customtkinter.CTkButton(dataframeleft, text="P R I N T", font=("Malgun Gothic", 15), cursor="hand2",
                                        height=60, width=180)
    print_Button.place(x=175, y=560)

    # ** Fetch button
    fetch_Button = customtkinter.CTkButton(dataframeleft, text="F E T C H", font=("Malgun Gothic", 15), cursor="hand2",
                                        height=60, width=180, hover_color="red",command=fetch_details)
    fetch_Button.place(x=450, y=560)

    dataframeright = Frame(bd=5, relief=GROOVE)
    dataframeright.place(x=1050, y=115, width=680, height=810)

    bill_lable = Label(dataframeright, text="B I L L    A R E A ", font=("Times new roman", 20, "bold"), bg="white",
                    relief=SUNKEN).pack(fill=X, side=TOP)

    # *************************Bills area***************************************

    textarea = Text(dataframeright, font=("arial", 15), bg="grey")
    textarea.pack(fill=BOTH, expand=1)

    display_initial_content()
