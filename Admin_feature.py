from tkinter import *
from tkinter import messagebox
from tkinter import ttk as ttk
import tkinter as tk
import customtkinter 
from customtkinter import *
import Database as db
from datetime import * 
 

def admin_feature(self):   
    
    if self.f1:
        self.f1.destroy()
        
    self.f2 = CTkFrame(self.w, width=self.win_width, height=self.win_height, bg_color='transparent')
    self.f2.place(x=0, y=45)

    # ******* LABLE ********************************
    dataframetop = Frame(self.f2,bd=10,bg="#262626")
    dataframetop.place(x=0,y=0,width=self.win_width,height=60)
    customer_lable = CTkLabel(self.f2,text=" Emplyees Information",
                                font=("Times new roman",30,"underline","bold"),
                                bg_color="#262626",
                                fg_color="transparent",
                                text_color="white")
    customer_lable.place(x=600,y=0)

    def add_employee():
        # Retrieve employee details from entry fields
        first_name = first_name_txt.get()
        last_name = last_name_txt.get()
        phone_number = phone_no_txt.get()
        address = address_txt.get()
        dob = date_of_birth_txt.get()
        date_of_hire = date_of_hire_txt.get()
        salary = salary_txt.get()
        emp_username = emp_username_txt.get()
        access_level = access_level_txt.get()

        # Validate input fields
        if not first_name or not last_name or not phone_number or not address or not dob or not date_of_hire or not salary or not emp_username or not access_level:
                messagebox.showerror("Error", "All fields are required")
                return
        
        # Insert employee details into the database
        db.insert_employee( emp_username,first_name, last_name, phone_number, address, dob, date_of_hire, salary, access_level)

        # Clear input fields after adding employee
        clear_input_fields()
        
        # message box to show that the employee has been added
        messagebox.showinfo("Success", "Employee added successfully")
        
        # Display employee details in the table
        inserted_employee = db.get_employee(emp_username)  # Implement this method in your Database module
        
        if not inserted_employee:
                messagebox.showerror("Error", "Employee not found")
                return
        
        # clear the table
        for row in self.table.get_children():
                self.table.delete(row)

        self.table.insert("", "end", values=inserted_employee)
                
    def display_employee_details():
        try:
            # Fetch employee details from the database
            employee_details = db.get_all_employees()  # Assuming this method fetches all employees from the database

            if not employee_details:
                    messagebox.showinfo("Info", "No employee details found")
                    return
            
            # Clear existing table data
            for row in self.table.get_children():
                    self.table.delete(row)

            # Populate the table with employee details
            for employee in employee_details:
                    self.table.insert("", "end", values=employee)

        except Exception as e:
            print("Error:", e)
                    
    def update_employee():
        try:
            # Get the selected item from the GUI table
            selected_item = self.table.selection()
            if not selected_item:
                messagebox.showerror("Error", "Please select an employee to update")
                return
            
            # Retrieve the values entered by the user for update
            updated_values = {
                "emp_username": emp_username_txt.get(),
                "first_name": first_name_txt.get(),
                "last_name": last_name_txt.get(),
                "phone_number": phone_no_txt.get(),
                "address": address_txt.get(),
                "date_of_birth": date_of_birth_txt.get(),
                "date_of_hire": date_of_hire_txt.get(),
                "salary": salary_txt.get(),
                "access_level": access_level_txt.get()
            }

            # Construct the UPDATE query
            update_query = "UPDATE Employee SET "
            update_query += ", ".join([f"{key} = %s" for key in updated_values.keys()])
            update_query += " WHERE emp_username = %s"

            # Retrieve the emp_username of the selected employee
            emp_username = self.table.item(selected_item, "values")[0]

            # Prepare the data to be updated
            update_data = tuple(updated_values.values()) + (emp_username,)

            # Connect to the database
            conn = db.connect_to_database()

            # Create a cursor object to execute SQL queries
            cursor = conn.cursor()

            # Execute the UPDATE query
            cursor.execute(update_query, update_data)

            # Commit changes to the database
            conn.commit()

            # Close cursor and database connection
            cursor.close()
            db.close_connection(conn)

            # Refresh the GUI table to reflect the changes
            display_employee_details()

            # Show success message
            messagebox.showinfo("Success", "Employee details updated successfully")


        except Exception as e:
            print("Error updating employee details:", e)


        
                
                        
        
                        
    def clear_input_fields():
        # Clear the contents of specific Entry widgets or input fields
        first_name_txt.delete(0, tk.END)
        last_name_txt.delete(0, tk.END)
        phone_no_txt.delete(0, tk.END)
        address_txt.delete(0, tk.END)
        date_of_birth_txt.delete(0, tk.END)
        date_of_hire_txt.delete(0, tk.END)
        salary_txt.delete(0, tk.END)
        emp_username_txt.delete(0, tk.END)
        # Clear the selection in the Access Level combo box
        access_level_txt.set('')


    
    # !================ MAIN DATAFRAME ====================
    
    # *------------ left side data frame ---------------------*
    
    detailsframe = Frame(self.f2,bd=0,relief="solid",padx=20,background="#262626")
    detailsframe.place(x=0,y=59,width=self.win_width,height=820)
    
    dataframeleft= CTkFrame(detailsframe,bg_color="#262626",border_width=2,
                            height=400,
                            width=1370,
                            border_color="light blue")
    dataframeleft.place(x=0,y=0)
    
    emp_deteails = CTkLabel(dataframeleft,text="Emplyees Details",
                                font=("Malgun Gothic", 25,"underline","bold"),
                                bg_color="transparent",
                                fg_color="transparent",
                                text_color="white")
    emp_deteails.place(x=260,y=10)
    
  
    #! ============ Seperator ==========
    seperator = ttk.Separator(dataframeleft, orient=VERTICAL)
    seperator.place(x=950, y=0, relheight=0.8,rely=0.1)
    
    # #*lables for MEDICINE INFORMARION Information
    
