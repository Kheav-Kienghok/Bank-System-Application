import sqlite3
from datetime import datetime

class BankAccount:
    def __init__(self, account_holder, balance=0, account_number=None):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, conn, amount, national_id, full_name, bank_id):
        if amount <= 0:
            return "Invalid input"
    
        self.balance += amount
        
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            cursor = conn.cursor()
        
            conn.execute("""INSERT INTO bank_transactions (bank_transaction_full_name, bank_transaction_date, bank_transaction_deposit_history, bank_transaction_bank_id)
                         VALUES (?, ?, ?, ?)""", (full_name, current_date, amount, bank_id))

   
            cursor.execute("""UPDATE bank_accounts 
                    SET bank_account_balance = ? 
                    WHERE bank_account_national_id = ?""", (self.balance, national_id))
            
            conn.commit()
            return f"Deposit of {amount} successful. New balance: {self.balance}"
        
        except sqlite3.Error as e:
            return f"Error updating deposit information: {e}"

    def withdraw(self, conn, amount, national_id, full_name, bank_id):
        if amount <= 0:
            return "Invalid input"
        elif amount > self.balance:
            return "Insufficient funds"
        self.balance -= amount
        
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute("""INSERT INTO bank_transactions (bank_transaction_full_name, bank_transaction_date, bank_transaction_withdrawal_history, bank_transaction_bank_id)
                VALUES (?, ?, ?, ?)""", (full_name, current_date, amount, bank_id))
        
        try:
            cursor = conn.cursor()
            cursor.execute("""UPDATE bank_accounts 
                    SET bank_account_balance = ? 
                    WHERE bank_account_national_id = ?""", (self.balance, national_id))
            
            conn.commit()
            return f"Withdrawal of {amount} successful. New balance: {self.balance}"
        except sqlite3.Error as e:
            return f"Error updating withdrawal information: {e}"

    def get_balance(self):
        return self.balance

class Database:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def initialize(self):
        try:
            self.conn.executescript('''
                CREATE TABLE IF NOT EXISTS personal_accounts (
                    personal_account_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    personal_account_first_name CHAR(50),
                    personal_account_surname CHAR(50),
                    personal_account_password TEXT,
                    personal_account_pin_number INTEGER,
                    personal_account_birthday TEXT,
                    personal_account_gender CHAR(6),
                    personal_national_id INTEGER NOT NULL UNIQUE
                );
                
                CREATE TABLE IF NOT EXISTS bank_accounts (
                    bank_account_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    bank_account_first_name CHAR(50),
                    bank_account_surname CHAR(50),
                    bank_account_pin_number INTEGER,
                    bank_account_national_id INTEGER NOT NULL,
                    bank_account_balance REAL DEFAULT 0,
                    FOREIGN KEY (bank_account_national_id) REFERENCES personal_accounts (personal_national_id)
                );
                
                CREATE TABLE IF NOT EXISTS bank_transactions (
                    bank_transaction_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    bank_transaction_full_name TEXT,
                    bank_transaction_date TEXT,
                    bank_transaction_withdrawal_history TEXT,
                    bank_transaction_deposit_history TEXT,
                    bank_transaction_bank_id INTEGER,
                    FOREIGN KEY (bank_transaction_bank_id) REFERENCES bank_accounts (bank_account_id)              
                );

                CREATE TRIGGER IF NOT EXISTS insert_bank_account_trigger
                AFTER INSERT ON personal_accounts
                BEGIN
                    INSERT INTO bank_accounts (
                        bank_account_first_name,
                        bank_account_surname,
                        bank_account_pin_number,
                        bank_account_national_id
                    )
                    VALUES (
                        NEW.personal_account_first_name,
                        NEW.personal_account_surname,
                        NEW.personal_account_pin_number,
                        NEW.personal_national_id
                    );
                END;
            ''')

            # print("Database connection established successfully.")
        except sqlite3.Error as e:
            print("Error connecting to the database:", e)

    def add_personal_information(self, first_name, last_name, password, pin_number, birthday, gender, national_id):
        try:
            self.conn.execute("""INSERT INTO personal_accounts (personal_account_first_name, personal_account_surname, personal_account_password, personal_account_pin_number, personal_account_birthday, personal_account_gender, personal_national_id) 
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (first_name, last_name, password, pin_number, birthday, gender, national_id))
            self.conn.commit()
            return "Personal information added successfully"
        except sqlite3.Error as e:
            return f"Error adding personal information: {e}"

    def check_bank_account(self, name, pin):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""SELECT * FROM bank_accounts 
                              WHERE bank_account_first_name = ? AND bank_account_pin_number = ?""", (name, pin))
            record = cursor.fetchone()

            if record:
                return list(record)

            return "No matching record found."
        except sqlite3.Error as e:
            print(f"Error retrieving record: {e}")
            return None

    def close(self):
        self.conn.close()




def main():
    db = Database("database.db")

    db.initialize()
    
    db.close()
    
if __name__ == "__main__":
    main()