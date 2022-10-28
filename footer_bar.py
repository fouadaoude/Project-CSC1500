import tkinter as tk
import login_page
from database import Database

class Footer(tk.Frame):
    def __init__(self, parent, text="", pady=0, padx=0, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.text = text
        self.parent = parent
        self.footer_frame = tk.Frame(self.parent, height=30)
        
        self.footer_frame.grid_columnconfigure(0, weight=1) 
        self.footer_frame.grid_columnconfigure(2, weight=1)

        self.pady = pady
        self.padx = padx

        self.footer_lbl = tk.Label(self.footer_frame, text=self.text, font="Times 16")
        self.footer_lbl.grid(row=0, column=1, pady=self.pady, padx=self.padx)   

        self.footer_frame.grid(row=3, sticky='ew', columnspan=3)