from tkinter import *
from tkinter import messagebox
from tkinter import ttk as ttk
import customtkinter 
from customtkinter import *
import Database as db
from datetime import * 

def supplier(self):
    
    def clear_table():
        self.table.delete(*self.table.get_children())
        
    def show_all_button():
        clear_table()
        values = db.show_all_suppliers()
        if values:
            for value in values:
                self.table.insert("", "end", values=value)
        else:
            messagebox.showinfo("No data", "No data available")
        
    def save_button():
        suppliers_id = txt_suppliers_id.get()
        Supplier_name = txt_Supplier_name.get()
        contact = txt_contact.get()
        
        if suppliers_id and Supplier_name and contact:
            db.add_to_supplier(suppliers_id, Supplier_name, contact)
            messagebox.showinfo("Success", "Supplier added successfully")
            clear_table()
            show_all_button()
        else:
            messagebox.showerror("Error", "All fields are required")
            
    def update_button():
        suppliers_id = txt_suppliers_id.get()
        Supplier_name = txt_Supplier_name.get()
        contact = txt_contact.get()
        
        if suppliers_id:
            update_data = {}  # Create a dictionary to store the fields to be updated
            if Supplier_name:
                update_data['SupplierName'] = Supplier_name  # Add SupplierName to update_data if not empty
            if contact:
                update_data['ContactInfo'] = contact  # Add ContactInfo to update_data if not empty
            
            if update_data:  # Check if there are fields to update
                db.update_supplier(suppliers_id, **update_data)  # Pass the update_data dictionary to the update_supplier function
                messagebox.showinfo("Success", "Supplier updated successfully")
                clear_table()
                show_all_button()
            else:
                messagebox.showerror("Error", "At least one field is required")  # Show error if no fields are entered
        else:
            messagebox.showerror("Error", "Supplier ID is required")  # Show error if SupplierID is not entered

            
            
    if self.f1:
        self.f1.destroy()
    self.f2 = CTkFrame(self.w, width=self.win_width, height=self.win_height, bg_color='transparent')
    self.f2.place(x=0, y=45)



    # ******* LABLE ********************************
    dataframetop = Frame(self.f2,bd=10,bg="#262626")
    dataframetop.place(x=0,y=0,width=self.win_width,height=60)
    customer_lable = CTkLabel(self.f2,text="SUPPLIERS",
                                font=("Times new roman", 30,"underline","bold"),
                                bg_color="#262626",
                                fg_color="transparent",
                                text_color="white")
    customer_lable.place(x=640,y=5)
    
        # !================ MAIN DATAFRAME ====================
    
    # *------------ left side data frame ---------------------*
    
    detailsframe = Frame(self.f2,bd=0,relief="solid",padx=20,background="#262626")
    detailsframe.place(x=0,y=59,width=self.win_width,height=820)
    
    dataframeleft= CTkFrame(detailsframe,bg_color="#262626",border_width=2,height=650,width=450,border_color="light blue")
    dataframeleft.place(x=0,y=0)
    
    title = CTkLabel(dataframeleft,text="Suppliers Details",
                                font=("Malgun Gothic", 25,"underline","bold"),
                                bg_color="transparent",
                                fg_color="transparent",
                                text_color="white")
    title.place(x=100,y=15)

    
    # #*lables for MEDICINE INFORMARION Information
    
    #     #! ============ ITEM CODE ==========
    suppliers_id = CTkLabel(dataframeleft, text="Suppliers ID", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    suppliers_id.place(x=25, y=85)
    txt_suppliers_id = CTkEntry(dataframeleft, font=("Malgun Gothic", 18),width=210,height=38,border_color="light blue")
    txt_suppliers_id.place(x=150, y=85)
    
    Supplier_name = CTkLabel(dataframeleft, text="Sup. name", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    Supplier_name.place(x=25, y=175)
    txt_Supplier_name = CTkEntry(dataframeleft, font=("Malgun Gothic", 18),width=210,height=38,border_color="light blue")
    txt_Supplier_name.place(x=150, y=175)
    
    
    contact = CTkLabel(dataframeleft, text="Contact", font=("Microsoft Tai Le", 20),fg_color="transparent",bg_color="transparent")
    contact.place(x=25, y=275)
    txt_contact = CTkEntry(dataframeleft, font=("Malgun Gothic", 18),width=210,height=38,border_color="light blue")
    txt_contact.place(x=150, y=275)
    
    
    
                # *============================= BUTTONS *=============================
        #**SAVE button**
    btn_save = customtkinter.CTkButton(dataframeleft, text="S A V E",cursor="hand2",font=("Malgun Gothic",15),height=40,width=150,hover_color=("#00cc66"),text_color="white",command=save_button)
    btn_save.place(x=45, y=430)
    
    #** UPDATE button
    update_Button = customtkinter.CTkButton(dataframeleft, text="U P D A T E",font=("Malgun Gothic",15),cursor="hand2",height=40,width=150,command=update_button)
    update_Button.place(x=45, y=500)
    
    
    #** SEARCH button
    search_Button =customtkinter.CTkButton(dataframeleft, text="S E A R C H",font=("Malgun Gothic",15),cursor="hand2",height=40,width=150)
    search_Button.place(x=250, y=430)      
    
    #** show_all button
    show_all_Button = customtkinter.CTkButton(dataframeleft, text="S H O W  A L L",font=("Malgun Gothic",15),cursor="hand2",height=40,width=150,command=show_all_button)
    show_all_Button.place(x=250, y=500)
    
    #** Exit button
    exit_Button = customtkinter.CTkButton(dataframeleft, text="E X I T",font=("Malgun Gothic",15),cursor="hand2",height=40,width=150,hover_color="red")
    exit_Button.place(x=150, y=590)
    
    #             # ! ================= RIGHT DATAFRAME =================
    dataframeright =LabelFrame(detailsframe, bd=5,relief=RIDGE,background="blue")
    dataframeright.place(x=575,y=3,width=1120,height=810)         
        
        # Create horizontal and vertical scrollbars
    Scroll_x = ttk.Scrollbar(dataframeright, orient=HORIZONTAL)
    Scroll_x.pack(side=BOTTOM, fill=X)

    Scroll_y = ttk.Scrollbar(dataframeright, orient=VERTICAL)
    Scroll_y.pack(side=RIGHT, fill=Y)

    self.table = ttk.Treeview(dataframeright, column=("Suppliers ID", "Suppliers Name", "Contact"), xscrollcommand=Scroll_x.set, yscrollcommand=Scroll_y.set)
    Scroll_x.config(command=self.table.xview)
    Scroll_y.config(command=self.table.yview)

    self.table.heading("Suppliers ID", text="𝐒 𝐔 𝐏 𝐏 𝐋 𝐈 𝐄 𝐑 𝐒   𝐈 𝐃 ")
    self.table.heading("Suppliers Name", text="𝐒 𝐔 𝐏 𝐏 𝐋 𝐈 𝐄 𝐑 𝐒   𝐍 𝐀 𝐌 𝐄")
    self.table.heading("Contact", text="𝐂 𝐎 𝐍 𝐓 𝐀 𝐂 𝐓")
    self.table['show'] = 'headings'

    self.table.column("Suppliers ID", width=100)
    self.table.column("Suppliers Name", width=120)
    self.table.column("Contact", width=100)

    self.table.pack(fill=BOTH, expand=1)

    
        
            
                
                
    self.toggle_win()
