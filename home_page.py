import tkinter as tk
from database import Database
import login_page
import query_page
import import_data_page
import add_data_page
import nav_bar as bar
import footer_bar as fb

class Home(tk.Frame):
    def __init__(self, parent, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.user_info = user_info
        
        # configurations for self.content_frame within Login class        
        self.content_frame = tk.Frame(self.parent)
        self.content_frame.grid_rowconfigure(0, weight=1)        
        self.content_frame.grid_rowconfigure(3, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1) 

        self.nav_bar = bar.NavBar(self.parent, self.user_info)      
        self.footer = fb.Footer(self.parent, text="Please Select an Option.")

        self.import_data_btn = tk.Button(self.content_frame, text="Import data",
                                            command=lambda:[self.destroy_children(),
                                                            import_data_page.ImportData(self.parent, self.user_info)])
        self.import_data_btn.grid(row=0, column=0, sticky='EW', ipady=10)

        self.add_data_btn = tk.Button(self.content_frame, text="Add Data", 
                                            command=lambda:[self.destroy_children(), 
                                                            add_data_page.AddData(self.parent, self.user_info)])
        self.add_data_btn.grid(row=1, column=0, sticky='EW', ipady=10)

        self.query_data_btn = tk.Button(self.content_frame, text="Query", 
                                            command=lambda:[self.destroy_children(), 
                                                            query_page.QueryData(self.parent, self.user_info)])
        self.query_data_btn.grid(row=2, column=0, sticky='EW', ipady=10)

        self.content_frame.config(highlightbackground='white', highlightthickness=.5)
        self.content_frame.grid(row=1, column=0, ipadx=50)

    def destroy_content(self):
        for child in self.content_frame.winfo_children():
            child.destroy()
        self.content_frame.config(bg="#7d8f91")
        self.content_frame.config(highlightthickness=0)

    def destroy_children(self):        
        for child in self.parent.winfo_children():            
            child.destroy()
        
            
        