#     #     #! ============ First name ==========
    emp_username_entry = CTkLabel(dataframeleft, text="Username", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    emp_username_entry.place(x=75, y=65)
    emp_username_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    emp_username_txt.place(x=20, y=95)  

        #! ============ Last name ==========

    first_name_entry = CTkLabel(dataframeleft, text="First Name", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    first_name_entry.place(x=310, y=65)
    first_name_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    first_name_txt.place(x=260, y=95)
    
            #! ============ Phone Number ==========    
    lastname_entry = CTkLabel(dataframeleft, text="Last Number", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    lastname_entry.place(x=545, y=65)
    last_name_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    last_name_txt.place(x=500, y=95)

            #! ============ Address ==========
    phone_no_entry = CTkLabel(dataframeleft, text="Phone Number", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    phone_no_entry.place(x=75, y=155)
    phone_no_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    phone_no_txt.place(x=20, y=185)

            #! ============ Date of Birth ==========
    address = CTkLabel(dataframeleft, text="Address", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    address.place(x=310, y=155)
    address_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    address_txt.place(x=260, y=185)
    
    
            #! ============ Date of Hire ==========
    date_of_birth = CTkLabel(dataframeleft, text="Date of Birth", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    date_of_birth.place(x=545, y=155)
    date_of_birth_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    date_of_birth_txt.place(x=500, y=185)
    
    
            #! ============ Salary ==========
    date_of_hire = CTkLabel(dataframeleft, text="Date of Hire", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    date_of_hire.place(x=75, y=245)
    date_of_hire_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    date_of_hire_txt.place(x=20, y=275)
    
    
            #! ============ Employee Username ==========
    salary = CTkLabel(dataframeleft, text="Salary", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    salary.place(x=310, y=245)
    salary_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    salary_txt.place(x=260, y=275)
    
    
            #! ============ Access Level ==========
    acesslevel = CTkLabel(dataframeleft, text="Access Level", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    acesslevel.place(x=545, y=245)
    access_level_txt = CTkComboBox(master=dataframeleft,
                                values=["Admin", "Employee"],
                                width=210,height=38,
                                border_color="light blue",
                                font=("Microsoft Tai Le",15,"bold"),
                                corner_radius=5,
                                dropdown_text_color="white",
                                dropdown_fg_color="#262626",
                                border_width=2,
                                state="readonly",
                                dropdown_hover_color="light blue",
                                justify="center")
    access_level_txt.place(x=500, y=275)
    
    
                # *============================= BUTTONS *=============================
        #**SAVE button**
    btn_save = customtkinter.CTkButton(dataframeleft, text="S A V E",cursor="hand2",font=("Malgun Gothic",15),height=40,width=120,hover_color=("#3AAD0D"),text_color="white",command=add_employee)
    btn_save.place(x=15, y=340)
    
    # # #** UPDATE button
    update_Button = customtkinter.CTkButton(dataframeleft, text="U P D A T E",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,command=update_employee)
    update_Button.place(x=160, y=340)
  
    
    #  #** SEARCH button
    search_Button = customtkinter.CTkButton(dataframeleft, text="S E A R C H",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120)
    search_Button.place(x=310, y=340)
   
    
    
    # *** Show All button
    show_all = customtkinter.CTkButton(dataframeleft, text="S H O W  A L L",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,text_color="white",command=display_employee_details)
    show_all.place(x=460, y=340)
    
    #** Delete button#*
    delete = customtkinter.CTkButton(dataframeleft, text="D E L E T E",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,hover_color=("#FF0000"))
    delete.place(x=610, y=340)
    
    #** clear button
    clear = customtkinter.CTkButton(dataframeleft, text="C L E A R",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,hover_color=("#FF0000"),command=clear_input_fields)
    clear.place(x=830, y=340)
    
    
    #** set password button
    set_password = customtkinter.CTkButton(dataframeleft, text="S E T",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,hover_color=("#3AAD0D"),text_color="white")
    set_password.place(x=1000, y=340)
    
    
    #** reset password button
    reset_password = customtkinter.CTkButton(dataframeleft, text="R E S E T",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,hover_color=("#FF0000"),text_color="white")
    reset_password.place(x=1170, y=340)
    
    #*============================= Buttons end =================
    
    update_password = CTkLabel(dataframeleft,text="Update Password",
                                font=("Malgun Gothic", 25,"underline","bold"),
                                bg_color="transparent",
                                fg_color="transparent",
                                text_color="white")
    update_password.place(x=980,y=10)
    
    
    Username = CTkLabel(dataframeleft, text="Username", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    Username.place(x=890, y=65)
    emp_username_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    emp_username_txt.place(x=830, y=95)
    
    password = CTkLabel(dataframeleft, text="Password", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    password.place(x=1145, y=65)
    password_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    password_txt.place(x=1090, y=95)
    
    confirm_password = CTkLabel(dataframeleft, text="Confirm Password", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    confirm_password.place(x=850, y=155)
    confirm_password_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    confirm_password_txt.place(x=830, y=185)
    
    Admin_pass = CTkLabel(dataframeleft, text="Admin Password", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    Admin_pass.place(x=1130, y=155)
    admin_pass_txt = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
    admin_pass_txt.place(x=1090, y=185)
    
   
          # ! ================= RIGHT DATAFRAME =================
    
    style = ttk.Style()
    style.theme_use("clam")
    
    dataframeright =Frame(self.f2, bd=5,relief="groove",bg="#262626",background="light blue")
    dataframeright.place(x=10,y=565,width=1730,height=310)      
        
        # Create horizontal and vertical scrollbars
    Scroll_x = ttk.Scrollbar(dataframeright, orient=HORIZONTAL)
    Scroll_x.pack(side=BOTTOM, fill=X)

    Scroll_y = ttk.Scrollbar(dataframeright, orient=VERTICAL)
    Scroll_y.pack(side=RIGHT, fill=Y)

    #* Create the Treeview widget
    self.table = ttk.Treeview(dataframeright, column=( "EmpUsername","first_name_entry", "LastName", "PhoneNumber", "Address", "DateOfBirth", "DateOfHire", "Salary", "AccessLevel"),
                                xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set,show="headings")

    #* Configure the scrollbar commands for the Treeview widget
    Scroll_x.config(command=self.table.xview)
    Scroll_y.config(command=self.table.yview)

    # *Set headings for the Treeview widget
    self.table.heading("EmpUsername", text="𝐄 𝐌 𝐏. 𝐔 𝐒 𝐄 𝐑 𝐍 𝐀 𝐌 𝐄",anchor="center")
    self.table.heading("first_name_entry", text="𝐅 𝐈 𝐑 𝐒 𝐓  𝐍 𝐀 𝐌 𝐄",anchor="center")
    self.table.heading("LastName", text="𝐋 𝐀 𝐒 𝐓  𝐍 𝐀 𝐌 𝐄",anchor="center")
    self.table.heading("PhoneNumber", text="𝐏 𝐇 𝐎 𝐍 𝐄  𝐍 𝐔 𝐌 𝐁 𝐄 𝐑.",anchor="center")
    self.table.heading("Address", text="𝐀 𝐃 𝐃 𝐑 𝐄 𝐒 𝐒",anchor="center")
    self.table.heading("DateOfBirth", text="𝐃 𝐀 𝐓 𝐄  𝐎 𝐅  𝐁 𝐈 𝐑 𝐓 𝐇",anchor="center")
    self.table.heading("DateOfHire", text="𝐃 𝐀 𝐓 𝐄  𝐎 𝐅  𝐇 𝐈 𝐑 𝐄",anchor="center")
    self.table.heading("Salary", text="𝐒 𝐀 𝐋 𝐀 𝐑 𝐘",anchor="center")
    self.table.heading("AccessLevel", text="𝐀 𝐂 𝐂 𝐄 𝐒 𝐒  𝐋 𝐀 𝐕 𝐄 𝐋",anchor="center")
    
    # *Set column widths for the Treeview widget
    self.column_widths = [100, 100, 100, 100, 100, 100, 100, 100, 100]

    self.table.column("EmpUsername", width=self.column_widths[0])
    self.table.column("first_name_entry", width=self.column_widths[1])
    self.table.column("LastName", width=self.column_widths[2])
    self.table.column("PhoneNumber", width=self.column_widths[3])
    self.table.column("Address", width=self.column_widths[4])
    self.table.column("DateOfBirth", width=self.column_widths[5])
    self.table.column("DateOfHire", width=self.column_widths[6])
    self.table.column("Salary", width=self.column_widths[7])
    self.table.column("AccessLevel", width=self.column_widths[8])
    self.table.pack(fill=BOTH, expand=True)

    self.toggle_win()


