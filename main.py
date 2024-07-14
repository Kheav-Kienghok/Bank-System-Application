from tkinter import *
from function import DatabaseFunction
from tkinter import messagebox
import os

class Window:
    def __init__(self):
        self.root = Tk()
        self.create_init()
        self.db = DatabaseFunction()

    def create_init(self, width = 520, height = 365):
        self.root.iconbitmap(os.path.join(os.getcwd(), 'images', 'bank_icon.ico'))
        self.root.title("Bank System")
        self.root.resizable(0, 0)
    
        self.root.configure(bg = "#ADD8E6")

        self.x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        self.y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{self.x}+{self.y}')
        
        Label(self.root, text="MyBank Banking", font=("Poppins", 20, "bold", "underline"), bg = "#ADD8E6").pack(side = TOP, pady = 10)
        
    def exit_button(self):
        self.root.quit()
        
    def show_page(self, page_class):
        self.root.withdraw()
        page_class()
    
    def show_main(self):
        self.root.deiconify()


class MainPage(Window):
    def __init__(self):
        super().__init__()
        

    def create_init(self):
        super().create_init()

        Button(self.root, text = "Exit", font = ("Poppins", 13), bg = "#000000", fg = "#FFFFFF", width = 8, height = 2, command = self.exit_button).place(x = 397, y = 310)

        label_frame = LabelFrame(self.root, text = "Login Account", font = ("Poppins", 12, "bold"), bg = "#ADD8E6", padx = 10, pady = 10)
        label_frame.pack(padx = 15, pady = 20)
        
        label_frame.grid_columnconfigure((0, 1, 2, 3), weight = 1)
        label_frame.grid_rowconfigure((0, 1, 2, 3), weight = 1)

        create_account_button = Button(label_frame, text = "Create Account", font = ("Poppins", 11), bg = "#ADD8E6", width = 20, height = 10, command = lambda: self.show_page(RegisterPage))
        create_account_button.grid(row = 0, column = 0, rowspan = 3, sticky = "news")
        
        Label(label_frame, text = "Username:", font = ("Poppins", 11, "bold"), bg = "#ADD8E6").grid(row = 0, column = 2, sticky = "wn", padx = 10, pady = 5)
        self.username_entry = Entry(label_frame, font = ("Poppins", 11), width = 25)
        self.username_entry.grid(row = 0, rowspan = 1,column = 2, padx = 10, pady = 30)

        Label(label_frame, text = "Password:", font = ("Poppins", 11, "bold"), bg = "#ADD8E6").grid(row = 0,rowspan = 1,column = 2, sticky = "ws", padx = 10)
        self.password_entry = Entry(label_frame, font = ("Poppins", 11), show = "*", width = 25)
        self.password_entry.grid(row = 1, column = 2, padx = 10)
        
        login_button = Button(label_frame, text = "Login", font = ("Poppins", 11), bg = "#000000", fg = "#FFFFFF", width = 10, height = 2, command = self.login_account_button)
        login_button.grid(row = 2, column = 1, columnspan = 2, rowspan = 3, sticky = "se", padx = 8, pady = 5)

    def login_account_button(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showwarning("Warning!", "No empty fields allowed")
            return
        
        valid_account = self.db.valid_bank_account(username, password)
        
        if isinstance(valid_account, list):
            self.login_page(BankPage, valid_account)
        else:
            messagebox.showerror("Error", "No Data were found")
            
    def login_page(self, page_class, account_information):
        self.root.withdraw()
        page_class(account_information)
        

class RegisterPage(Window):
    def __init__(self):
        super().__init__()
        
    def show_main_page(self):
        self.root.withdraw()
        MainPage()
        
    def create_init(self):
        super().create_init(width = 500, height = 600)
        
        self.register_exit_btn = Button(self.root, text = "Exit", font = ("Poppins", 13), bg = "#000000", fg = "#FFFFFF", width = 8, height = 2, command = self.exit_button)
        self.register_exit_btn.place(x = 370, y = 545)
        
        self.register_back_btn = Button(self.root, text = "Back", font = ("Poppins", 13), bg = "#000000", fg = "#FFFFFF", width = 8, height = 2, command = lambda: self.show_page(MainPage))
        self.register_back_btn.place(x = 45, y = 545)

        label_frame = LabelFrame(self.root, text = "Register Account", font = ("Poppins", 12, "bold"), bg = "#ADD8E6", padx = 10, pady = 10)
        label_frame.pack(padx = 15, pady = 15)
        
        label_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight = 1)
        label_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight = 1)

        register_labels = ["Username:", "Password:", "Confirm Password:", "Create PINS:", "Confirm PINS:", "Birthdate:", "Gender:", "National ID:"]
        
        global register_entry_names
        register_entry_names = ["username_entry", "password_entry", "confirm_password_entry", "create_pins_entry", "confirm_pins_entry", "birthdate_entry", "gender_entry", "national_id_entry"]

        # Dictionary to store entry widgets
        self.entries = {}

        for i, (label_text, entry_name) in enumerate(zip(register_labels, register_entry_names)):
            Label(label_frame, text = label_text, font = ("Poppins", 11, "bold"), bg = "#ADD8E6").grid(row = i, column = 0, sticky = "w", pady = 10)
            entry = Entry(label_frame, font = ("Poppins", 11), width = 25)
            entry.grid(row = i, column = 2, columnspan = 4, padx = 20)
            self.entries[entry_name] = entry
        
        Button(label_frame, text = "Create Account", font = ("Poppins", 11, "bold"), bg = "#000000", fg = "#FFFFFF", width = 20, height = 2, command = self.create_account_button).grid(row = 8, column = 0, columnspan = 5, padx = 25, pady = 5, sticky = "e")

        self.sucessful_register = Label(label_frame, text = "", font = ("Poppins", 11, "bold"), bg = "#ADD8E6")
        
        
    def create_account_button(self):
        information = [self.entries[entry_name].get().strip() for entry_name in self.entries]
        result = self.db.create_customer_account(information)
        
        if result[0] == 200:
            self.root.geometry(f"500x610+{self.x}+{self.y}")
 
            self.register_exit_btn.place(x = 370, y = 555)
            self.register_back_btn.place(x = 45, y = 555)
            
            self.sucessful_register.config(text = f"{result[1]}")
            self.sucessful_register.grid(row = 9, column = 0, columnspan = 7, padx = 10, sticky="we")
        else:
            messagebox.showerror("Error", result)        

