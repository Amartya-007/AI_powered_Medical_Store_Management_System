from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk as ttk
import customtkinter 
from customtkinter import *
from tkcalendar import Calendar
from datetime import *
import Database as db


def customer_info(self):
    
    def display_values(values):
        # Clear the table before displaying search results
        for record in self.table.get_children():
            self.table.delete(record)
        self.table.insert('', 'end', values=values)
        
    def save_action():
        # Retrieve values from Entry widgets
        CustomerID = txt_C_id.get()
        Customer_name = txt_C_name.get()
        Customer_dob = txt_DOB_entry.get()
        phone = txt_phone.get()
        blood_group = combobox.get()
        reference_id = txt_ref.get()
        gender = combobox_gen.get()
        allergies = txt_allergies.get()
        address = txt_add.get()

        # Check if Customer_name and phone are empty
        if Customer_name.strip() == "":
            messagebox.showerror("Error", "Customer name cannot be empty.")
            return
        if phone.strip() == "":
            messagebox.showerror("Error", "Phone number cannot be empty.")
            return

        # If DOB is empty, set it to NULL
        if Customer_dob.strip() == "" or Customer_dob == "YYYY-MM-DD":
            Customer_dob = None

        # Construct tuple with data
        values = (CustomerID, Customer_name, phone, Customer_dob, blood_group, reference_id, gender, allergies, address)

        # Call function to add data to database
        last_row_id = db.add_to_customers("customers", values)
        
        if last_row_id is not None:
            # Clear entry fields
            txt_C_id.delete(0, 'end')
            txt_C_name.delete(0, 'end')
            txt_DOB_entry.delete(0, 'end')
            txt_phone.delete(0, 'end')
            combobox.set("O+")  # Reset combobox to default value
            txt_ref.delete(0, 'end')
            combobox_gen.set("Male")  # Reset combobox to default value
            txt_allergies.delete(0, 'end')
            txt_add.delete(0, 'end')
            
            # Fetch and display next Customer ID
            next_CustomerID = db.fetch_next_C_ID()
            txt_C_id.delete(0, 'end')
            txt_C_id.insert(0, next_CustomerID)
            
            # Display popup message
            messagebox.showinfo("Success", "Data saved successfully.")
        
        # Display the saved record in the table
        display_values(values)

    def update_action():
        # Get selected item from the table
        selected_item = self.table.selection()

        # Check if any item is selected
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update.")
            return

        # Retrieve Customer ID from the selected item
        CustomerID = self.table.item(selected_item, "values")[0]

        # Retrieve values from Entry widgets
        Customer_name = txt_C_name.get()
        Customer_dob = txt_DOB_entry.get()
        phone = txt_phone.get()
        blood_group = combobox.get()
        reference_id = txt_ref.get()
        gender = combobox_gen.get()
        allergies = txt_allergies.get()
        address = txt_add.get()

        # Check if any field is updated
        if not any([Customer_name, Customer_dob, phone, blood_group, gender, allergies, address, reference_id]):
            messagebox.showerror("Error", "Please update at least one field.")
            return

        # Check if DOB is in the format 'YYYY-MM-DD'
        if Customer_dob == 'yyyy/mm/dd':
            Customer_dob = None

        # Construct the update query
        update_query = "UPDATE customers SET "
        fields = []
        if Customer_name:
            fields.append(f"Name = '{Customer_name}'")
        if Customer_dob:
            fields.append(f"DOB = '{Customer_dob}'")
        if phone:
            fields.append(f"Phone = '{phone}'")
        if blood_group:
            fields.append(f"BloodGroup = '{blood_group}'")
        if gender:
            fields.append(f"Gender = '{gender}'")
        if allergies:
            fields.append(f"Allergies = '{allergies}'")
        if address:
            fields.append(f"Address = '{address}'")
        if reference_id:
            fields.append(f"ReferenceID = '{reference_id}'")

        # Combine the fields into the query
        update_query += ", ".join(fields)
        update_query += f" WHERE CustomerID = {CustomerID};"

        # Execute the update query
        try:
            connection = db.connect_to_database()
            if connection:
                cursor = connection.cursor()
                cursor.execute(update_query)
                connection.commit()
                messagebox.showinfo("Success", "Record updated successfully.")
                # Refresh the GUI table to reflect the changes
                showall_action()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating record: {e}")
        finally:
            db.close_connection(connection)

    def showall_action():
        try:
            connection = db.connect_to_database()
            if connection:
                cursor = connection.cursor()
                # Execute SQL query to select all records
                cursor.execute("SELECT * FROM customers ORDER BY CustomerID")
                # Clear GUI table
                self.table.delete(*self.table.get_children())
                # Display all records in the GUI table
                for row in cursor.fetchall():
                    self.table.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error retrieving records: {e}")
        finally:
            db.close_connection(connection)

    def search_action():
        # Retrieve Customer ID from Entry widget
        CustomerID = txt_C_id.get()

        # Check if Customer ID is provided
        if not CustomerID:
            messagebox.showerror("Error", "Please enter a Customer ID.")
            return

        # Fetch the record from the database based on the Customer ID
        record = db.fetch_record_by_C_ID(CustomerID)

        # Check if record exists
        if record:
            # Clear the table before displaying search result
            for item in self.table.get_children():
                self.table.delete(item)
            # Display the record in the table
            self.table.insert("", "end", values=record)
        else:
            messagebox.showinfo("Information", f"No record found for Customer ID {CustomerID}.")

    def delete_action():
        # Get selected item from the table
        selected_item = self.table.selection()

        # Check if any item is selected
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to delete.")
            return

        # Retrieve Customer ID from the selected item
        CustomerID = self.table.item(selected_item, "values")[0]

        # Ask for confirmation before deleting
        confirmation = messagebox.askquestion("Confirm Delete", "Are you sure you want to delete this record and its associated billing records?")
        if confirmation == "yes":
            try:
                connection = db.connect_to_database()
                if connection:
                    cursor = connection.cursor()

                    # Retrieve associated billing records for the customer
                    cursor.execute(f"SELECT order_id FROM bills WHERE CustomerID = {CustomerID}")
                    billing_records = cursor.fetchall()

                    # Delete billing records first
                    for record in billing_records:
                        cursor.execute(f"DELETE FROM bills WHERE order_id = {record[0]}")
                    
                    # Then, delete the customer record
                    cursor.execute(f"DELETE FROM customers WHERE CustomerID = {CustomerID}")

                    connection.commit()
                    messagebox.showinfo("Success", f"Customer record with Customer ID {CustomerID} and associated billing records deleted successfully.")
                    # Clear entry fields after deletion
                    clear_action()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting record: {e}")
            finally:
                db.close_connection(connection)
                
            # Refresh the GUI table to reflect the changes
            showall_action()
                 
    def count_bills_for_customer(CustomerID):
        try:
            connection = db.connect_to_database()
            if connection:
                cursor = connection.cursor()
                # Execute SQL query to count the number of billing records for the given CustomerID
                cursor.execute(f"SELECT COUNT(*) FROM bills WHERE CustomerID = {CustomerID}")
                count = cursor.fetchone()[0]  # Fetch the count value
                return count
        except Exception as e:
            print(f"Error counting billing records: {e}")
        finally:
            db.close_connection(connection)

    def clear_action():
        # Clear entry fields
        txt_C_id.delete(0, 'end')
        txt_C_name.delete(0, 'end')
        txt_DOB_entry.delete(0, 'end')
        txt_phone.delete(0, 'end')
        combobox.set("O+")  # Reset combobox to default value
        txt_ref.delete(0, 'end')
        combobox_gen.set("Male")  # Reset combobox to default value
        txt_allergies.delete(0, 'end')
        txt_add.delete(0, 'end')
        
  
    if self.f1:
        self.f1.destroy()
    self.f2 = CTkFrame(self.w, width=self.win_width, height=self.win_height, bg_color='blue')
    self.f2.place(x=0, y=45)
    
    dataframe = CTkFrame(self.f2, border_width=2,border_color="light blue",width=1400, height=330, fg_color="#262626" )
    dataframe.place(x=0, y=0)
    
    customer_label = CTkLabel(dataframe, text="𝐂𝐮𝐬𝐭𝐨𝐦𝐞𝐫 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧", font=("Times new roman", 35, "underline"), fg_color="#262626", bg_color="#FFFFFF", text_color="white")
    customer_label.place(x=590, y=15)
                        # !=================================row 1 ===========================
    # ********* some funtions ================= 
    
    
    # ********* some funtions end  ================= 
    #                                     #********** Customer ID*********
    CustomerID = CTkLabel(dataframe, text="Customer ID", font=("Microsoft Tai Le", 20),fg_color="#262626")
    CustomerID.place(x=25, y=100)
    txt_C_id = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    txt_C_id.place(x=150, y=95)
    
                                # ********* Patient name********
    C_name = CTkLabel(dataframe, text="Customer name", font=("Microsoft Tai Le", 20),fg_color="#262626")
    C_name.place(x=480, y=100)
    txt_C_name = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    txt_C_name.place(x=640, y=95)
                                # ********* Phone number********
    Phone = CTkLabel(dataframe, text="Phone number", font=("Microsoft Tai Le", 20),fg_color="#262626")
    Phone.place(x=920, y=100)
    txt_phone = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    txt_phone.place(x=1080, y=95)
    
                # !=================================row 2 ===========================
                            # ********* DOB ********
        # Function to clear placeholder text when entry field is clicked
    def clear_placeholder(event):
        if txt_DOB_entry.get() == "yyyy/mm/dd":
            txt_DOB_entry.delete(0, "end")  # Clear placeholder text

    # Set placeholder text for DOB entry field
    txt_DOB_label = CTkLabel(dataframe, text="DOB", font=("Microsoft Tai Le", 20), fg_color="#262626")
    txt_DOB_label.place(x=55, y=180)

    txt_DOB_entry = CTkEntry(dataframe, font=("Microsoft Tai Le", 18), width=200, height=38, border_color="light blue")
    txt_DOB_entry.insert(0, "yyyy/mm/dd")  # Insert placeholder text
    txt_DOB_entry.place(x=150, y=180)

    # Bind entry field to clear_placeholder function when clicked
    txt_DOB_entry.bind("<FocusIn>", clear_placeholder)
    
                            # ********* blood group********
    text_BG = CTkLabel(dataframe, text="Blood Group", font=("Microsoft Tai Le", 20),fg_color="#262626")
    text_BG.place(x=480, y=180)
    # txt_BG =CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    # txt_BG.place(x=620, y=175)
    combobox = customtkinter.CTkComboBox(master=dataframe,
                                values=["O+","A+","B+","AB+","O-","A-","B-","AB-"],
                                width=200,height=38,
                                border_color="light blue",
                                font=("Microsoft Tai Le",15,"bold"),
                                corner_radius=10,
                                dropdown_text_color="white",
                                dropdown_fg_color="#262626",
                                border_width=2,
                                state="readonly",
                                dropdown_hover_color="light blue",
                                justify="center")
    combobox.set("O+")  # set initial value
    combobox.place(x=640, y=175)
    
    #                 # ********* Reference id********
    
    Allergies = CTkLabel(dataframe, text="Allergies ", font=("Microsoft Tai Le", 20),fg_color="#262626")
    Allergies.place(x=40, y=265)
    txt_allergies = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    txt_allergies.place(x=150, y=260)
    
        # !=================================row 3===========================
                # ********* gender********
    Gender = CTkLabel(dataframe, text="Gender", font=("Microsoft Tai Le", 20),fg_color="#262626")
    Gender.place(x=920, y=180)
    # txt_gender = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    # txt_gender.place(x=150, y=260)
    combobox_gen = customtkinter.CTkComboBox(master=dataframe,
                                values=["Male", "Female","Other"],
                                width=200,height=38,
                                border_color="light blue",
                                corner_radius=10,
                                font=("Microsoft Tai Le",15,"bold"),
                                dropdown_text_color="white",
                                dropdown_fg_color="#262626",
                                border_width=2,
                                dropdown_hover_color="light blue",
                                justify="center")
    combobox_gen.set("Male")  # set initial value
    combobox_gen.place(x=1080, y=175)

                # ********* Allergirs********
    refereceid = CTkLabel(dataframe, text="Reference ID", font=("Microsoft Tai Le", 20),fg_color="#262626")
    refereceid.place(x=920, y=265)
    txt_ref = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    txt_ref.place(x=1080, y=260)

    #                 # ********* Address********
    address = CTkLabel(dataframe, text="Address", font=("Microsoft Tai Le", 20),fg_color="#262626")
    address.place(x=480, y=265)
    txt_add = CTkEntry(dataframe, font=("Microsoft Tai Le", 18),width=200,height=38,border_color="light blue")
    txt_add.place(x=640, y=260)
    
    #*============================= Buttons=====================================

    # Add commands to the buttons
    btn_save = customtkinter.CTkButton(self.w, text="S A V E", cursor="hand2", font=("Malgun Gothic",15), height=40, width=150, hover_color="#3AAD0D", command=save_action)
    btn_save.place(x=25, y=390)

    update_Button = customtkinter.CTkButton(self.w, text="U P D A T E", font=("Malgun Gothic",15), cursor="hand2", height=40, width=150, command=update_action)
    update_Button.place(x=255, y=390)

    show_Button = customtkinter.CTkButton(self.w, text="S H O W  R E C O R D S", font=("Malgun Gothic",15), cursor="hand2", height=40, width=150, command=showall_action)
    show_Button.place(x=485, y=390)

    search_Button = customtkinter.CTkButton(self.w, text="S E A R C H", font=("Malgun Gothic",15), cursor="hand2", height=40, width=150, command=search_action)
    search_Button.place(x=740, y=390)

    delete_Button = customtkinter.CTkButton(self.w, text="D E L E T E", font=("Malgun Gothic",15), cursor="hand2", height=40, width=150, hover_color="red", command=delete_action)
    delete_Button.place(x=975, y=390)

    clear_Button = customtkinter.CTkButton(self.w, text="C L E A R", font=("Malgun Gothic",15), cursor="hand2", height=40, width=150, hover_color="red", command=clear_action)
    clear_Button.place(x=1220, y=390)
        

    # Table
    style = ttk.Style()
    style.theme_use("clam")
    
    detailsframe =Frame(self.w,bg="#262626",borderwidth=5,background="blue")
    detailsframe.place(x=0,y=550,height=380,width=self.win_width)

    Scroll_x = ttk.Scrollbar(detailsframe, orient=HORIZONTAL)
    Scroll_x.pack(side=BOTTOM, fill=X)

    Scroll_y = ttk.Scrollbar(detailsframe, orient=VERTICAL)
    Scroll_y.pack(side=RIGHT, fill=Y)

    self.table = ttk.Treeview(detailsframe, column=("C_ID", "C_name", "C_no", "DOB", "BG", "Gen", "Alle", "ADDRESS", "R_ID"), xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
    Scroll_x.config(command=self.table.xview)
    Scroll_y.config(command=self.table.yview)
    
    self.table.heading("C_ID", text="𝐂 𝐔 𝐒 𝐓 𝐎 𝐌 𝐄 𝐑   𝐈 𝐃")
    self.table.heading("C_name", text="𝐂 𝐔 𝐒 𝐓 𝐎 𝐌 𝐄 𝐑   𝐍 𝐀 𝐌 𝐄")
    self.table.heading("C_no", text="𝐏 𝐇 𝐎 𝐍 𝐄  𝐍 𝐎 .")
    self.table.heading("DOB", text="𝐃 𝐎 𝐁")
    self.table.heading("BG", text="𝐁 𝐋 𝐎 𝐎 𝐃   𝐆 𝐑 𝐎 𝐔 𝐏")
    self.table.heading("Gen", text="𝐆 𝐄 𝐍 𝐃 𝐄 𝐑")
    self.table.heading("Alle", text="𝐀 𝐋 𝐋 𝐄 𝐑 𝐆 𝐈 𝐄 𝐒")
    self.table.heading("ADDRESS", text="𝐀 𝐃 𝐃 𝐑 𝐄 𝐒 𝐒")
    self.table.heading("R_ID", text="𝐑 𝐄 𝐅 .  𝐈 𝐃 .")
    self.table['show'] = 'headings'

    self.table.column("C_ID", width=100)
    self.table.column("C_name", width=120)
    self.table.column("C_no", width=100)
    self.table.column("DOB", width=100)
    self.table.column("BG", width=100)
    self.table.column("Gen", width=100)
    self.table.column("Alle", width=100)
    self.table.column("ADDRESS", width=100)
    self.table.column("R_ID", width=100)
    self.table.pack(fill="both", expand=True)

    def combobox_callback(choice):
        print("combobox dropdown clicked:", choice)
    
    def on_enter_exit(event):
        clear_Button.config(bg="red")

    def on_leave_exit(event):
        clear_Button.config(bg="light blue")

    def confirm_exit( ):
        confirmation = messagebox.askquestion("Confirm Exit", "Are you sure you want to exit?")
        if confirmation == "yes":
            dataframe.destroy()

    self.toggle_win()