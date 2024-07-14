import sqlite3
# import hashlib
from datetime import datetime

class DatabaseFunction:
    """
    This class handles bank account operations such as creating accounts, deposit, withdrawal, and balance inquiry.
    """
    def __init__(self):
        self.conn = sqlite3.connect("database_bank.db")
        self.initialize()
        
    def initialize(self):
        """
        Initialize the database with the required tables and triggers.
        """
        self.conn.executescript('''
            CREATE TABLE IF NOT EXISTS Customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                customer_username VARCHAR(50),
                customer_password TEXT,
                customer_pin_number INTEGER,
                customer_birthdate TEXT,
                customer_gender VARCHAR(6),
                customer_national_id INTEGER NOT NULL UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS Accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                account_username VARCHAR(50),
                account_password TEXT,
                account_pin_number INTEGER,
                account_balance REAL DEFAULT 0
            );
            
            CREATE TABLE IF NOT EXISTS Transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                transaction_username TEXT,
                transaction_date TEXT,
                transaction_withdrawal_history TEXT,
                transaction_deposit_history TEXT,
                transaction_bank_id INTEGER,
                FOREIGN KEY (transaction_bank_id) REFERENCES bank_accounts (account_id)              
            );

            CREATE TRIGGER IF NOT EXISTS insert_bank_account_trigger
            AFTER INSERT ON Customers
            BEGIN
                INSERT INTO Accounts (
                    account_username,
                    account_password,
                    account_pin_number
                )
                VALUES (
                    NEW.customer_username,
                    NEW.customer_password,
                    NEW.customer_pin_number
                );
            END;    
        ''')
        
    # def hash_password(self, password):
    #     """
    #     Hash the password using SHA-256.
    #     """
    #     return hashlib.sha256(password.encode()).hexdigest()

    def create_customer_account(self, information):
        """
        Create a new customer account with the provided information.
        """
        if not all(information):
            return "Please fill in all required fields!"

        username, password, confirm_pwd, create_pin, confirm_pin, birthdate, gender, national_id = information
        
        gender_options = ["Male", "Female", "M", "F"]
        gender = gender.capitalize()
        
        if gender not in gender_options:
            return "Please provid your gender"
     
        if password != confirm_pwd:
            return "Password and Confirm password do not match!"
        
        if create_pin != confirm_pin and not create_pin.isdigit():
            return "Pin and Confirm pin do not match!"
        
        if len(national_id) != 9:
            return "National ID must be 9 Digits!"
        
        if len(create_pin) != 6:
            return "PINs numbers must be 6 Digits!"
             
        try:
            self.conn.execute("""INSERT INTO Customers (customer_username, customer_password, customer_pin_number, customer_birthdate, customer_gender, customer_national_id) 
                VALUES (?, ?, ?, ?, ?, ?)""", (username, password, create_pin, birthdate, gender, national_id))
        except sqlite3.IntegrityError:
            return "Something went wrong: National ID must be unique"
        except sqlite3.Error as e:
            return f"Something went wrong: {e}"
    
        self.conn.commit()
        
        return [200, "Personal information added successfully"]
    
    def valid_bank_account(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM Accounts
                              WHERE account_username = ? AND account_password = ?""", (username, password))
            
            record = cursor.fetchone()

            if record:
                return list(record) 
            else:
                return "No matching record found."
            
        except sqlite3.Error as e:
            return f"Error retrieving record: {e}"
    
    def deposit(self, username, amount, username_bank_id):
        """
        Deposit a specified amount into the bank account.
        """       
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT account_balance FROM Accounts 
                            WHERE account_id = ? AND account_username = ?""", (username_bank_id, username))
            balance = cursor.fetchone()[0]

            new_balance = round(balance + float(amount), 2)

            self.conn.execute("""INSERT INTO Transactions (transaction_username, transaction_date, transaction_deposit_history, transaction_bank_id)
                                 VALUES (?, ?, ?, ?)""", (username, current_date, amount, username_bank_id))
            self.conn.execute("""UPDATE Accounts 
                                 SET account_balance = ? 
                                 WHERE account_username = ? AND account_id = ?""", (new_balance, username, username_bank_id))
            self.conn.commit()
            
            return [f"Deposit of {amount} successful. New balance: {new_balance}", new_balance]
        except sqlite3.Error as e:
            return f"Error updating deposit information: {e}"


    def withdraw(self, username, amount, username_bank_id):
        """
        Withdraw a specified amount from the bank account.
        """
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT account_balance FROM Accounts 
                            WHERE account_id = ? AND account_username = ?""", (username_bank_id, username))
            balance = cursor.fetchone()[0]
            
            amount = float(amount)
            if amount > balance:
                return "Withdrawal amount exceeds account balance"
                
            new_balance = balance - amount           
            new_balance = round(new_balance, 2)

            self.conn.execute("""INSERT INTO Transactions (transaction_username, transaction_date, transaction_withdrawal_history, transaction_bank_id)
                                 VALUES (?, ?, ?, ?)""", (username, current_date, amount, username_bank_id))
            self.conn.execute("""UPDATE Accounts 
                                 SET account_balance = ? 
                                 WHERE account_username = ? AND account_id = ?""", (new_balance, username, username_bank_id))
            self.conn.commit()
            
            return [f"Deposit of {amount} successful. New balance: {new_balance}", new_balance]
        except sqlite3.Error as e:
            return f"Error updating deposit information: {e}"


    def close_db(self):
        """
        Close the database connection.
        """
        self.conn.close()