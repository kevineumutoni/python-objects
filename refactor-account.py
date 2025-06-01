import datetime

class Transaction:
    def __init__(self, transaction_type, amount, narration=""):
        self.date_time = datetime.datetime.now()
        self.transaction_type = transaction_type
        self.amount = amount
        self.narration = narration

    def __str__(self):
        return f"{self.date_time.strftime('%Y-%m-%d %H:%M:%S')} - {self.narration}: {self.transaction_type} ${self.amount:.2f}"

class Account:
    def __init__(self, account_number, owner, initial_deposit=0):
        self._account_number = account_number
        self._owner = owner
        self._transactions = []
        self._is_frozen = False
        self._is_closed = False
        self._minimum_balance = 0
        if initial_deposit > 0:
            self._transactions.append(Transaction('deposit', initial_deposit, "Initial deposit"))
    
    def get_account_number(self):
        return self._account_number
    
    def get_owner(self):
        return self._owner
    
    def is_frozen(self):
        return self._is_frozen
    
    def is_closed(self):
        return self._is_closed
    
    def deposit(self, amount):
        if self._is_closed:
            return "Account closed. Operation not allowed."
        if self._is_frozen:
            return "Account frozen. Operation not allowed."
        if amount <= 0:
            return "Deposit amount must be positive."
        self._transactions.append(Transaction('deposit', amount, "Deposit"))
        balance = self.get_balance()
        return f"Deposited ${amount:.2f}. New balance: ${balance:.2f}"
    
    def withdraw(self, amount):
        if self._is_closed:
            return "Account closed. Operation not allowed."
        if self._is_frozen:
            return "Account frozen. Operation not allowed."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        current_balance = self.get_balance()
        if current_balance - amount < 0:
            return "Withdrawal failed: account cannot be overdrawn."
        if current_balance - amount < self._minimum_balance:
            return f"Withdrawal failed: balance would fall below the minimum balance of ${self._minimum_balance:.2f}."
        self._transactions.append(Transaction('withdrawal', amount, "Withdrawal"))
        new_balance = self.get_balance()
        return f"Withdrew ${amount:.2f}. New balance: ${new_balance:.2f}"
    
    def transfer_funds(self, amount, other_account):
        if self._is_closed or other_account.is_closed():
            return "One or both accounts are closed. Operation not allowed."
        if self._is_frozen or other_account.is_frozen():
            return "One or both accounts are frozen. Operation not allowed."
        if amount <= 0:
            return "Transfer amount must be positive."
        current_balance = self.get_balance()
        if current_balance - amount < 0:
            return "Transfer failed: insufficient funds."
        if current_balance - amount < self._minimum_balance:
            return f"Transfer failed: balance would fall below the minimum balance of ${self._minimum_balance:.2f}."
        self._transactions.append(Transaction('withdrawal', amount, f"Transfer to account {other_account.get_account_number()}"))
        other_account._transactions.append(Transaction('deposit', amount, f"Transfer from account {self._account_number}"))
        new_balance = self.get_balance()
        return f"Transferred ${amount:.2f} to account {other_account.get_account_number()}. Your new balance: ${new_balance:.2f}"
    
    def get_balance(self):
        balance = 0
        for transaction in self._transactions:
            if transaction.transaction_type in ['deposit', 'loan', 'interest']:
                balance += transaction.amount
            elif transaction.transaction_type in ['withdrawal', 'repayment']:
                balance -= transaction.amount
        return balance
    
    def request_loan(self, amount):
        if self._is_closed:
            return "Account closed. Operation not allowed."
        if self._is_frozen:
            return "Account frozen. Operation not allowed."
        if amount <= 0:
            return "Loan amount must be positive."
        self._transactions.append(Transaction('loan', amount, "Loan granted"))
        balance = self.get_balance()
        return f"Loan of ${amount:.2f} granted. New balance: ${balance:.2f}"
    
    def repay_loan(self, amount):
        if self._is_closed:
            return "Account closed. Operation not allowed."
        if self._is_frozen:
            return "Account frozen. Operation not allowed."
        if amount <= 0:
            return "Repayment amount must be positive."
        self._transactions.append(Transaction('repayment', amount, "Loan repayment"))
        balance = self.get_balance()
        return f"Repaid ${amount:.2f} of the loan. New balance: ${balance:.2f}"
    
    def view_account_details(self):
        balance = self.get_balance()
        return f"Account Owner: {self._owner}, Current Balance: ${balance:.2f}"
    
    def change_account_owner(self, new_owner):
        self._owner = new_owner
        return f"Account owner updated to: {new_owner}"
    
    def account_statement(self):
        if not self._transactions:
            print("No transactions.")
            return
        for i, transaction in enumerate(self._transactions, 1):
            print(f"{i}. {transaction}")
    
    def apply_interest(self):
        if self._is_closed:
            return "Account closed. Operation not allowed."
        if self._is_frozen:
            return "Account frozen. Operation not allowed."
        balance = self.get_balance()
        interest = balance * 0.05
        self._transactions.append(Transaction('interest', interest, "Interest applied"))
        new_balance = self.get_balance()
        return f"Applied interest: ${interest:.2f}. New balance: ${new_balance:.2f}"
    
    def freeze_account(self):
        self._is_frozen = True
        return "Account frozen."
    
    def unfreeze_account(self):
        self._is_frozen = False
        return "Account unfrozen."
    
    def set_minimum_balance(self, min_balance):
        self._minimum_balance = min_balance
        return f"Minimum balance set to ${min_balance:.2f}"
    
    def close_account(self):
        if not self._is_closed:
            self._is_closed = True
            self._transactions = []
            return "Account closed. All transactions cleared."
        return "Account already closed."
