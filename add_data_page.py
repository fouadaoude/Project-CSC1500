import tkinter as tk
import home_page
import nav_bar as bar
import footer_bar as fb
import re
from database import Database
from tkinter import messagebox

class AddData(tk.Frame):
    def __init__(self, parent, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        # parent is root Tk() object
        self.parent = parent

        # new frames to add into add_data_page for header, content and footer
        self.header_frame = tk.Frame(self.parent)
        self.content_frame = tk.Frame(self.parent)
        self.footer = fb.Footer(self.parent, text="Please Enter ALL Fields CORRECTLY in Order to Save Data.")
        
        # user_info passed in from last page
        self.user_info = user_info        
        
        # to validate fields as sufficient. Holds ssn, email, and phone_number
        self.format_bool = {'ssn': False, 'email': False, 'phone_number': False} 

        # nav bar content 
        self.nav_bar = bar.NavBar(self.parent, self.user_info)
        
        # configuring rows for add data frame
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(8, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)              
        
        # header label that states title for page: (Add Data)
        self.header = tk.Label(self.header_frame, text="Add Data", font="Times 35 underline")
        self.header.grid(row=1, column=0) # place header accordingly, under nav bar

        # label, and entry for employee_name 
        self.employee_name_lbl = tk.Label(self.content_frame, text="Employee Name", font="Times 20")
        self.employee_name_lbl.grid(row=0, column=0, sticky="W")
        self.employee_name_entry = tk.Entry(self.content_frame)
        self.employee_name_entry.grid(row=0, column=1, sticky="EW", pady=5)

        # entry and label for new employee password
        self.password = tk.StringVar(self.content_frame)
        self.password_lbl = tk.Label(self.content_frame, text="Password", font=("Times 20"))
        self.password_lbl.grid(row=1, column=0, sticky="W")
        self.password_entry = tk.Entry(self.content_frame, textvariable=self.password, show='*')
        self.password_entry.grid(row=1, column=1, sticky="EW", pady=5)

        # entry and label for new employee position
        self.position_lbl = tk.Label(self.content_frame, text="Position", font=("Times 20"))
        self.position_lbl.grid(row=2, column=0, sticky="W")
        self.position_entry = tk.Entry(self.content_frame)
        self.position_entry.grid(row=2, column=1, sticky="EW", pady=5)

        # entry and label for new employee social security number
        self.ssn_lbl = tk.Label(self.content_frame, text="SSN", font=("Times 20"))
        self.ssn_lbl.grid(row=3, column=0, sticky="W")
        self.ssn_entry = tk.Text(self.content_frame, height=1.45)
        
        # <KeyPress> for automatic format correction
        self.ssn_entry.bind('<KeyPress>', lambda event: [self.format_data(event, format_type='ssn')])        
        
        # once user focuses out of ssn entry, validate entry
        self.ssn_entry.bind('<FocusOut>', lambda event: [self.ssn_validation(self.format_bool['ssn']) if len(self.ssn_entry.get('1.0', "end-1c")) > 0 else False])        
        self.ssn_entry.grid(row=3, column=1, sticky="EW", pady=5)

        # entry and label for new employee address
        self.address_lbl = tk.Label(self.content_frame, text="Home Address", font=("Times 20"))
        self.address_lbl.grid(row=4, column=0, sticky="W")
        self.address_entry = tk.Entry(self.content_frame)
        self.address_entry.grid(row=4, column=1, sticky="EW", pady=5)

        # entry and label for email
        self.email_lbl = tk.Label(self.content_frame, text="Email", font=("Times 20"))
        self.email_lbl.grid(row=5, column=0, sticky="W")
        self.email_entry = tk.Entry(self.content_frame)
        
        # bind '<KeyPress>' to: self.format_data(event, format_type='email') within self.email_entry
        # when this event occurs, the users entered email will be filtered, edited, and validated
        self.email_entry.bind('<KeyPress>', lambda event: [self.format_data(event, format_type='email')])
        
        # bind '<FocusOut>' to: 
        # self.email_validation(self.format_bool['email']) if len(self.email_entry.get()) > 0 else False within self.email_entry
        # when this event occurs, run command to check if user has entered a valid email and length of entry > 0
        self.email_entry.bind('<FocusOut>', lambda event: [self.email_validation(self.format_bool['email']) if len(self.email_entry.get()) > 0 else False])
        self.email_entry.grid(row=5, column=1, sticky="EW", pady=5)

        # self.phone_entry labels, and textbox
        self.phone_lbl = tk.Label(self.content_frame, text="Phone Number", font=("Times 20"))
        self.phone_lbl.grid(row=6, column=0, sticky="W")
        self.phone_entry = tk.Text(self.content_frame, height=1.45)
        
        # bind '<KeyPress>' to run command self.format_data(event, format_type='phone_number')        
        self.phone_entry.bind('<KeyPress>',lambda event: [self.format_data(event, format_type='phone_number')])
        
        # bind '<FocusOut>' to run command:
        # self.phone_validation(self.format_bool['phone_number']) 
        # if len(self.phone_entry.get('1.0', "end-1c")) > 0 else False
        # whenever user focuses out of phone_entry, the user will be notified if something is incorrect
        self.phone_entry.bind('<FocusOut>', lambda event: [self.phone_validation(self.format_bool['phone_number']) if len(self.phone_entry.get('1.0', "end-1c")) > 0 else False])
        self.phone_entry.grid(row=6, column=1, sticky="EW", pady=5)

        # skills entry is fairly untouched and pretty standard for a user to enter as many lines as possible
        # to indicate their skills
        self.skills = tk.Label(self.content_frame, text="Skills", font=("Times 20"))
        self.skills.grid(row=7, column=0, sticky="W")
        self.skills_entry = tk.Text(self.content_frame)        
        self.skills_entry.grid(row=7, column=1, sticky="EW", pady=5)

        # cancel button will destroy all children contained in add_data_page THEN take user back to home_page
        self.cancel_btn = tk.Button(self.content_frame, text="Cancel", 
                        command=lambda:[self.destroy_children(), home_page.Home(self.parent, self.user_info)])
        self.cancel_btn.grid(row=8, column=0, sticky="WE", ipady=15, padx=5)           

        # all user fields of data being passed to Database() class to insert new employee into database
        self.add_data_btn = tk.Button(self.content_frame, text="Add Data", 
                        command=lambda:[Database().insert(employee_id=0, employee_name=self.employee_name_entry.get(), 
                                                password=self.password.get(), position=self.position_entry.get(), 
                                                ssn=self.ssn_entry.get('1.0', "end-1c"), home_address=self.address_entry.get(), 
                                                email=self.email_entry.get(), phone_number=self.phone_entry.get('1.0', "end-1c"), 
                                                skills=self.skills_entry.get('1.0', "end-1c")), 
                                                Database().select_all()])    

        # binds self.parent to user actions containing keypress and keyrelease, as well as focusin and focusout
        # these are meant to continuously check and validate the form and make sure all fields are filled in
        # correctly.
        self.parent.focus_set()
        self.parent.bind('<KeyRelease>', lambda event:[self.form_validation(event)])
        self.parent.bind('<KeyPress>', lambda event:[self.form_validation(event)])        
        self.parent.bind('<FocusOut>', lambda event:[self.form_validation(event)])
        self.parent.bind('<FocusIn>', lambda event:[self.form_validation(event)])                        

        self.header_frame.grid(row=1, column=0)        
        self.content_frame.config(highlightbackground='white', highlightthickness=.5)
        self.content_frame.grid(row=2, column=0, pady=(0, 30))

    # function form_validation sole job is to continuously check whether fields are valid and update
    # button functionality and visibility within form
    def form_validation(self, event=None):
        name = self.employee_name_entry.get()
        password = self.password.get()
        position = self.position_entry.get()
        address = self.address_entry.get()
        # check if skills has length greater than 0 and check if user enters valid char instead of just '\n' char
        skills = (len(self.skills_entry.get('1.0', 'end-1c')) > 0) and (self.skills_entry.get('1.0', 'end-1c') != '\n')
        
        valid = False
        
        # check if all fields are valid, if so make add new employee button visible
        if (name and password and position and address and skills and all(val == True for val in self.format_bool.values())):            
            self.add_data_btn.grid(row=8, column=1, sticky="EW", ipady=15, padx=5)
            valid = True
        # check if add new employee button is enabled and check if one or all entered fields are invalid,
        # if one or all fields are supposedly invalid and add data button is viewable, immediately remove from grid.
        elif self.add_data_btn.winfo_viewable() and valid == False:
            self.add_data_btn.grid_forget()
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
            elif (str(event.keysym) == 'BackSpace'):                
                # if user hits delete btn delete previous char
                self.ssn_entry.delete('1.0', 'end-2c')   
                self.ssn_entry.insert('1.0', text[:len(text)-1])
                break # break to end loop early to not delete entire entry input
        
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
            elif (str(event.keysym) == 'BackSpace'):                
                # if user hits delete btn delete previous char                
                self.phone_entry.delete('1.0', 'end-2c')                                
                self.phone_entry.insert('1.0', text[:len(text)-1])
                break # break to end loop early to prevent deleting entire input instead of one char
        
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

        print(self.format_bool)
            
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
        print(self.format_bool)

    def destroy_children(self):
        self.parent.unbind('<KeyRelease>')
        self.parent.unbind('<KeyPress>')
        self.parent.unbind('<FocusOut>')
        self.parent.unbind('<FocusIn>')

        # you were loved dearly, child... farewell.
        for child in self.parent.winfo_children():
            child.destroy()