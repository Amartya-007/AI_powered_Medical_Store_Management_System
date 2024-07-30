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
        
        
        
        def add_employee():
                # Retrieve employee details from entry fields
                first_name = text_FirstName.get()
                last_name = text_LastName.get()
                phone_number = txt_PhoneNumber.get()
                address = txt_Address.get()
                dob = text_DateOfBirth.get()
                date_of_hire = text_DateOfHire.get()
                salary = txt_Salary.get()
                emp_username = txt_EmpUsername.get()
                access_level = txt_AccessLevel.get()

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
                
                # Update Employee functionality
        def update_employee():
                # Retrieve updated employee details from entry fields
                # Update employee details in the database
                pass  # Implement this based on your database structure

                # Delete Employee functionality
        def delete_employee():
                pass
                # # Retrieve employee username to delete
                # emp_username = txt_EmpUsername.get()
                # # Delete employee from the database
                # db.delete_employee(emp_username)

                # # Clear input fields after deleting employee
                # clear_input_fields()

                # # Set/Reset Password functionality
        def set_reset_password():
                pass
                # # Retrieve employee username and new password from entry fields
                # emp_username = text_Username.get()
                # new_password = text_Password.get()
                # # Update employee password in the database
                # db.update_password(emp_username, new_password)

                # # Clear input fields after setting/resetting password
                # clear_input_fields()

                # # Display Employee Details in Table
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


        # ******* LABLE ********************************
        dataframetop = Frame(self.f2,bd=10,bg="#262626")
        dataframetop.place(x=0,y=0,width=self.win_width,height=60)
        customer_lable = CTkLabel(self.f2,text=" Emplyees Information",
                                        font=("Times new roman",30,"underline","bold"),
                                        bg_color="#262626",
                                        fg_color="transparent",
                                        text_color="white")
        customer_lable.place(x=600,y=0)


        def clear_input_fields():
                # Clear the contents of specific Entry widgets or input fields
                text_FirstName.delete(0, tk.END)
                text_LastName.delete(0, tk.END)
                txt_PhoneNumber.delete(0, tk.END)
                txt_Address.delete(0, tk.END)
                text_DateOfBirth.delete(0, tk.END)
                text_DateOfHire.delete(0, tk.END)
                txt_Salary.delete(0, tk.END)
                txt_EmpUsername.delete(0, tk.END)
                # Clear the selection in the Access Level combo box
                txt_AccessLevel.set('')
                

                


        # !================ MAIN DATAFRAME ====================

        # *------------ left side data frame ---------------------*

        detailsframe = Frame(self.f2,bd=0,relief="solid",padx=20,background="#262626")
        detailsframe.place(x=0,y=59,width=self.win_width,height=820)

        dataframeleft= CTkFrame(detailsframe,bg_color="#262626",border_width=2,
                                height=650,
                                width=730,
                                border_color="light blue")
        dataframeleft.place(x=0,y=0)

        title = CTkLabel(dataframeleft,text="Emplyees Details",
                                        font=("Malgun Gothic", 25,"underline","bold"),
                                        bg_color="transparent",
                                        fg_color="transparent",
                                        text_color="white")
        title.place(x=260,y=10)


        # #*lables for MEDICINE INFORMARION Information

        #     #! ============ First name ==========
        FirstName = CTkLabel(dataframeleft, text="First Name", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        FirstName.place(x=75, y=65)
        text_FirstName = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_FirstName.place(x=20, y=95)

                #! ============ Last name ==========
        LastName = CTkLabel(dataframeleft, text="Last Name", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        LastName.place(x=310, y=65)
        text_LastName = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_LastName.place(x=260, y=95)

                #! ============ Phone Number ==========    
        phone = CTkLabel(dataframeleft, text="Phone Number", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        phone.place(x=545, y=65)
        txt_PhoneNumber = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        txt_PhoneNumber.place(x=500, y=95)

                #! ============ Address ==========
        address = CTkLabel(dataframeleft, text="Address", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        address.place(x=75, y=155)
        txt_Address = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        txt_Address.place(x=20, y=185)

                #! ============ Date of Birth ==========
        DOB = CTkLabel(dataframeleft, text="Date of Birth", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        DOB.place(x=310, y=155)
        text_DateOfBirth = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_DateOfBirth.place(x=260, y=185)


                #! ============ Date of Hire ==========
        date_of_hire = CTkLabel(dataframeleft, text="Date of Hire", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        date_of_hire.place(x=545, y=155)
        text_DateOfHire = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_DateOfHire.place(x=500, y=185)


                #! ============ Salary ==========
        salary = CTkLabel(dataframeleft, text="Salary", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        salary.place(x=75, y=245)
        txt_Salary = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        txt_Salary.place(x=20, y=275)


                #! ============ Employee Username ==========
        empUsername = CTkLabel(dataframeleft, text="Emp. Username", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        empUsername.place(x=310, y=245)
        txt_EmpUsername = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        txt_EmpUsername.place(x=260, y=275)


                #! ============ Access Level ==========
        acesslevel = CTkLabel(dataframeleft, text="Access Level", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        acesslevel.place(x=545, y=245)
        txt_AccessLevel = CTkComboBox(master=dataframeleft,
                                        values=["Admin", "Employee"],
                                        width=200,height=38,
                                        border_color="light blue",
                                        font=("Microsoft Tai Le",15,"bold"),
                                        corner_radius=5,
                                        dropdown_text_color="white",
                                        dropdown_fg_color="#262626",
                                        border_width=2,
                                        state="readonly",
                                        dropdown_hover_color="light blue",
                                        justify="center")
        txt_AccessLevel.place(x=500, y=275)


                        # *============================= BUTTONS *=============================
                #**SAVE button**
        btn_save = customtkinter.CTkButton(dataframeleft, text="S A V E",cursor="hand2",font=("Malgun Gothic",15),height=40,width=120,hover_color=("#3AAD0D"),text_color="white",)
        btn_save.place(x=50, y=340)

        # # #** UPDATE button
        update_Button = customtkinter.CTkButton(dataframeleft, text="U P D A T E",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120)
        update_Button.place(x=220, y=340)

        #  #** SEARCH button
        search_Button = customtkinter.CTkButton(dataframeleft, text="S E A R C H",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120)
        search_Button.place(x=390, y=340)

        # #** Delete button
        delete_Button = customtkinter.CTkButton(dataframeleft, text="D E L E T E",font=("Malgun Gothic",15),cursor="hand2",height=40,width=120,hover_color=("#FF0000"),text_color="white")
        delete_Button.place(x=560, y=340)

        seperator = ttk.Separator(dataframeleft, orient=HORIZONTAL)
        seperator.place(x=0, y=525,relx=0.1, relwidth=0.8)

        update_emplyee_details = CTkLabel(dataframeleft,text=" Update Password ",
                                        font=("Malgun Gothic", 25,"bold"),
                                        bg_color="transparent",
                                        fg_color="transparent",
                                        text_color="white")
        update_emplyee_details.place(x=260,y=400)

        Username = CTkLabel(dataframeleft, text="Username", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        Username.place(x=10, y=455)
        text_Username = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_Username.place(x=140, y=450)

        password = CTkLabel(dataframeleft, text="Password", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        password.place(x=378, y=455)
        text_Password = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_Password.place(x=500, y=450)

        confirm_password = CTkLabel(dataframeleft, text="Confirm-Pass.", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        confirm_password.place(x=10, y=515)
        text_confirm_password = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_confirm_password.place(x=140, y=510)

        Admin_pass = CTkLabel(dataframeleft, text="Admin_Pass.", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
        Admin_pass.place(x=378, y=515)
        text_Admin_pass = CTkEntry(dataframeleft, font=("Microsoft Tai Le MS", 18),width=210,height=38,border_color="light blue")
        text_Admin_pass.place(x=500, y=510)

        set_password = customtkinter.CTkButton(dataframeleft, text="S E T / R E S E T",font=("Malgun Gothic",15),cursor="hand2",height=40,width=250,hover_color=("#3AAD0D"),text_color="white")
        set_password.place(x=230, y=580)

        set_password.configure(command=display_employee_details)
        btn_save.configure(command=add_employee)
        update_Button.configure(command=update_employee)
        delete_Button.configure(command=delete_employee)
        set_password.configure(command=set_reset_password)
        search_Button.configure(command=display_employee_details)

                # ! ================= RIGHT DATAFRAME =================
        style = ttk.Style()
        style.theme_use("clam")

        dataframeright =Frame(detailsframe, bd=5,relief="groove",bg="#262626",background="light blue")
        dataframeright.place(x=930,y=0,width=775,height=810)      
                
                # Create horizontal and vertical scrollbars
        Scroll_x = ttk.Scrollbar(dataframeright, orient=HORIZONTAL)
        Scroll_x.pack(side=BOTTOM, fill=X)

        Scroll_y = ttk.Scrollbar(dataframeright, orient=VERTICAL)
        Scroll_y.pack(side=RIGHT, fill=Y)

        #* Create the Treeview widget
        self.table = ttk.Treeview(dataframeright, column=("EmpUsername","FirstName", "LastName", "PhoneNumber", "Address", "DateOfBirth", "DateOfHire", "Salary",  "AccessLevel"),
                                        xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set,show="headings")

        #* Configure the scrollbar commands for the Treeview widget
        Scroll_x.config(command=self.table.xview)
        Scroll_y.config(command=self.table.yview)

        # *Set headings for the Treeview widget
        self.table.heading("FirstName", text="𝐅 𝐈 𝐑 𝐒 𝐓  𝐍 𝐀 𝐌 𝐄",anchor="center")
        self.table.heading("LastName", text="𝐋 𝐀 𝐒 𝐓  𝐍 𝐀 𝐌 𝐄",anchor="center")
        self.table.heading("PhoneNumber", text="𝐏  𝐍 𝐎.",anchor="center")
        self.table.heading("Address", text="𝐀 𝐃 𝐃 𝐑 𝐄 𝐒 𝐒",anchor="center")
        self.table.heading("DateOfBirth", text="𝐃 𝐎 𝐁",anchor="center")
        self.table.heading("DateOfHire", text="𝐃 𝐎 𝐇",anchor="center")
        self.table.heading("Salary", text="𝐒 𝐀 𝐋 𝐀 𝐑 𝐘",anchor="center")
        self.table.heading("EmpUsername", text="𝐄 𝐌 𝐏. 𝐔 𝐒 𝐄 𝐑 𝐍 𝐀 𝐌 𝐄",anchor="center")
        self.table.heading("AccessLevel", text="𝐀 𝐂 𝐂 𝐄 𝐒 𝐒  𝐋 𝐀 𝐕 𝐄 𝐋",anchor="center")

        # *Set column widths for the Treeview widget
        self.column_widths = [150, 150, 150, 150, 150, 150, 150, 150, 150]

        self.table.column("FirstName", width=self.column_widths[0],stretch=NO)
        self.table.column("LastName", width=self.column_widths[1],stretch=NO)
        self.table.column("PhoneNumber", width=self.column_widths[2],stretch=NO)
        self.table.column("Address", width=self.column_widths[3],stretch=NO)
        self.table.column("DateOfBirth", width=self.column_widths[4],stretch=NO)
        self.table.column("DateOfHire", width=self.column_widths[5],stretch=NO)
        self.table.column("Salary", width=self.column_widths[6],stretch=NO)
        self.table.column("EmpUsername", width=self.column_widths[7],stretch=NO)
        self.table.column("AccessLevel", width=self.column_widths[8],stretch=NO)

        self.table.pack(fill=BOTH, expand=1)

        self.toggle_win()