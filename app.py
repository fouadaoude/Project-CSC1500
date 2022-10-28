import tkinter as tk
import login_page

class App(tk.Frame):
    def __init__(self, parent, user_info=None, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args,  **kwargs)
        
        self.parent = parent

        self.login = login_page.Login(parent)  

        self.parent.grid_rowconfigure(1, weight=1) 
        self.parent.grid_columnconfigure(0, weight=1)

        self.parent.config(bg='#7d8f91') # sets background color 
        self.parent.title('Forest View') # sets title
        self.parent.geometry('1200x1400') # sets sizing of window


if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()
