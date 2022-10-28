import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
import pickle
import home_page
import nav_bar as bar
import footer_bar as fb
import re
from database import Database

reverse = False # for reversing treeview

class QueryData(tk.Frame):
    def __init__(self, parent=None, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.parent = parent
        self.user_info = user_info
        

        # frame initializations
        self.content_frame = tk.Frame(self.parent)

        # nav bar content 
        self.nav_bar = bar.NavBar(self.parent, self.user_info)
        self.footer = fb.Footer(self.parent, text="Please Enter ALL Fields CORRECTLY in Order to Save Data.")
        
        self.search_frame = tk.Frame(self.content_frame)
        self.search_results_frame = tk.Frame(self.content_frame)        
        self.btn_frame = tk.Frame(self.content_frame)
        self.search_options_frame = tk.Frame(self.search_frame)                

        # frame configurations
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)
        
        self.search_frame.grid_columnconfigure(0, weight=0)
        self.search_frame.grid_columnconfigure(1, weight=1)

        self.search_options_frame.grid_columnconfigure(0, weight=1)
        self.search_options_frame.grid_columnconfigure(1, weight=0)

        # labels, entries, variables for search options, and treeview
        self.search_lbl = tk.Label(self.search_frame, text="Search", font="Times 35")
        self.search_lbl.grid(row=0, column=0, sticky='W')

        self.search_results = []
        
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, font="Times 25", textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky='W')
        self.search_entry.bind('<KeyRelease>', lambda event:[self.search(event)])

        self.search_by_var = tk.StringVar()        
        self.search_options = ['employee_id','employee_name', 'position', 'ssn', 'home_address', 'email', 'phone_number', 'skills']

        self.search_by_lbl = tk.Label(self.search_options_frame, text="Search By: ")
        self.search_by_lbl.grid(row=0, column=0, sticky='E')
        self.search_options_menu = tk.OptionMenu(self.search_options_frame, self.search_by_var, *self.search_options)
        self.search_options_menu.grid(row=0, column=1, sticky='E')

        self.s = ttk.Style() # alter treeview
        self.s.layout('unwrap.Treeview', [('unwrap.Treeview.treearea', {'sticky': 'nswe'})])
        self.s.configure('unwrap.Treeview', rowheight=30)

        self.result_tree = ttk.Treeview(self.search_results_frame, 
                columns=(self.get_column_names()), show="headings", height=20, style='unwrap.Treeview', selectmode='browse')       
        self.result_tree.pack(side='left', expand=True) 
        self.result_tree.bind('<ButtonRelease-1>', lambda event:[self.tree_select(event)])
        self.result_tree.bind('<Double-1>', lambda event:[Query(data=self.tree_select()) if self.tree_select() else False])          
        self.result_tree.bind('<Activate>', lambda event:[self.update_tree(event, reversed=reverse)])        

        self.content_frame.bind('<Leave>', lambda event:[self.unfocus_tree()])

        self.ybar = ttk.Scrollbar(self.search_results_frame, orient="vertical", command=self.result_tree.yview)
        self.ybar.pack(side='right', fill='y')
        self.result_tree.configure(yscrollcommand=self.ybar.set)

        self.delete_btn = tk.Button(self.btn_frame, text="Delete", command=lambda:[self.delete_option()])        
        self.export_btn = tk.Button(self.btn_frame, text="Export All", command=lambda:[self.export_file()])  
        self.export_btn.grid(row=0, column=1, ipady=10, ipadx=15)      
        self.update_tree() # inserts all data from database into treeview
        
        self.back_btn = tk.Button(self.btn_frame, text="Back", 
                                command=lambda:[self.destroy_content(), home_page.Home(self.parent, self.user_info)])        
        self.back_btn.grid(row=0, column=0, ipady=10, ipadx=15)

        self.reverse_btn = tk.Button(self.btn_frame, text="Reverse",
                                command=lambda:[self.update_tree(reversed=self.reverse_tree())])
        self.reverse_btn.grid(row=0, column=2, ipady=10, ipadx=15)      

        self.search_options_frame.grid(row=0, column=1, sticky='NSEW')
        self.search_frame.grid(row=0, column=0, sticky='NSEW')
        self.content_frame.grid(row=1, column=0)        
        self.search_results_frame.grid(row=1, column=0)
        self.btn_frame.grid(row=2, column=0, padx=20, pady=(10, 15))

    def unfocus_tree(self):
        for item in self.result_tree.selection():
            self.result_tree.selection_remove(item)
        self.export_btn['command'] = lambda: [self.export_file()]
        self.export_btn.config(text='Export All')
        self.delete_btn.grid_forget()

    def save_location(self):
        files = [('Binary', '*.dat')]

        location = fd.asksaveasfile(filetypes=files, defaultextension=files)

        return location.name
        
    def export_file(self, dict=None):
        if dict:            
            try:
                file_name = self.save_location()
                file = open(file_name, 'wb')
                pickle.dump(dict, file)
                file.close()
                self.export_btn.grid_forget()
                print("Exported file successfully")
            except:
                print("Could Not Save File. Try Again.")
        else:
            try:
                dict = self.get_data_for_tree()
                file_name = self.save_location()
                file = open(file_name, 'wb')
                pickle.dump(dict, file)
                file.close()
                self.export_btn.grid_forget()
                print("Exported file successfully")
            except:
                print("Could Not Save File. Try Again.")

    def export_config(self, export_type='select'):
        searched_dict = {}
        selected_dict = {}
        columns = self.get_column_names()              

        if export_type == 'select':            
            # check if user has selected a row            
            selected = int(self.result_tree.focus())
            selected_value = self.result_tree.item(selected)['values'] 
            selected_db_value = self.get_data_for_tree()    
            
            valid = False     

            if selected_value:                
                selected_dict[selected] = selected_db_value[selected]                                   

                self.export_btn.config(text='Export Selected')                 
                self.export_btn['command'] = lambda: [self.export_file(selected_dict)]
                self.export_btn.grid(row=0, column=1, ipady=10, ipadx=15)
                self.delete_btn.grid(row=0, column=3, ipady=10, ipadx=15)
                valid = True            
            elif self.export_btn.winfo_exists() and valid == False:
                self.export_btn.grid_forget()                     

        elif export_type == 'search':
            valid = False 
            # check if user has searched row(s)
            if self.search_results:
                tree_dict = self.get_data_for_tree()
                data = [] 
                
                x = 0
                for row in self.search_results:                    
                    data.append(tree_dict[int(row)])
                    searched_dict[int(row)] = data[x]
                    x+=1                
                
                self.export_btn.config(text='Export {} Highlighted'.format(
                                'All '+str(len(self.search_results)) if len(self.search_results) > 1 else '1'))
                self.export_btn['command'] = lambda: [self.export_file(searched_dict)]
                self.delete_btn.grid(row=0, column=2, ipady=10, ipadx=15)
                self.export_btn.grid(row=0, column=1, ipady=10, ipadx=15)      
                valid = True            
            elif self.export_btn.winfo_exists() and valid == False:
                print("REMOVING EXPORT BTN, LINE 179")
                self.export_btn.grid_forget()

    def search(self, event):
        data = self.get_data_for_tree()
        search_value = self.search_var.get()
        search_by = self.search_by_var.get() 

        valid = False

        self.search_results = []        

        if search_by: # checks if user has search by filter enabled
            for child in self.result_tree.get_children(): # loop through treeview children
                for e_id, dict in data.items(): # check seperate treeview data dict to make it easier to search without treeview
                    if search_by == 'employee_id' and len(str(search_value)) > 0: # check if user has filter employee_id enabled
                        if str(search_value) in str(data[e_id][search_by]): # check if search_value is in seperate tree view data dict                    
                            self.search_results.append(e_id)
                    elif str(search_value).lower() in str(dict[search_by]).lower() and len(str(search_value)) > 1:
                        # if filter is not employee_id then check if search_value is in seperate tree view data dict
                        self.search_results.append(e_id)                       
                    elif len(str(search_value)) < 1:
                        # clear list if there is no search_value
                        self.search_results = []        
                break # break out on every child loop to avoid excessive loops

        else: # if there is no filter enabled and want to search ALL elements of the tree view
            for child in self.result_tree.get_children():                                
                if str(search_value).lower() in str(data[int(child)].values()).lower() and len(str(search_value)) > 1:
                    self.search_results.append(child)        
                elif len(str(search_value)) < 1:
                    self.search_results = []
        
        self.result_tree.selection_set(self.search_results)
        
        self.export_config(export_type='search')
        
    def delete_option(self):        
        user_info = self.tree_select(None)        
        row_id = int(self.result_tree.focus())
        
        db = Database()
        db.delete_entry(employee_id=user_info[row_id]['employee_id'])
        self.update_tree()

    def tree_select(self, event=None):

        tree_dict = self.get_data_for_tree()
        selected_dict = {}
        selected = self.result_tree.focus()

        if selected:
            self.search_entry.delete(0, 'end')
            selected_dict[int(selected)] = tree_dict[int(selected)]    
    
            self.export_config(export_type='select')

        return selected_dict        

    def get_data_for_tree(self, event=None):
        global reverse
        
        db = Database()

        if reverse:
            info = db.select_all(reverse=True)
        else:
            info = db.select_all()
        columns = self.get_column_names()

        tree_dict = {}

        x = 0
        for dict in info.values():
            tree_dict[x] = dict
            x+=1
        
        return tree_dict

    def get_tree_data(self, event=None):
        data = []
        data_dict = {}
        columns = self.get_column_names()        

        for parent in self.result_tree.get_children():
            data.append(self.result_tree.item(parent)['values'])
        
        for x in range(len(data)):
            for i in range(len(columns)):                  
                data_dict.setdefault(x, {})[columns[i]] = data[x][i] 

        return data_dict

    def get_column_names(self):
        db = Database()
        info = db.select_all()
        columns = []

        for header in info.values():
            for key in header.keys():
                columns.append(key)
            break

        return columns

    def clear_tree(self):
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def reverse_tree(self):
        global reverse

        if reverse:
            reverse = False
        else:
            reverse = True

        return reverse

    def update_tree(self, event=None, reversed=False):
        db = Database()
        
        if reversed:
            info = db.select_all(reverse=True)
        else:
            info = db.select_all()

        columns = self.get_column_names()        
        selected = self.result_tree.focus()
        
        x = 0
        # to update Treeview rows, if there are rows already, clear it and update by re-inserting.
        if len(self.result_tree.get_children()) > 0:
            self.clear_tree()
        
        if event and self.delete_btn.winfo_exists():
            self.delete_btn.grid_forget()        
        
        for header in info.values():
            for key in header.keys():                         
                self.result_tree.column("{}".format(columns[x]), width=125, anchor='nw')                    
                self.result_tree.heading("{}".format(columns[x]), text=key)                    
                x += 1                
            break        

        row = []
        x = 0                

        for key, val in info.items():
            i = 0
            for data in val.values():
                print("DATA",data)                
                if i == 2 or i == 4: # to hide password and ssn                    
                    data = "*" * len(data)   
                row.append(data)
                i += 1
            # (prevent wrapping)  
            check_char = row[-1].find('\n') 
            
            if check_char > 0:
                row[-1] = str(row[-1][:check_char]) + ' ...'

            self.result_tree.insert('', 'end', iid=x, values=(row))
            x+=1                
            row = []                  
        
    def destroy_content(self):
        for child in self.parent.winfo_children():
            child.destroy()
        
