import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from database import Database
import nav_bar as bar
import home_page
import query_page
import footer_bar as fb
import pickle

class ImportData(tk.Frame):
    def __init__(self, parent, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.user_info = user_info        

        # declaring variables necessary for importing files and file contents with self variables
        self.file_name = None # contains value of file name

        # file_info_frame to contain all file information in side a listview
        # top and bottom frame for extra space and making page easier to view and navigate        
        self.file_info_frame = tk.Frame(self.parent)
        self.top_frame = tk.Frame(self.parent)
        self.btn_frame = tk.Frame(self.file_info_frame)                

        self.file_info_frame.grid_rowconfigure(0, weight=1)   
        self.file_info_frame.grid_rowconfigure(2, weight=1)   
        self.file_info_frame.grid_columnconfigure(0, weight=1)        
        self.file_info_frame.grid_columnconfigure(1, weight=1)

        self.top_frame.grid_columnconfigure(0, weight=0)
        self.top_frame.grid_columnconfigure(1, weight=1)

        #self.btn_frame.grid_rowconfigure(0, weight=1)
        #self.btn_frame.grid_rowconfigure(1, weight=1)
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(2, weight=1)

        # ensure nav bar is visible at top of frame by calling NavBar class made for navigating
        # application, user name, and log out option
        self.nav_bar = bar.NavBar(self.parent, self.user_info)                

        # header label titling content as 'Import File'
        self.header_lbl = tk.Label(self.file_info_frame, text='Import File', font=("Times 30"))
        self.header_lbl.grid(row=0, column=0, sticky='nw')

        # select label telling user to select file and update when file is selected
        self.select_lbl = tk.Label(self.file_info_frame, text='Select a File:', font=("Times 20"))
        self.select_lbl.grid(row=0, column=2, sticky='ne')
        
        # select_file_btn assists user to select file, and command to validate file and its content
        self.select_file_btn = tk.Button(self.file_info_frame, text="Select File",
                                    command=lambda:[self.clear_tree(),self.get_file(), 
                                        [self.read_file(), self.update_tree()] if self.file_name else False])
        self.select_file_btn.grid(row=0, column=3, sticky='ne')            

        self.selected_file_name = tk.Label(self.file_info_frame, font=("Times 20"))                    

        self.s = ttk.Style() # alter treeview
        self.s.layout('unwrap.Treeview', [('unwrap.Treeview.treearea', {'sticky': 'nswe'})])
        self.s.configure('unwrap.Treeview', rowheight=30)

        # file_info_view contains all file information in a Treeview object
        self.file_info_view = ttk.Treeview(self.file_info_frame, 
                    column=(self.get_column_names()),show='headings', height=30)
        self.file_info_view.bind('<ButtonRelease-1>', lambda event: [self.tree_select()])
        self.file_info_view.bind('<Double-1>', lambda event:[query_page.Query(data=self.tree_select(), mode="disabled") if self.file_name else False])                  
        self.file_info_view.grid(row=1,column=0, sticky='ew', columnspan=4)
        self.file_info_frame.bind('<Leave>', lambda event:[self.unfocus_tree()])

        # takes user back to previous page
        self.back_btn = tk.Button(self.btn_frame, text="Back",
                                    command=lambda:[self.destroy_children(), home_page.Home(self.parent, self.user_info)])
        self.back_btn.grid(row=0, column=0, ipady=10, ipadx=15)                
        
        self.save_btn = tk.Button(self.btn_frame, text="Save All")     
        self.save_btn['command'] = lambda: [self.save_tree()]   

        # ensure footer is visible at bottom of frame by calling Footer class made for displaying instructions.
        self.footer = fb.Footer(self.parent, text="Please Select a Valid File.")                

        # place frames accordingly
        self.top_frame.grid(row=0, column=0)
        self.file_info_frame.grid(row=1, column=0)        
        self.btn_frame.grid(row=2, column=1, padx=20, pady=(10,15),sticky='nw')
    
    def unfocus_tree(self):
        for item in self.file_info_view.selection():
            self.file_info_view.selection_remove(item)
        self.save_btn['command'] = lambda: [self.save_tree(mode='all')]
        self.save_btn.config(text='Save All')

    def save_tree(self, mode='all'):
        if mode == 'all':
            tree_dict = self.read_file()
            keys = list(tree_dict.keys())

            for key in keys:
                Database().insert(dict=tree_dict[key])
                print("INSERTING...", tree_dict[key])
        
        elif mode == 'selected':
            tree_dict = self.tree_select()
            keys = list(tree_dict.keys())

            for key in keys:
                Database().insert(dict=tree_dict[key])
                print("INSERTING SELECTION...", tree_dict[key])

    def tree_select(self, event=None):
        tree_dict = self.read_file()
        selected_dict = {}
        selected = self.file_info_view.focus()
        selections = self.file_info_view.selection()        

        if len(selections) > 1:
            print("SELECTIONS", selections) 
            self.save_btn.config(text="Save Highlighted Rows (" + str(len(selections)) + ")")
            
            for selection in selections:
                selected_dict[int(selection)] = tree_dict[int(selection)]

            self.save_btn['command'] = lambda: [self.save_tree(mode='selected')]            
        elif selected:
            self.save_btn.config(text="Save Highlighted Row")
            selected_dict[int(selected)] = tree_dict[int(selected)]  
            self.save_btn['command'] = lambda: [self.save_tree(mode='selected')]
            
        print("SELECTED", selected)
        print("DICT",selected_dict)

        return selected_dict

    def update_tree(self, event=None):
        file_content = self.read_file(self)
        
        x = 0

        for header in file_content.values():
            for key in header.keys():
                self.file_info_view.column("{}". format(key), width=125, anchor='nw')
                self.file_info_view.heading("{}".format(key), text=key)                
            break

        row = []
        x = 0        

        for key, val in file_content.items():
            for data in val.values():
                row.append(data)
            
            # (prevent wrapping)  
            check_char = row[-1].find('\n') 
            
            if check_char > 0:
                row[-1] = str(row[-1][:check_char]) + ' ...'

            self.file_info_view.insert('', 'end', iid=int(key), values=(row))
            x+=1                
            row = []
        
        if len(self.file_info_view.get_children()) > 0:
            self.save_btn.grid(row=0, column=1, ipady=10, ipadx=15)            
            self.selected_file_name.config(text=self.file_name)            
            self.selected_file_name.grid(row=0, column=1, sticky='nw')
        elif len(self.file_info_view.get_children()) < 1 and self.save_btn.winfo_exists():
            self.save_btn.grid_forget()

    def clear_tree(self, event=None):
        for item in self.file_info_view.get_children():
            self.file_info_view.delete(item)

    def get_column_names(self):
        db = Database()
        info = db.select_all()
        columns = []

        for header in info.values():
            for key in header.keys():
                columns.append(key)
            break

        return columns

    # function to have user select and import local file. Returns file name
    def get_file(self):
        try:
            # file_types to validate users selected file type, to ensure proper import
            file_types = [('Binary', '*.dat')]

            # file_name asks user to select a file
            self.file_name = fd.askopenfilename(
                title='Please Select a Valid File to Import',
                initialdir='/',
                filetypes=file_types
            )

            return self.file_name
        except:
            print("Something went wrong retrieving file.")
        
    def read_file(self, file_name=None):        
        if self.file_name:
            content = []
            with (open(self.file_name, 'rb')) as f:
                while True:
                    try:
                        content.append(pickle.load(f))
                    except EOFError:
                        break
            
            return content[0]
            
    # function to get all columns from database and return column names
    def get_column_names(self):
        db = Database()
        info = db.select_all()
        columns = []

        for header in info.values():
            for key in header.keys():
                columns.append(key)
            break

        return columns

    def destroy_children(self):
        # you were loved dearly, child... farewell.
        for child in self.parent.winfo_children():
            child.destroy()

