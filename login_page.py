import tkinter as tk
import home_page
from database import Database
import footer_bar as fb

class Login(tk.Frame):
    def __init__(self, parent, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        Database().create_admin()
        
        self.top_frame = tk.Frame(self.parent, bg='#7d8f91', height=150)
        self.login_frame = tk.Frame(self.parent)
        self.bottom_frame = tk.Frame(self.parent, bg='#7d8f91', height=150)
        self.footer = fb.Footer(self.parent, text="Welcome to Forest View; Please Enter Credentials.")

        self.login_frame.grid_rowconfigure(0, weight=1)
        self.login_frame.grid_columnconfigure(1, weight=1)

        self.top_frame.grid(row=0, sticky='ew')
        self.login_frame.grid(row=1, sticky='nsew')
        self.bottom_frame.grid(row=2, sticky='ew')        

        self.center_left_frame = tk.Frame(self.login_frame, bg='#7d8f91', width=400)
        self.center_mid_frame = tk.Frame(self.login_frame, width=50)
        self.center_mid_frame.config(highlightbackground='white', highlightthickness=1)
        self.center_right_frame = tk.Frame(self.login_frame, bg='#7d8f91', width=400)

        self.center_mid_frame.grid_rowconfigure(0, weight=1)
        self.center_mid_frame.grid_rowconfigure(5, weight=1)

        self.center_mid_frame.grid_columnconfigure(0, weight=1)
        self.center_mid_frame.grid_columnconfigure(3, weight=1)        

         # header label for login frame
        self.header = tk.Label(self.center_mid_frame, text="Forest View", font="Times 35 underline")
        self.header.grid(row=0, column=1, sticky='ew')

        # label for username
        self.uname_label = tk.Label(self.center_mid_frame, text="Username", font=("Times", 20))        
        self.uname_label.grid(row=1, column=1, sticky='W')        

        # entry for username
        self.uname = tk.StringVar(self.center_mid_frame)
        self.uname_entry = tk.Entry(self.center_mid_frame, textvariable=self.uname, width=20)
        self.uname.set('admin')
        self.uname_entry.grid(row=2, column=1, sticky='ew')

        # label for password
        self.password_label = tk.Label(self.center_mid_frame, text="Password", font=("Times", 20))
        self.password_label.grid(row=3, column=1, sticky='W')

        # entry for password
        self.password = tk.StringVar(self.center_mid_frame)
        self.password_entry = tk.Entry(self.center_mid_frame, textvariable=self.password, width=20, show="*")
        self.password.set('123')
        self.password_entry.grid(row=4, column=1, sticky='ew')

        # login button with validate_login command
        self.login_btn = tk.Button(self.center_mid_frame, text="Login", command=lambda: [self.log_user_in()])
        self.login_btn.grid(row=5, column=1, ipadx=30, ipady=10)     
        
        self.center_left_frame.grid(row=0, column=0, sticky='ns')
        self.center_mid_frame.grid(row=0, column=1, sticky='nsew')
        self.center_right_frame.grid(row=0, column=2, sticky='ns')        

        #self.login_frame.config(pady=25, highlightbackground='white', highlightthickness=1) # pady and padx parameters are to change size of login container
    
    def log_user_in(self):     
        db = Database()              
         # destroys all children within container and takes user to Home class
        self.user_info = db.validate_login(employee_name=self.uname.get(), password=self.password.get())
        print(self.user_info)

        # if user and pass are in db
        if self.user_info:
            self.destroy_children()
            home_page.Home(self.parent, self.user_info)

    def destroy_children(self):
        for widgets in self.parent.winfo_children():
            widgets.destroy()