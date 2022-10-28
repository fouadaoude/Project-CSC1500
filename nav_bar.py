import tkinter as tk
import login_page
from database import Database

class NavBar(tk.Frame):
    def __init__(self, parent, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.user_info = user_info

        self.header_frame = tk.Frame(self.parent)
        self.header_frame.grid_columnconfigure(0, weight=1) 
        self.header_frame.grid_columnconfigure(2, weight=1)
        self.header_frame.grid(row=0, column=0, sticky="EW", columnspan=3)

        self.header_lbl = tk.Label(self.header_frame, text="Forest View", font="Times 20")
        self.header_lbl.grid(row=0, column=0, sticky="W")

        self.header_user_lbl = tk.Label(self.header_frame, text="Logged in as {}".format(self.user_info['employee_name']), font="Times 20")
        self.header_user_lbl.grid(row=0, column=1)

        self.log_out_btn = tk.Button(self.header_frame, text="Log Out", command=lambda: 
                                    [Database().log_out(), self.destroy_children(), login_page.Login(self.parent)])
        self.log_out_btn.grid(row=0, column=2, sticky="E")

    def destroy_children(self):      
        for child in self.parent.winfo_children():            
            child.destroy()