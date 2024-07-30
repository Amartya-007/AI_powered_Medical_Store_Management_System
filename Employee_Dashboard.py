from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import ttk as ttk
from customtkinter import *
import customtkinter
from datetime import *
import Customer,Inventory,Reports,Supplier,Billing,employee
from main import LoginSignupPage

class MedicalStoreApp:
    def __init__(self):
        self.w = customtkinter.CTk()

        self.w.geometry('1400x750+80+30')
        self.w.resizable(0,0)
        # customtkinter.set_default_color_theme('dark-blue')  # Set default color theme to white
        self.w.title('Shri Hari Medical Store')
    
        self.w.iconbitmap(r"Assets\logo.ico")
        # Set window icon
        icon_img = Image.open(r"Assets\image_2.png")
        self.icon_photo = ImageTk.PhotoImage(icon_img)
        self.w.iconphoto(False, self.icon_photo)
        
        self.f1 = None  # Define f1 at the beginning
        self.win_height = self.w.winfo_height()
        self.win_width = self.w.winfo_width()
        self.w.config(bg="#262626")
        self.default_home()

    def customer_info(self):
        Customer.customer_info(self)

    def inventory(self):
        Inventory.inventory(self)

    def suppliers(self):
        Supplier.supplier(self)
        
    def reports(self):
        Reports.reports(self)

    def billing(self):
        Billing.billing(self)    
        
    def admin_feature(self):
        employee.admin_feature(self)
        
        
    def logout(self):
        if self.f1:
            self.f1.destroy()
        result = messagebox.askquestion("Logout", "Are you sure you want to log out?")
        if result == "yes":
            self.w.destroy()  # Close the current Toplevel window
            # Create a new instance of the LoginSignupPage class to display the login page
            login_page = LoginSignupPage()
            login_page.mainloop()

                  
    def dele(self):
        if self.f1:
            self.f1.destroy()
            icon_img = Image.open(r"Assets\open.png")
            icon_img = icon_img.resize((45, 45))
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            b2 = Button(self.w, image=self.icon_photo,
                        command=self.toggle_win,
                        border=0,
                        bg='#262626',
                        activebackground='#262626')
            b2.image = self.icon_photo
            b2.place(x=12, y=8)
            
            
    def toggle_win(self):
        if self.f1:
            self.f1.destroy()
            self.f1 = None
        else:
            window_height = self.w.winfo_height()
            
            self.f1 = Frame(self.w, width=300, height=window_height, bg='#12c4c0')
            self.f1.place(x=0, y=0)
            lb1 = CTkLabel(self.w, text="𝐒𝐇𝐑𝚰 𝐇𝐀𝐑𝚰 𝐌𝐄𝐃𝚰𝐂𝐀𝐋 𝐒𝐓𝐎𝐑𝐄", bg_color='#262626', font=("Microsoft JhengHei UI Bold",33, "bold"))
            lb1.place(x=575, y=0)
            lb2 = CTkLabel(self.w, text="( E M P L O Y E E )", bg_color='#262626', font=("Microsoft JhengHei UI Bold",28, "bold"),text_color="#12c4c0")
            lb2.place(x=1000,y=5)
            img1 = Image.open(r"Assets\image_2.png")
            img1 = img1.resize((45, 45))
            self.photoimg1 = ImageTk.PhotoImage(img1)
            logo_label = Label(self.w, image=self.photoimg1, bg='#262626', activebackground='#3FDFBA')
            logo_label.place(x=650, y=2)

            def bttn(x, y, text, bcolor, fcolor, cmd):
                def on_entera(e):
                    myButton1['background'] = bcolor
                    myButton1['foreground'] = '#262626'

                def on_leavea(e):
                    myButton1['background'] = fcolor
                    myButton1['foreground'] = '#262626'

                myButton1 = Button(self.f1, text=text,
                                width=42,
                                height=2,
                                fg='#262626',
                                font=("Segoe UI Bold",10,"bold"),
                                border=0,
                                bg=fcolor,
                                activeforeground='#262626',
                                activebackground=bcolor,  # Darker shade of blue
                                command=cmd)
                myButton1.bind("<Enter>", on_entera)
                myButton1.bind("<Leave>", on_leavea)
                myButton1.place(x=x, y=y)

            bttn(0, 120, 'C U S T O M E R   I N F O', '#0f9d9a', '#12c4c0', self.customer_info)
            bttn(0, 200, 'I N V E N T O R Y', '#0f9d9a', '#12c4c0', self.inventory)
            bttn(0, 280, 'S U P P L I E R S', '#0f9d9a', '#12c4c0', self.suppliers)
            bttn(0, 360, 'R E P O R T S', '#0f9d9a', '#12c4c0', self.reports)
            bttn(0, 440, 'B I L L I N G', '#0f9d9a', '#12c4c0', self.billing)
            # bttn(0, 520, 'A D M I N  F E A T U R E', '#0f9d9a', '#12c4c0', self.admin_feature)
            bttn(0, 780, 'L O G O U T', 'red', '#12c4c0', self.logout)

            global img2
            img2 = ImageTk.PhotoImage(Image.open(r"Assets\close.png"))
            Button(self.f1,
                image=img2,
                border=0,
                command=self.dele,
                bg='#12c4c0',
                activebackground='#12c4c0',
                activeforeground='#12c4c0').place(x=12, y=10)



    def default_home(self):
        self.customer_info()

    def run(self):
        # Open the image
        image = Image.open(r"Assets\open.png")
        image = image.resize((35,35))
        global img1
        img1 = ImageTk.PhotoImage(image)
        b2 = Button(self.w, image=img1,
                    command=self.toggle_win,
                    border=0,
                    bg='#262626',
                    activebackground='#262626')
        b2.place(x=12, y=8)
        self.w.mainloop()

# app = MedicalStoreApp()
# app.run()
