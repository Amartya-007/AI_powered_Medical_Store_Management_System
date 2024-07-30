import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import Database as db


class LoginSignupPage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x600+590+140")
        self.resizable(0,0)
        self.title("Login to Shri Hari Medical Store")

        self.iconbitmap(r"Assets\logo.ico")
                                        
        # setting the title 
        self.title_label = ctk.CTkLabel(master=self, text="SHRI HARI MEDICAL STORE ", font=("Arial", 28, "bold", "italic", "bold"), text_color="white")
        self.title_label.place(x=150, y=20)
        
        # title logo setting beside the title
        img1 = Image.open(r"Assets\logo.ico")
        img1 = img1.resize((60,60))
        self.photoimg1 = ImageTk.PhotoImage(img1)
        logo_label = tk.Label(self, image=self.photoimg1, background='#262626', activebackground='#262626')
        logo_label.place(x=110, y=20)
        
        # frame where all elements are going to be displayed
        self.mainframe = ctk.CTkFrame(self , border_color="light blue", bg_color="#262626", background_corner_colors=None, border_width=3, height=400, width=450, corner_radius=16 )
        self.mainframe.place(x=70, y=100)
        
        # login label
        log_label = ctk.CTkLabel(self.mainframe, text="Log into your Account as:", font=("Century Gothic", 20))
        log_label.place(x=95, y=12)
        
        # radio buttons to choose ADMIN or EMPLOYEE
        self.user_type = ctk.StringVar()
        self.admin_button = ctk.CTkRadioButton(self.mainframe, text="ADMIN", font=("Century Gothic", 15, "bold"), border_width_checked=7, border_width_unchecked=4, fg_color="green", variable=self.user_type, value="admin", command=self.change_admin_color)
        self.admin_button.place(x=85, y=55)
        
        self.employee_button = ctk.CTkRadioButton(self.mainframe, text="EMPLOYEE", font=("Century Gothic", 15, "bold"), border_width_checked=7, border_width_unchecked=4, fg_color="green", variable=self.user_type, value="employee", command=self.change_employee_color)
        self.employee_button.place(x=250, y=55)

        # username and password fields
        user_label = ctk.CTkLabel(self.mainframe, text="Username:", font=("Arial MS", 20, "bold"))
        user_label.place(x=45, y=120)
        self.username_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Username", width=210, font=("Century Gothic", 20), placeholder_text_color="white")
        self.username_entry.place(x=180, y=120)
        
        pass_label = ctk.CTkLabel(self.mainframe, text="Password:", font=("Arial MS", 20, "bold"))
        pass_label.place(x=45, y=180)
        self.password_entry = ctk.CTkEntry(self.mainframe, placeholder_text="Password", width=210, font=("Century Gothic", 20), placeholder_text_color="white", show="*")
        self.password_entry.place(x=180, y=180)
        
        # login button
        login_btn = ctk.CTkButton(self.mainframe, text="Login", font=("Arial MS", 18, "bold"), width=200, height=40, hover_color="light Green", command=self.login)
        login_btn.place(x=120, y=320)
        
        # Error message label
        self.error_label = ctk.CTkLabel(self.mainframe, text="", font=("Arial MS", 20), text_color="red")
        self.error_label.place(x=35, y=250)
        
        # Connect to the database
        self.conn = db.connect_to_database()
        
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check if username or password is empty
        if not username or not password:
            self.error_label.configure(text="* Username and password cannot be empty")
            return

        # Query the database to check if the provided username and password match
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM authentication WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        cursor.close()

        if result:
            user_type = result[2]
            if user_type == "admin" and self.user_type.get() != "admin":
                self.error_label.configure(text="* Invalid username or password")
            elif user_type == "employee" and self.user_type.get() != "employee":
                self.error_label.configure(text="* Invalid username or password")
            else:
                self.destroy()  # Close the current window
                if user_type == "admin":
                    import Admin_Dashboard
                    new_window = Admin_Dashboard.MedicalStoreApp()
                elif user_type == "employee":
                    import Employee_Dashboard
                    new_window = Employee_Dashboard.MedicalStoreApp()
                new_window.run()
        else:
            self.error_label.configure(text="* Invalid username or password")


    def __del__(self):
        if self.conn.is_connected():
            db.close_connection(self.conn)
        
    def change_admin_color(self):
        self.admin_button.configure(fg_color="red")
        self.employee_button.configure(fg_color="green")
    
    def change_employee_color(self):
        self.employee_button.configure(fg_color="red")
        self.admin_button.configure(fg_color="green")

if __name__ == "__main__":
    app = LoginSignupPage()
    app.mainloop()