# Here
class BankPage(Window):
    def __init__(self, account_information):
        self.account_information = account_information
        super().__init__()

    def create_init(self):
        super().create_init(height = 430)

        Button(self.root, text="Exit", font=("Poppins", 13), bg="#000000", fg="#FFFFFF", width=8, height=2, command=self.exit_button).place(x = 418, y = 375)

        label_frame = LabelFrame(self.root, text="My Account", font=("Poppins", 12, "bold"), bg = "#ADD8E6", padx = 10, pady = 10)
        label_frame.pack(padx = 20, pady = 20)

        for i in range(4):
            label_frame.grid_columnconfigure(i, weight = 1)
            label_frame.grid_rowconfigure(i, weight = 1)


        Label(label_frame, text = "Username:", font = ("Poppins", 11, "underline"), bg = "#ADD8E6").grid(row = 0, column = 0, padx = 5, sticky="w")
        username = Label(label_frame, text = self.account_information[1], font = ("Times", 11), bg = "#ADD8E6")
        username.grid(row = 0, column = 1, padx = 5, sticky = "w")
        
        Label(label_frame, text = "Your Balance:", font = ("Poppins", 11, "underline"), bg = "#ADD8E6").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
        global balance
        balance = Label(label_frame, text = f"${self.account_information[5]}", font = ("Times", 11), bg = "#ADD8E6")
        balance.grid(row = 1, column = 1, pady = 5, sticky = "w")

        Button(label_frame, text = "Deposit", font = ("Poppins", 11), width = 20, height = 10, command = lambda: self.withdraw_page(DepositPage)).grid(row = 2, column = 0, rowspan = 3, padx = 5, pady = 5, sticky = "news")
        Button(label_frame, text = "Withdraw", font = ("Poppins", 11), width = 20, height = 10, command = lambda: self.withdraw_page(WithdrawPage)).grid(row = 2, column = 1, rowspan = 3, padx = 5, pady = 5, sticky = "news")
        Button(label_frame, text = "History", font = ("Poppins", 11), width = 20, height = 10).grid(row = 2, column = 2, rowspan = 3, padx = 5, pady = 5, sticky = "news")
        
    def withdraw_page(self, page_class):
        self.root.withdraw()
        page_class(self, self.account_information)

