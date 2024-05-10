from system_function import Database, BankAccount
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox

class BankApplication:
    def __init__(self):
        self.tk = Tk()
        self.db = Database("database.db")
        self.gender_var = StringVar()
        self.initialize_gui()
        self.center_window(self.tk)

    def open_exit(self, function_name):
        self.tk.withdraw()
        getattr(self, function_name)()
        
    def destroy_message_box(self):
        self.tk.withdraw()
        
    def center_window(self, window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        
        
    def initialize_gui(self):
        self.tk.title("Bank System")
        self.tk.geometry("629x393")
        self.tk.resizable(0, 0)
        self.tk.configure(bg="light blue")

        
        label = Label(self.tk, text="MyBANK Banking", font=("Arial", 20))
        label.grid(row=2, column=5, columnspan=13, padx=200)

        username_label = Label(self.tk, text="Username:", font=("Arial", 11, "bold"))
        username_label.grid(row=29, column=14)

        self.username_entry = Entry(self.tk)
        self.username_entry.grid(row=29, column=15, padx=10, pady=5)

        password_label = Label(self.tk, text="Password:", font=("Arial", 11, "bold"))
        password_label.grid(row=30, column=14)

        self.password_entry = Entry(self.tk, show="*") 
        self.password_entry.grid(row=30, column=15, padx=10, pady=5)

        open_account_btn = Button(self.tk, text="Open Bank Account", font=("Arial", 10), command=lambda: self.open_exit("create_bank_account"), width=20, height=10)
        open_account_btn.grid(row=20, column=7, rowspan=21, columnspan=7, padx=10, pady=60)

        login_btn = Button(self.tk, text="Login", font=("Arial", 10, "bold"), command=self.login_account, width=10)
        login_btn.grid(row=33, column=15, padx=10, pady=5, sticky="ew")

        exit_btn = Button(self.tk, text="Exit", font=("Arial", 15, "bold"), command=self.exit_button, width=12)
        exit_btn.grid(row=41, column=15, padx=5, pady=10, sticky="se")

    def create_bank_account(self):
        self.bank_account_window = Toplevel(self.tk)
        self.bank_account_window.title("User Information")
        self.bank_account_window.geometry("500x650")
        self.bank_account_window.resizable(0, 0)
        self.bank_account_window.configure(bg="light gray")
        self.center_window(self.bank_account_window) 

        header_frame = Frame(self.bank_account_window, bg="light gray")
        header_frame.pack(pady=20)

        bank_label = Label(header_frame, text="MyBANK Banking", font=("Arial", 20,), bg="light gray")
        bank_label.pack()

        box_label = Label(self.bank_account_window, text="Register Bank Account", font=("Arial", 12, "underline"), bg="light gray")
        box_label.pack(pady= 21)

        user_info_frame = Frame(self.bank_account_window, bg="light gray")
        user_info_frame.pack(pady=10)

        labels = ["First name:", "Last name:", "Password:", "Confirm Password:", 
                  "Create PIN (4 Digits):", "Confirm PIN:", "Birthdate (YYYY-MM-DD):", "Gender:", "Nation ID (9 Digits):"]

        for i, label_text in enumerate(labels):
            label = Label(user_info_frame, text=label_text, font=("Arial", 12))
            label.grid(row=i, column=0, padx=20, pady=10, sticky="w")

        self.ask_first_name_entry = Entry(user_info_frame)
        self.ask_first_name_entry.grid(row=0, column=1, padx=20, pady=10)

        self.ask_last_name_entry = Entry(user_info_frame)
        self.ask_last_name_entry.grid(row=1, column=1, padx=20, pady=10)

        self.ask_password_entry = Entry(user_info_frame, show="*")
        self.ask_password_entry.grid(row=2, column=1, padx=20, pady=10)

        self.confirm_password_entry = Entry(user_info_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=20, pady=10)

        self.ask_pin_number_entry = Entry(user_info_frame, show="*")
        self.ask_pin_number_entry.grid(row=4, column=1, padx=20, pady=10)

        self.confirm_pin_entry = Entry(user_info_frame, show="*")
        self.confirm_pin_entry.grid(row=5, column=1, padx=20, pady=10)

        self.ask_birthdate_entry = Entry(user_info_frame)
        self.ask_birthdate_entry.grid(row=6, column=1, padx=20, pady=10)

        gender_var = StringVar()
        self.gender_var = gender_var  
        gender_combobox = Combobox(user_info_frame, textvariable=gender_var, values=["Male", "Female"])
        gender_combobox.grid(row=7, column=1, padx=20, pady=10)

        self.ask_national_id_entry = Entry(user_info_frame)
        self.ask_national_id_entry.grid(row=8, column=1, padx=20, pady=10)

        create_account_btn = Button(self.bank_account_window, text="Create Account", command=self.create_account, font=("Arial", 13, "bold"))
        create_account_btn.pack(pady= 25)


    def create_account(self):
        first_name = self.ask_first_name_entry.get().strip()
        last_name = self.ask_last_name_entry.get().strip()
        password = self.ask_password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        pin = self.ask_pin_number_entry.get().strip()
        confirm_pin = self.confirm_pin_entry.get().strip()
        birthdate = self.ask_birthdate_entry.get().strip()
        gender = self.gender_var.get().strip()
        national_id = self.ask_national_id_entry.get().strip()

        if not all([first_name, last_name, password, confirm_password, pin, confirm_pin, birthdate, gender, national_id]):
            messagebox.showerror("Error", "Please fill in all required fields.")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
        elif len(national_id) < 9 or len(national_id) > 9:
            messagebox.showerror("Error", "National ID must be 9 Digits!")
        elif len(pin) < 4 or len(pin) > 4:
            messagebox.showerror("Error", "PINs numbers must be 4 Digits!")
        elif pin != confirm_pin:
            messagebox.showerror("Error", "PINs do not match.")
        else:
            self.db.add_personal_information(first_name, last_name, password, pin, birthdate, gender, national_id)
            messagebox.showinfo("Success", "Account created successfully!")

            self.tk.destroy()
  

    def deposit_btn(self, bank_account, bank_id, national_id, full_name):
        amount = int(self.bank_number())

        if amount is not None: 
            bank_account.deposit(self.db.conn, amount, national_id, full_name, bank_id)
 
            updated_balance = bank_account.get_balance()
            messagebox.showinfo("Success",f"Deposit of ${amount} successful!\n\nNew balance: ${updated_balance}")
            
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def withdraw_btn(self, bank_account, bank_id, national_id, full_name):
        amount = int(self.bank_number())
        
        if amount is not None: 
            bank_account.withdraw(self.db.conn, amount, national_id, full_name, bank_id)
            updated_balance = bank_account.get_balance()
            messagebox.showinfo("Success",f"Withdraw of ${amount} successful!\n\nNew balance: ${updated_balance}")
            
        else:
            messagebox.showerror("Error", "Please enter a valid amount.")

    def exit_button(self):
        self.tk.destroy()
 

    def login_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = self.db.check_bank_account(username, password)
        authenticated = isinstance(result, list)
        
        if authenticated:
            success_window = Toplevel(self.tk)
            success_window.title("Success")
            success_window.geometry("150x80")
            self.center_window(success_window)
            
            success_label = Label(success_window, text="Login successful!", font=("Arail", 13))
            success_label.pack(pady=20)
            
            success_window.after(1500, success_window.destroy)
            
            bank_account = BankAccount(account_holder=username, balance=result[5])
            
            bank_id = result[0]
            national_id = result[4]
            full_name = " ".join(result[1:3])
            
            self.tk.withdraw() 
            
            self.tk.after(2000, lambda: self.bank_account_window(username, bank_account, bank_id, national_id, full_name))
            
        else:
            messagebox.showerror("Error", "Authentication failed. Please try again.")
            
        self.tk.mainloop()
            


    def bank_number(self):
        top = Toplevel()
        top.geometry("345x290")
        top.resizable(0, 0)
        self.center_window(top) 

        input_text = StringVar()
        expression = ""
        
        def btn_click(item):
            nonlocal expression 
            if item == "Enter":
                top.destroy()  
                
            else:
                expression = expression + str(item)
                input_text.set(expression)

        input_frame = Frame(top, width=312, height=50)
        input_frame.pack(side=TOP)

        input_field = Entry(input_frame, font=('arial', 18, 'bold'), width=45, justify=RIGHT, textvariable=input_text)
        input_field.grid(row=0, column=0)
        input_field.pack(ipady=10) 

        btns_frame = Frame(top, width=310, height=270)
        btns_frame.pack()

        Button(btns_frame, text="7", width=10, height=3, command = lambda: btn_click(7)).grid(row=1, column=0, padx=1, pady=1)
        Button(btns_frame, text="8", width=10, height=3, command = lambda: btn_click(8)).grid(row=1, column=1, padx=1, pady=1)
        Button(btns_frame, text="9", width=10, height=3, command = lambda: btn_click(9)).grid(row=1, column=2, padx=1, pady=1)

        Button(btns_frame, text="4", width=10, height=3, command = lambda: btn_click(4)).grid(row=2, column=0, padx=1, pady=1)
        Button(btns_frame, text="5", width=10, height=3, command = lambda: btn_click(5)).grid(row=2, column=1, padx=1, pady=1)
        Button(btns_frame, text="6", width=10, height=3, command = lambda: btn_click(6)).grid(row=2, column=2, padx=1, pady=1)

        Button(btns_frame, text="1", width=10, height=3, command = lambda: btn_click(1)).grid(row=3, column=0, padx=1, pady=1)
        Button(btns_frame, text="2", width=10, height=3, command = lambda: btn_click(2)).grid(row=3, column=1, padx=1, pady=1)
        Button(btns_frame, text="3", width=10, height=3, command = lambda: btn_click(3)).grid(row=3, column=2, padx=1)
        Button(btns_frame, text="0", width=24, height=3, command = lambda: btn_click(0)).grid(row=4, column=0, columnspan=2, padx=1, pady=1)
        Button(btns_frame, text=".", width=10, height=3, command = lambda: btn_click('.')).grid(row=4, column=2, padx=1, pady=1)

        Button(btns_frame, text="Enter", width=10, height=15, command = lambda: btn_click("Enter")).grid(row=1, column=3, rowspan=5, padx=1, pady=1)

        top.wait_window(top) 
        return eval(input_text.get())
            
    def bank_account_window(self, username, bank_account, bank_id, national_id, full_name):
        bank_window = Toplevel()
        bank_window.geometry("500x400")
        bank_window.resizable(0, 0)
        bank_window.title("Bank Account")
        bank_window.configure(bg="light blue")
        self.center_window(bank_window)
        

        bank_title = Label(bank_window, text="MyBANK Banking", font=("Arial", 20))
        bank_title.grid(row=0, column=0, columnspan=3)

        account_label = Label(bank_window, text=f"Account Username: {username}", font=("Arial", 10))
        account_label.grid(row=2, column=0, padx=30, pady=20, sticky=W)

        deposit = Button(bank_window, text="Deposit", command=lambda: self.deposit_btn(bank_account, bank_id, national_id, full_name), width=25, height=12)
        deposit.grid(row=4, column=0, padx=35, pady=15)

        withdraw = Button(bank_window, text="Withdraw", command=lambda: self.withdraw_btn(bank_account, bank_id, national_id, full_name), width=25, height=12)
        withdraw.grid(row=4, column=2, padx=30, pady=10)

        exit_btn = Button(bank_window, text="Exit", command=self.exit_button, width=13, height=3)
        exit_btn.grid(row=5, column=2, padx=30, pady=10, sticky=E)
        

if __name__ == '__main__':
    app = BankApplication()
    app.tk.mainloop()
