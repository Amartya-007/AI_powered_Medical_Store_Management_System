from tkinter import *
from tkinter import messagebox
from tkinter import ttk as ttk
import tkinter as tk
import customtkinter 
from customtkinter import *
import Database as db
import datetime
 

def inventory(self):   
    
    def clear_table():
        for i in self.table.get_children():
            self.table.delete(i)
    
    def clear_entries():
        # Clear the text in all entry widgets
        txt_store_code.delete(0, 'end')
        txt_item_code.delete(0, 'end')
        txt_item_name.delete(0, 'end')
        txt_price.delete(0, 'end')
        text_Quantity.delete(0, 'end')
        text_MFG_DATE.delete(0, 'end')
        text_EXP_DATE.delete(0, 'end')

    def validate_input(itemocode_txt, itemname_txt, price_txt, quantity_txt, mfg_date_txt, exp_date_txt, store_id):
        """Validate input fields."""
        if itemocode_txt == "" or itemname_txt == "" or price_txt == "" or quantity_txt == "" or mfg_date_txt == "" or exp_date_txt == "" or store_id == "":
            raise ValueError("All fields are required")

    def save_values():
        # Retrieve values from Entry widgets
        store_id = txt_store_code.get()
        itemocode_txt = txt_item_code.get()
        itemname_txt = txt_item_name.get()
        price_txt = txt_price.get()
        quantity_txt = text_Quantity.get()
        mfg_date_txt = text_MFG_DATE.get()
        exp_date_txt = text_EXP_DATE.get()

        try:
            # Parse date strings to extract year and month only
            mfg_date_txt_f = datetime.strptime(mfg_date_txt, '%Y-%m-%d').date()
            exp_date_txt_f = datetime.strptime(exp_date_txt, '%Y-%m-%d').date()

            validate_input(itemocode_txt, itemname_txt, price_txt, quantity_txt, mfg_date_txt_f, exp_date_txt_f, store_id)
            values = (itemocode_txt, itemname_txt, quantity_txt, price_txt, store_id,exp_date_txt_f, mfg_date_txt_f)
            db.add_to_inventoryitem(values)
            messagebox.showinfo("Success", "Record added successfully")
            clear_table()
            # Display saved record in GUI table if needed
            self.table.insert('', 'end', values=values)  # Call function to update GUI table
        except ValueError as ve:
            messagebox.showerror("Error", str(ve))
        except Exception as e:
            messagebox.showerror("Error", f"Error adding record: {e}")
            
        clear_entries()

    def update_record():
        selected_item = self.table.selection()

        # Check if an item is selected from the GUI table
        if selected_item:
            # Get the selected item from the Treeview widget
            item_code = self.table.item(selected_item, 'values')[0]

            # Define a dictionary to store updated values
            updated_values = {}

            # Retrieve values from Entry widgets if they are not empty
            if txt_item_name.get():
                updated_values["ItemName"] = txt_item_name.get()
            if txt_price.get():
                updated_values["PricePerUnit"] = txt_price.get()
            if text_Quantity.get():
                updated_values["QuantityAvailable"] = text_Quantity.get()
            if text_MFG_DATE.get():
                updated_values["MfgDate"] = text_MFG_DATE.get()
            if text_EXP_DATE.get():
                updated_values["ExpDate"] = text_EXP_DATE.get()
            # Add conditions for other entry widgets as needed

            if updated_values:
                try:
                    # Update the record in the database using the item code and updated values
                    db.update_inventory_item(item_code, **updated_values)
                    messagebox.showinfo("Success", "Record updated successfully")
                    # Clear the Entry widgets or input fields
                    clear_input_fields()
                    # Refresh the GUI table to reflect the changes
                    show_all()
                except Exception as e:
                    messagebox.showerror("Error", f"Error updating record: {e}")
            else:
                messagebox.showerror("Error", "No values entered for update")
        else:
            messagebox.showerror("Error", "Please select a record to update")

    def clear_input_fields():
        # Clear the contents of all Entry widgets or input fields
        txt_item_code.delete(0, tk.END)
        txt_item_name.delete(0, tk.END)
        txt_price.delete(0, tk.END)
        text_Quantity.delete(0, tk.END)
        text_MFG_DATE.delete(0, tk.END)
        text_EXP_DATE.delete(0, tk.END)
        
    def search_item():
        # Retrieve the search parameters entered by the user
        item_code = txt_item_code.get()
        exp_date = text_EXP_DATE.get().lower()

        # Check if only item code is provided
        if item_code and not exp_date.lower() == "expired":
            search_item_by_code(item_code)
        # Check if only expiration date is set to "expired"
        elif not item_code and exp_date.lower() == "expired":
            search_expired_medicines()
        # Check if both item code and expiration date are provided
        elif item_code and exp_date.lower() == "expired":
            search_by_both_parameters(item_code)
        else:
            messagebox.showerror("Error", "Invalid search parameters")
    
    # under progress        
    def search_by_both_parameters(item_code):
        try:
            connection = db.connect_to_database()
            if connection:
                cursor = connection.cursor()
                current_date = datetime.datetime.now().date()
                exp_date_txt = text_EXP_DATE.get()
                exp_date_param_lower = exp_date_txt.lower()

                # Check if both item code and expiry date are provided
                if item_code and exp_date_param_lower == "expired":
                    # Convert the current date to the format 'YYYY-MM-DD'
                    current_date_str = current_date.strftime('%Y-%m-%d')
                    
                    # Construct the SQL query with both parameters
                    query = "SELECT * FROM inventoryitem WHERE ItemCode LIKE %s AND ExpiryDate < %s"
                
                    # Execute the query with parameters
                    cursor.execute(query, (f"%{item_code}%", current_date_str))
                    
                    # Fetch all matching records
                    search_results = cursor.fetchall()

                    return search_results
                else:
                    messagebox.showerror("Error", "Invalid search parameters")

        except Exception as e:
            messagebox.showerror("Error", f"Error searching for items: {e}")
            # Log the error for debugging purposes
            print(f"Error searching for items: {e}")

        finally:
            # Close the database connection
            db.close_connection(connection)

    def search_item_by_code(search_param):
        try:
            # Query the database based on the search parameter
            search_results = db.search_inventory_items_by_code(search_param)
            
            if not search_results:
                messagebox.showerror("Error", "Item code does not exist.")
                return

            # Clear the existing items in the GUI table
            clear_table()

            # Populate the GUI table with the search results
            for medicine in search_results:
                # Exclude lot_number from the record before insertion
                record_without_lot_number = medicine[1:]  # Exclude the first element (lot_number)
                self.table.insert('', 'end', values=record_without_lot_number)

            messagebox.showinfo("Success", "Search completed successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Error searching for items: {e}")

    def search_expired_medicines():
        try:
            # Fetch expired medicines from the database
            records = db.fetch_expired_medicines()
            
            # Clear the existing items in the GUI table
            clear_table()

            # Populate the GUI table with the expired medicines
            for medicine in records:
                # Exclude lot_number from the record before insertion
                record_without_lot_number = medicine[1:]  # Exclude the first element (lot_number)
                self.table.insert('', 'end', values=record_without_lot_number)

            messagebox.showinfo("Success", "Expired medicines retrieved successfully")

        except Exception as e:
            messagebox.showerror("Error", f"Error fetching expired medicines: {e}")

    def show_all(): 
        # Clear existing records in the table
        for record in self.table.get_children():
            self.table.delete(record)

        # Fetch all records from the database
        try:
            connection = db.connect_to_database()
            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM inventoryitem")
                records = cursor.fetchall()

                # Insert fetched records into the table
                for record in records:
                    # Exclude lot_number from the record before insertion
                    record_without_lot_number = record[1:]  # Exclude the first element (lot_number)
                    self.table.insert("", "end", values=record_without_lot_number)

        except Exception as e:
            print(f"Error fetching records: {e}")

        finally:
            db.close_connection(connection)
         
    if self.f1:
        self.f1.destroy()
        
    self.f2 = CTkFrame(self.w, width=self.win_width, height=self.win_height, bg_color='transparent')
    self.f2.place(x=0, y=45)

    # ******* LABLE ********************************
    dataframetop = Frame(self.f2,bd=10,bg="#262626")
    dataframetop.place(x=0,y=0,width=self.win_width,height=60)
    customer_lable = CTkLabel(self.f2,text=" Inventory ",
                                font=("Times new roman",35,"underline","bold"),
                                bg_color="#262626",
                                fg_color="transparent",
                                text_color="white")
    customer_lable.place(x=640,y=0)

    # !================ MAIN DATAFRAME ====================
    
    # *------------ left side data frame ---------------------*
    
    detailsframe = Frame(self.f2,bd=0,relief="solid",padx=20,background="#262626")
    detailsframe.place(x=0,y=59,width=self.win_width,height=820)
    
    dataframeleft= CTkFrame(detailsframe,bg_color="#262626",border_width=2,height=650,width=450,border_color="light blue")
    dataframeleft.place(x=0,y=0)
    
    title = CTkLabel(dataframeleft,text="Medicine  Information",
                                font=("Malgun Gothic", 25,"underline","bold"),
                                bg_color="transparent",
                                fg_color="transparent",
                                text_color="white")
    title.place(x=100,y=10)

    
    # #*lables for MEDICINE INFORMARION Information
    
    #     #! ============ ITEM CODE ==========
    
    item_code = CTkLabel(dataframeleft, text="Item code", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    item_code.place(x=25, y=65)
    txt_item_code = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    txt_item_code.place(x=150, y=65)
    
    item_name = CTkLabel(dataframeleft, text="Item name", font=("Microsoft Tai Le MS", 20),fg_color="transparent",bg_color="transparent")
    item_name.place(x=25, y=115)
    txt_item_name = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    txt_item_name.place(x=150, y=115)
    
    Quantity = CTkLabel(dataframeleft, text="Quantity", font=("Microsoft Tai Le MS", 20),fg_color="transparent",bg_color="transparent")
    Quantity.place(x=25, y=175)
    text_Quantity = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    text_Quantity.place(x=150, y=175)
    
    price = CTkLabel(dataframeleft, text="Price", font=("Microsoft Tai Le MS", 20),fg_color="transparent",bg_color="transparent")
    price.place(x=25, y=235)
    txt_price = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    txt_price.place(x=150, y=235)
    
    storeid_code = CTkLabel(dataframeleft, text="Store ID", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    storeid_code.place(x=25, y=295)
    txt_store_code = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    txt_store_code.place(x=150, y=295)
    
    EXP_DATE = CTkLabel(dataframeleft, text="EXP", font=("Microsoft Tai Le MS", 20),fg_color="transparent",bg_color="transparent")
    EXP_DATE.place(x=25, y=355)
    text_EXP_DATE = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    text_EXP_DATE.place(x=150, y=355)
    
    MFG_DATE = CTkLabel(dataframeleft, text="MFG", font=("Microsoft Tai Le MS", 20),fg_color="transparent",bg_color="transparent")
    MFG_DATE.place(x=25, y=415)
    text_MFG_DATE = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    text_MFG_DATE.place(x=150, y=415)
    
    
                # *============================= BUTTONS *=============================
        #**SAVE button**
    btn_save = customtkinter.CTkButton(dataframeleft, text="S A V E",cursor="hand2",font=("Malgun Gothic",15),height=40,width=150,hover_color=("#3AAD0D"),text_color="white",command=save_values)
    btn_save.place(x=45, y=480)
    
    #** SEARCH button
    search_Button =customtkinter.CTkButton(dataframeleft, text="S E A R C H",font=("Malgun Gothic",15),cursor="hand2",height=40,width=150,command=search_item)
    search_Button.place(x=250, y=480)      
    
    #** UPDATE button
    update_Button = customtkinter.CTkButton(dataframeleft, text="U P D A T E",font=("Malgun Gothic",15),cursor="hand2",height=40,width=150,command=update_record)
    update_Button.place(x=45, y=545)
    
    
    #** show_all button
    show_all_Button = customtkinter.CTkButton(dataframeleft, text="S H O W  A L L",font=("Malgun Gothic ",15),cursor="hand2",height=40,width=150,command=show_all)
    show_all_Button.place(x=250, y=545)
    
    #** Clear button
    clear_Button = customtkinter.CTkButton(dataframeleft, text="C L E A R",font=("Malgun Gothic ",15),cursor="hand2",height=40,width=150,hover_color="red")
    clear_Button.place(x=150, y=600)
    
    #             # ! ================= RIGHT DATAFRAME =================
    dataframeright =LabelFrame(detailsframe, bd=5,relief=RIDGE,background="blue")
    dataframeright.place(x=575,y=3,width=1120,height=810)         
        
        # Create horizontal and vertical scrollbars
    Scroll_x = ttk.Scrollbar(dataframeright, orient=HORIZONTAL)
    Scroll_x.pack(side=BOTTOM, fill=X)

    Scroll_y = ttk.Scrollbar(dataframeright, orient=VERTICAL)
    Scroll_y.pack(side=RIGHT, fill=Y)

    # Create the Treeview widget
    self.table = ttk.Treeview(dataframeright, column=("I_CODE", "I_NAME","QUANT.","PRICE" ,"S_ID", "EXP", "MFG"),
                                xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set,show="headings")

    # Configure the scrollbar commands for the Treeview widget
    Scroll_x.config(command=self.table.xview)
    Scroll_y.config(command=self.table.yview)

    # Set headings for the Treeview widget
    self.table.heading("S_ID", text="𝐒 𝐓 𝐎 𝐑 𝐄  𝐈 𝐃")
    self.table.heading("I_CODE", text="𝐈 𝐓 𝐄 𝐌   𝐂 𝐎 𝐃 𝐄")
    self.table.heading("I_NAME", text="𝐈 𝐓 𝐄 𝐌   𝐍 𝐀 𝐌 𝐄")
    self.table.heading("QUANT.", text="𝐐 𝐔 𝐀 𝐍 𝐓 𝐈 𝐓 𝐘")
    self.table.heading("PRICE", text="𝐏 𝐑 𝐈 𝐂 𝐄")
    self.table.heading("EXP", text="𝐄 𝐗 𝐏   𝐃 𝐀 𝐓 𝐄") 
    self.table.heading("MFG", text="𝐌 𝐅 𝐆  𝐃 𝐀 𝐓 𝐄")
    

    # Set column widths for the Treeview widget
    self.table.column("S_ID", width=100)
    self.table.column("I_CODE", width=100)
    self.table.column("I_NAME", width=100)
    self.table.column("PRICE", width=100)
    self.table.column("QUANT.", width=100)
    self.table.column("MFG", width=100)
    self.table.column("EXP", width=100)

    self.table.pack(fill=BOTH, expand=1)         
    self.toggle_win()