class SystemPage:
    def __init__(self, main_app):
        self.root = Toplevel(main_app.root)
        self.main_app = main_app
        self.db = DatabaseFunction()
        self.create_init()

    def create_init(self, width = 400, height = 430):
        self.root.title("Bank Application")
        self.root.resizable(0, 0)
        self.root.configure(bg = "#ADD8E6")
        
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        Label(self.root, text = "MyBank Banking", font = ("Poppins", 20, "bold"), bg = "#ADD8E6").pack(pady = 5)
        
        Button(self.root, text = "Exit", font = ("Poppins", 13), bg = "#000000", fg = "#FFFFFF", width = 8, height = 2, command = self.exit_button).place(x = 295, y = 375)
        Button(self.root, text = "Back", font = ("Poppins", 13), bg = "#000000", fg = "#FFFFFF", width = 8, height = 2, command = lambda: self.back_to_main()).place(x = 23, y = 375)
        
        self.input_text = StringVar()
        self.amount_entry = Entry(self.root, font=("Poppins", 14), width = 32, justify = RIGHT, textvariable = self.input_text, state = "readonly", fg = "#000000")
        self.amount_entry.pack(ipady = 10)

        label_frame = LabelFrame(self.root, text = "", font = ("Poppins", 12, "bold"), bg = "#ADD8E6", padx = 10, pady = 10)
        label_frame.pack(padx = 20, pady = 20)
        
        for i in range(5):
            label_frame.grid_columnconfigure(i, weight = 1)
            label_frame.grid_rowconfigure(i, weight = 1)
        
        buttons = [
            ('1', 0, 0, 1, 1), ('2', 0, 1, 1, 1), ('3', 0, 2, 1, 1), ('Delete', 0, 3, 1, 1),
            ('4', 1, 0, 1, 1), ('5', 1, 1, 1, 1), ('6', 1, 2, 1, 1),
            ('7', 2, 0, 1, 1), ('8', 2, 1, 1, 1), ('9', 2, 2, 1, 1),
            ('0', 3, 0, 1, 2), ('.', 3, 2, 1, 1),
            ('Enter', 1, 3, 4, 1)
        ]
        
        for (text, row, col, rowspan, colspan) in buttons:
            Button(label_frame, text = text, width = 10, height = 3, command = lambda t = text: self.button_click(t)).grid(row = row, column = col, rowspan = rowspan, columnspan = colspan, padx = 1, pady = 1, sticky = "news")
        
    def button_click(self, item):

        if item == "Enter":
            self.process_transaction()
        elif item == "Delete":
            self.input_text.set(self.input_text.get()[:-1])
            self.update_amount_entry()
        else:
            current_value = self.input_text.get()
            self.input_text.set(current_value + item)
            self.update_amount_entry()
    
    def update_amount_entry(self):
        self.amount_entry.config(state = NORMAL)
        self.amount_entry.delete(0, END)
        self.amount_entry.insert(0, self.input_text.get())
        self.amount_entry.config(state = "readonly")
            
    def back_to_main(self):
        self.root.destroy()
        self.main_app.show_main()
        
    def exit_button(self):
        self.root.quit()
    
    def process_transaction(self):
        raise NotImplementedError("This method should be implemented in subclasses.")
        

class DepositPage(SystemPage):
    def __init__(self, main_app, account_information):
        self.account_information = account_information
        super().__init__(main_app)
        
    def process_transaction(self):
        amount = self.input_text.get()
        username_id = self.account_information[0]
        username = self.account_information[1]
        
        result = self.db.deposit(username, amount, username_id)  
        
        self.input_text.set("")
        self.update_amount_entry()
        
        balance.config(text = f"{result[1]}")
        
        self.back_to_main()


class WithdrawPage(SystemPage):
    def __init__(self, main_app, account_information):
        self.account_information = account_information
        super().__init__(main_app)

    def process_transaction(self):
        amount = self.input_text.get()
        username_id = self.account_information[0]
        username = self.account_information[1]
        
        result = self.db.withdraw(username, amount, username_id)  
        
        self.input_text.set("")
        self.update_amount_entry()
        
        if len(result) == 2:
            balance.config(text = f"{result[1]}")
        
        self.back_to_main()


# Create an instance of the Main_page class and start the Tkinter main loop
if __name__ == "__main__":
    app = MainPage()
    app.root.mainloop()