import json
import uuid
from datetime import datetime

# 🎯 Account Class
class Account:
    def __init__(self, name, balance=0.0):
        self.id = str(uuid.uuid4())[:8]  # Generate short unique ID
        self.name = name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            print("❌ Deposit amount must be positive.")
            return
        self.balance += amount
        msg = f"[{datetime.now()}] Deposited ₹{amount:.2f}"
        self.transactions.append(msg)
        print("✅", msg)

    def withdraw(self, amount):
        if amount <= 0:
            print("❌ Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("❌ Insufficient balance.")
            return
        self.balance -= amount
        msg = f"[{datetime.now()}] Withdrew ₹{amount:.2f}"
        self.transactions.append(msg)
        print("✅", msg)

    def get_balance(self):
        return self.balance

    def get_history(self):
        return self.transactions

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'balance': self.balance,
            'transactions': self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        acc = cls(data['name'], data['balance'])
        acc.id = data['id']
        acc.transactions = data['transactions']
        return acc

# 🏦 Bank Class
class Bank:
    def __init__(self):
        self.accounts = []

    def create_account(self, name, balance=0.0):
        account = Account(name, balance)
        self.accounts.append(account)
        print(f"✅ Account created for {name}. ID: {account.id}")

    def find_account_by_id(self, acc_id):
        for acc in self.accounts:
            if acc.id == acc_id:
                return acc
        print("❌ Account not found.")
        return None

    def deposit_to_account(self, acc_id, amount):
        account = self.find_account_by_id(acc_id)
        if account:
            account.deposit(amount)

    def withdraw_from_account(self, acc_id, amount):
        account = self.find_account_by_id(acc_id)
        if account:
            account.withdraw(amount)

    def show_account_details(self, acc_id):
        account = self.find_account_by_id(acc_id)
        if account:
            print(f"\n🧾 Account ID: {account.id}")
            print(f"👤 Name     : {account.name}")
            print(f"💰 Balance  : ₹{account.get_balance():.2f}")
            print("📜 Transaction History:")
            for t in account.get_history():
                print("  ", t)

    def save_to_file(self, filename="bank.json"):
        data = [acc.to_dict() for acc in self.accounts]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print("✅ Data saved to bank.json")

    def load_from_file(self, filename="bank.json"):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                self.accounts = [Account.from_dict(acc) for acc in data]
            print("✅ Data loaded from bank.json")
        except FileNotFoundError:
            print("⚠️ No saved data found. Starting fresh.")

# 🧪 Console Menu Interface
def main():
    bank = Bank()
    bank.load_from_file()

    while True:
        print("\n🏦 BankLite Menu:")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. View Balance & History")
        print("5. Save Data")
        print("6. Exit")

        choice = input("👉 Choose an option: ")

        if choice == '1':
            name = input("Enter name: ")
            balance = float(input("Enter starting balance (₹): "))
            bank.create_account(name, balance)

        elif choice == '2':
            acc_id = input("Enter Account ID: ")
            amount = float(input("Enter deposit amount (₹): "))
            bank.deposit_to_account(acc_id, amount)

        elif choice == '3':
            acc_id = input("Enter Account ID: ")
            amount = float(input("Enter withdrawal amount (₹): "))
            bank.withdraw_from_account(acc_id, amount)

        elif choice == '4':
            acc_id = input("Enter Account ID: ")
            bank.show_account_details(acc_id)

        elif choice == '5':
            bank.save_to_file()

        elif choice == '6':
            print("👋 Exiting. Saving data...")
            bank.save_to_file()
            break

        else:
            print("❌ Invalid option. Try again.")

# 🔃 Run the system
main()