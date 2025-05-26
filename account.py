class Account:
    def __init__(self, name):
        self.name = name
        self.deposits = []
        self.withdrawals = []
        self.loan_taken = []
        self.loan_repaid = []
        self.transfers = []  
        self.received = []   
        
    def deposit(self, amount):
        if amount > 0:
            self.deposits.append(amount)
            print(f"Deposited ${amount}")
        else:
            print("Deposit amount must be positive")
    def withdraw(self, amount):
        if amount > 0 and self.get_balance() >= amount:
            self.withdrawals.append(amount)
            print(f"Withdrew ${amount}")
        else:
            print("Withdrawal failed: Insufficient funds or invalid amount")
            
    def get_balance(self):
        total_deposit = sum(self.deposits)
        total_withdrawal = sum(self.withdrawals)
        return total_deposit - total_withdrawal
    
    def show_balance(self):
        print(f"{self.name}'s Balance: ${self.get_balance()}")
    def transfer(self, amount, receiver_account):
        if amount > 0 and self.get_balance() >= amount:
            self.withdrawals.append(amount)
            receiver_account.deposits.append(amount)
            self.transfers.append((amount, receiver_account.name))
            receiver_account.received.append((amount, self.name))
            print(f"Transferred ${amount} to {receiver_account.name}")
        else:
            print("Transfer failed: Insufficient balance or invalid amount")
    def get_loan(self, amount):
        if amount > 0:
            self.loan_taken.append(amount)
            self.deposits.append(amount)
            print(f"Loan of ${amount} taken successfully")
        else:
            print("Loan amount must be positive")
    def repay_loan(self, amount):
        if amount > 0 and self.get_balance() >= amount:
            total_loan = sum(self.loan_taken) - sum(self.loan_repaid)
            if amount <= total_loan:
                self.withdrawals.append(amount)
                self.loan_repaid.append(amount)
                print(f"Repaid ${amount} of loan")
            else:
                print("You cannot repay more than the loan you owe")
        else:
            print("Repayment failed: Insufficient balance or invalid amount")
    def get_statement(self):
        print(f"{self.name}'s Transaction History:")
        print("Deposits:", self.deposits)
        print("Withdrawals:", self.withdrawals)
        print("Transfers Sent:", self.transfers)
        print("Transfers Received:", self.received)
    def get_loan_statement(self):
        print(f"{self.name}'s Loan History:")
        print("Loans Taken:", self.loan_taken)
        print("Loans Repaid:", self.loan_repaid)
        loan_balance = sum(self.loan_taken) - sum(self.loan_repaid)
        print(f"Current Loan Balance: ${loan_balance}")
        
a1 = Account("Alice")
a2 = Account("Bob")
a1.deposit(1000)
a1.withdraw(200)
a1.transfer(300, a2)
a1.get_loan(500)
a1.repay_loan(100)
a1.show_balance()
a2.show_balance()
a1.get_statement()
a2.get_statement()
a1.get_loan_statement()