class Query(tk.Toplevel):
    def __init__(self, parent=None, data=None, mode="normal"):
        super().__init__(parent=parent)
        
        self.data = data
        self.key = list(self.data.keys())
        self.key = self.key[0]# if mode == "normal" else self.key
        self.val = list(self.data.values())
        self.mode = mode
        # to validate fields as sufficient. Holds ssn, email, and phone_number
        self.format_bool = {'ssn': False, 'email': False, 'phone_number': False}   

        self.title("View Query")
        self.geometry("705x650")
        self.config(bg='#7d8f91')
        self.resizable(False, False)
        # only allow one toplevel window at a time
        self.grab_set()

        self.frame = tk.Frame(self)
        
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_columnconfigure(1, weight=1)

        self.content_frame = tk.Frame(self.frame)        

        self.bind('<KeyRelease>', lambda event:[self.update_data(event)])        

        self.e_id = tk.Label(self.content_frame, text="employee_id", font=("Times 20"))
        self.e_id.grid(row=1, column=1, sticky='w')

        self.e_id_lbl = tk.Label(self.content_frame, text=str(self.data[self.key]['employee_id']))
        self.e_id_lbl.grid(row=1, column=2, sticky='w')

        self.e_name = tk.Label(self.content_frame, text="employee_name", font=("Times 20"))
        self.e_name.grid(row=2, column=1, sticky='w')
        
        self.e_name_entry = tk.Entry(self.content_frame, state='normal')
        self.e_name_entry.insert(0, str(self.data[self.key]['employee_name']))
        self.e_name_entry.grid(row=2, column=2, sticky='ew')
        self.e_name_entry.configure(state=self.mode)

        self.password = tk.Label(self.content_frame, text="password", font=("Times 20"))
        self.password.grid(row=3, column=1, sticky='w')

        self.password_entry = tk.Entry(self.content_frame, state='normal')
        self.password_entry.insert(0, str(self.data[self.key]['password']))
        self.password_entry.grid(row=3, column=2, sticky='ew')
        self.password_entry.config(state=self.mode)
        
        self.pos = tk.Label(self.content_frame, text="position", font=("Times 20"))
        self.pos.grid(row=4, column=1, sticky='w')

        self.pos_entry = tk.Entry(self.content_frame, state='normal')
        self.pos_entry.insert(0, str(self.data[self.key]['position']))
        self.pos_entry.grid(row=4, column=2, sticky='ew')
        self.pos_entry.config(state=self.mode)

        self.ssn = tk.Label(self.content_frame, text="ssn", font=("Times 20"))
        self.ssn.grid(row=5, column=1, sticky='w')

        self.ssn_entry = tk.Text(self.content_frame, height=1.45, state='normal')
        self.ssn_entry.insert('1.0', str(self.data[self.key]['ssn']))
        # <KeyPress> for automatic format correction
        self.ssn_entry.bind('<KeyPress>', lambda event: [self.format_data(event, format_type='ssn')])     
        # once user focuses out of ssn entry, validate entry
        self.ssn_entry.bind('<FocusOut>', lambda event: 
                [self.ssn_validation(self.format_bool['ssn']) if len(self.ssn_entry.get('1.0', "end-1c")) > 0 else False])           
        self.ssn_entry.grid(row=5, column=2, sticky='ew')
        self.ssn_entry.config(state=self.mode)

        self.address = tk.Label(self.content_frame, text="home_address", font=("Times 20"))
        self.address.grid(row=6, column=1, sticky='w')

        self.address_entry = tk.Entry(self.content_frame, state='normal')
        self.address_entry.insert(0, str(self.data[self.key]['home_address']))
        self.address_entry.grid(row=6, column=2, sticky='ew')
        self.address_entry.config(state=self.mode)

        self.email = tk.Label(self.content_frame, text="email", font=("Times 20"))
        self.email.grid(row=7, column=1, sticky='w')

        self.email_entry = tk.Entry(self.content_frame, state='normal')
        self.email_entry.insert(0, str(self.data[self.key]['email']))        

        # bind '<KeyPress>' to: self.format_data(event, format_type='email') within self.email_entry
        # when this event occurs, the users entered email will be filtered, edited, and validated
        self.email_entry.bind('<KeyPress>', lambda event: [self.format_data(event, format_type='email')])
        
        # bind '<FocusOut>' to: 
        # self.email_validation(self.format_bool['email']) if len(self.email_entry.get()) > 0 else False within self.email_entry
        # when this event occurs, run command to check if user has entered a valid email and length of entry > 0
        self.email_entry.bind('<FocusOut>', lambda event: 
                [self.email_validation(self.format_bool['email']) if len(self.email_entry.get()) > 0 else False])
        self.email_entry.grid(row=7, column=2, sticky='ew')
        self.email_entry.config(state=self.mode)

        self.phone = tk.Label(self.content_frame, text="phone_number", font=("Times 20"))
        self.phone.grid(row=8, column=1, sticky='w')

        self.phone_entry = tk.Text(self.content_frame, height=1.45, state='normal')
        self.phone_entry.insert('1.0', str(self.data[self.key]['phone_number']))
        # bind '<KeyPress>' to run command self.format_data(event, format_type='phone_number')        
        self.phone_entry.bind('<KeyPress>',lambda event: [self.format_data(event, format_type='phone_number')])

        # bind '<FocusOut>' to run command:
        # self.phone_validation(self.format_bool['phone_number']) 
        # if len(self.phone_entry.get('1.0', "end-1c")) > 0 else False
        # whenever user focuses out of phone_entry, the user will be notified if something is incorrect
        self.phone_entry.bind('<FocusOut>', lambda event: 
                [self.phone_validation(self.format_bool['phone_number']) if len(self.phone_entry.get('1.0', "end-1c")) > 0 else False])
        self.phone_entry.grid(row=8, column=2, sticky='ew')
        self.phone_entry.config(state=self.mode)


        self.skills = tk.Label(self.content_frame, text="skills", font=("Times 20"))
        self.skills.grid(row=9, column=1, sticky='w')

        self.skills_entry = tk.Text(self.content_frame, state='normal')
        self.skills_entry.insert("1.0", str(self.data[self.key]['skills']))
        self.skills_entry.grid(row=9, column=2, sticky='ew')   
        self.skills_entry.config(state=self.mode)

        self.update_btn = tk.Button(self.frame, text="Update")

        # validate initial format bools
        self.ssn_format()   
        self.email_format()
        self.phone_format()      

        self.frame.grid(row=0, column=0, sticky='ew')
        self.content_frame.grid(row=1, column=1, sticky='ew')        

    def get_current_entry_data(self):
        row_dict = {}
        entry_dict = {}

        entry_dict['employee_id'] = self.data[self.key]['employee_id']
        entry_dict['employee_name'] = self.e_name_entry.get()
        entry_dict['password'] = self.password_entry.get()
        entry_dict['position'] = self.pos_entry.get()
        entry_dict['ssn'] = self.ssn_entry.get('1.0', 'end-1c')
        entry_dict['home_address'] = self.address_entry.get()
        entry_dict['email'] = self.email_entry.get()
        entry_dict['phone_number'] = self.phone_entry.get('1.0', 'end-1c')
        entry_dict['skills'] = self.skills_entry.get('1.0', 'end-1c')

        row_dict[self.key] = entry_dict

        return row_dict

    def update_data(self, event=None):
        fields = ['employee_id', 'employee_name', 'password', 
                  'position', 'ssn', 'home_address', 'email',
                  'phone_number', 'skills']

        valid = False

        db = Database()
        saved_data = db.select(employee_id=self.data[self.key]['employee_id'])
        cur_data = self.get_current_entry_data()                

        if str(cur_data[self.key]) != str(saved_data) and all(val == True for val in self.format_bool.values()):            
            valid = True
            self.update_btn.grid(row=3, column=1)
            self.update_btn.config(command=lambda: [db.update(cur_data[self.key])])
        elif not all(val == True for val in self.format_bool.values()):
            self.update_btn.grid_forget()
        elif self.update_btn.winfo_viewable() and valid == False:
            self.update_btn.grid_forget()

        
        #btn['command'] = lambda: []    
    
    def ssn_format(self, event=None):
        # set format_bool['ssn'] to False to make sure ssn is fresh, continuously updated, and formatted properly
        self.format_bool['ssn'] = False

        # called for formatting reasons. ssn_entry will delete entered entry and re-insert 
        # var text based on user actions
        text = self.ssn_entry.get('1.0', 'end-1c')

        # loop through all chars in ssn_entry to filter, format, and validate ssn
        for char in self.ssn_entry.get('1.0', 'end-1c'):
            # check for new line chars and max char input to be 11 chars
            if self.ssn_entry.get('end-1c', 'end') == '\n':
                self.ssn_entry.delete('end-1c', 'end')
             
            # check third char for '-' char, if does not exist, insert '-'
            if (len(self.ssn_entry.get('1.0', 'end-1c')) == 2) and (char != '-'):                    
                self.ssn_entry.insert('end', '-')
            # check third char for '-' char, if does not exist, insert '-'
            if (len(self.ssn_entry.get('1.0', 'end-1c')) == 6) and (char != '-'):                    
                self.ssn_entry.insert('end', '-')          
            
        
        if (len(self.ssn_entry.get('1.0', 'end-1c')) == 11) and (self.ssn_entry.get('1.0', 'end-1c').count('-') == 2):
            self.format_bool['ssn'] = True # verify that the correct number of chars are included and has 2 '-' chars
        
        return self.format_bool['ssn']

    def phone_format(self, event=None):
        # standard phone characters required for formatting    
        phone_chars = ['(', ')', ' ', '-']

        # set format_bool['phone_number'] to False indicating new round of checking for:
        # validity, and filtered to required format
        self.format_bool['phone_number'] = False
        text = self.phone_entry.get('1.0', 'end-1c')                
        
        # loop through entire phone_entry to format, and automatically update validity of entry
        for char in self.phone_entry.get('1.0', "end-1c"):
            # check if user types \n in phone_entry, if so delete it            
            if self.phone_entry.get('end-1c', 'end') == '\n':
                self.phone_entry.delete('end-1c', 'end')
            
            # all fields up to elif statement are for formatting purposes.
            # if statements track user input and insert phone characters where needed.
            if (len(self.phone_entry.get('1.0', "end-1c")) == 1) and (char != '('):
                self.phone_entry.insert('1.0', '(')
            if (len(self.phone_entry.get('1.0', "end-1c")) == 4) and (char != ')'):
                self.phone_entry.insert('end',')')
            if (len(self.phone_entry.get('1.0', "end-1c")) == 5) and (char != ' '):
                self.phone_entry.insert('end',' ')
            if (len(self.phone_entry.get('1.0', "end-1c")) == 9) and (char != '-'):
                self.phone_entry.insert('end', '-')
            # check if user hits backspace btn and if so ONLY delete ONE char
            '''elif (str(event.keysym) == 'BackSpace'):                
                # if user hits delete btn delete previous char                
                self.phone_entry.delete('1.0', 'end-2c')                                
                self.phone_entry.insert('1.0', text[:len(text)-1])
                break # break to end loop early to prevent deleting entire input instead of one char'''
        
        # make sure entered phone number is == 14 chars indicating perfect length and format
        if len(self.phone_entry.get('1.0', "end-1c")) == 14:
            # call all() function to make sure ALL elements within list phone_chars are valid, and exist within phone_entry
            self.format_bool['phone_number'] = all([char in self.phone_entry.get('1.0', 'end-1c') for char in phone_chars])

        # not necessary but available if needed.            
        return self.format_bool['phone_number'] # True or False

    def email_format(self, event=None):
        # regex indicates valid email chars
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # set format_bool['email'] to False in-order to automatically check current entry,
        # and filter results
        self.format_bool['email'] = False            

        # check if email_entry contains fields within correct email format variable regex set to [True || False]
        if (re.fullmatch(regex, self.email_entry.get())):
            self.format_bool['email'] = True            
        else:
            self.format_bool['email'] = False     
        
        # not used but available if needed
        return self.format_bool['email'] # True || False

    def format_data(self, event=None, format_type=None):        

        if format_type == 'ssn':  
            # bind '<KeyRelease>' to ssn_entry and call snn_char_limit(event) on KeyRelease to automatically
            # update, filter and format ssn_entry
            self.ssn_entry.bind('<KeyRelease>', lambda event: [self.ssn_char_limit(event)])
            # call ssn_format(event) to store ssn variable that contains ssn format boolean
            ssn = self.ssn_format(event)     
            if str(event.type) == '10': # 10 is for <FocusOut> binding                                      
                # if user focuses out of entry, validate entry and indicate to user validity
                self.ssn_entry.bind('<FocusIn>', self.ssn_validation(ssn)) 
            self.format_bool['ssn'] = ssn # passing True or False depending on format validation

        elif format_type == 'phone_number':
            # bind '<KeyRelease>' to phone_entry to check when user releases key and call phone_char_limit,
            # which checks format and filters according to format requirements
            self.phone_entry.bind('<KeyRelease>', lambda event: [self.phone_char_limit(event)])
            # call phone_format() to format phone_entry and store returned variable of whether the 
            # entered format is True or False
            phone = self.phone_format(event)
            if str(event.type) == '10': # 10 is for <FocusOut> binding            
                # if user focuses out of phone_entry user is then capable of focusin in on phone_entry
                # in order to call phone_validation() to validate and update user on current entry
                self.phone_entry.bind('<FocusIn>', self.phone_validation(phone)) 
                # format_bool['phone_number'] contains boolean of phone_number validity
            self.format_bool['phone_number'] = phone

        elif format_type == 'email':
            # bind <KeyRelease> to self.email_format(event) to automatically format email according to requirements.
            self.email_entry.bind('<KeyRelease>', lambda event: [self.email_format(event)])
            # call self.email_format(event) to store email variable indicating validity of users email
            email = self.email_format(event)
            if str(event.type) == '10': # '10' is for '<FocusOut>' binding
                # if user decides to '<FocusOut>' of email entry, '<FocusIn>' gets called.
                # binding '<FocusIn>' to self.email_validation(email) within widget 'self.email_entry'.
                # self.email_validation(email) contains parameter 'email' that holds value of email validity
                self.email_entry.bind('<FocusIn>', self.email_validation(email))                
            # self.format_bool['email'] contains True or False whether the email is formatted CORRECTLY or NOT
            self.format_bool['email'] = email
    
    def phone_char_limit(self, event=None):
        # phone_chars contains list of characters that are the required format for every employee at fairview
        phone_chars = ['(', ')', ' ', '-']

        # reset self.format_bool['phone_chars'] to False to be filtered through conditionals to
        # filter and validate phone number length, and put phone number in required format
        self.format_bool['phone_number'] = False
        # check if user types more than standard phone number length, if so delete end chars
        if len(self.phone_entry.get('1.0', "end-1c")) >= 15:
            self.phone_entry.delete('end-2c')
        # check if entered char is a digit also check if the char isnt part of standard phone chars, if so delete last char
        elif (not self.phone_entry.get("end-2c").isdigit()) and (self.phone_entry.get('end-2c') not in phone_chars):
            self.phone_entry.delete('end-2c')

        # double check if phone entry meets standard.
        if len(self.phone_entry.get('1.0', "end-1c")) == 14:
            phone = all([char in self.phone_entry.get('1.0', 'end-1c') for char in phone_chars])
            self.format_bool['phone_number'] = True
    
    def ssn_char_limit(self, event=None):
        # reset self.format_bool['ssn'] to False so that every iteration of this function\n
        # self.format_bool['ssn'] is filtered out to (True or False) considering conditionals
        self.format_bool['ssn'] = False
        # check if user types more than standard ssn length, if so delete end chars
        if len(self.ssn_entry.get('1.0', "end-1c")) >= 12:
            self.ssn_entry.delete('end-2c')
        # check if the current entered char is a digit also check if the char isnt part of\n
        # standard phone chars, if so, delete last char
        elif (not self.ssn_entry.get("end-2c").isdigit()) and (self.ssn_entry.get('end-2c') not in ['-']):
            self.ssn_entry.delete('end-2c')

        # double check if phone entry meets standard.
        if (len(self.ssn_entry.get('1.0', 'end-1c')) == 11) and (self.ssn_entry.get('1.0', 'end-1c').count('-') == 2):
            ssn = True # verify that the correct number of chars are included and has 2 '-' chars
            self.format_bool['ssn'] = True

    # function form_validation sole job is to continuously check whether fields are valid and update
    # button functionality and visibility within form
    def form_validation(self, event=None):
        name = self.e_name_entry.get()
        password = self.password_entry.get()
        position = self.pos_entry.get()
        address = self.address_entry.get()
        # check if skills has length greater than 0 and check if user enters valid char instead of just '\n' char
        skills = (len(self.skills_entry.get('1.0', 'end-1c')) > 0) and (self.skills_entry.get('1.0', 'end-1c') != '\n')
        
        valid = False
        
        # check if all fields are valid, if so make add new employee button visible
        if (name and password and position and address and skills and all(val == True for val in self.format_bool.values())):            
            self.update_btn.grid(row=8, column=1, sticky="EW", ipady=15, padx=5)
            valid = True
        # check if add new employee button is enabled and check if one or all entered fields are invalid,
        # if one or all fields are supposedly invalid and add data button is viewable, immediately remove from grid.
        elif self.update_btn.winfo_viewable() and valid == False:
            self.update_btn.grid_forget()
            valid = False
    
        return valid
    
    # all _validation functions EXCEPT 'form_validation(self, event=None)', role is to validate and 
    # indicate to user whether entry is valid, formatted, and filtered properly
    def email_validation(self, email=False):
        if email == False:
            messagebox.showerror('Invalid Email', 'The email you entered is invalid.\n\n Please Try Again.')
        else:
            return True

    def phone_validation(self, phone=False):         
        if phone == False:
            messagebox.showerror('Invalid Phone Format', 'The Phone Number You Entered is in an Invalid Format.\n\nCorrect Format:\n(123) 1234-5678\n\nPlease Try Again.')
        else:
            return True

    def ssn_validation(self, ssn=False):
        if ssn == False:
            messagebox.showerror('Invalid SSN Format', 'The SSN You Entered is in an Invalid Format\n\nCORRECT FORMAT:\nAA-AAA-AAAA\n\nPlease Try Again.')
        else:
            return True