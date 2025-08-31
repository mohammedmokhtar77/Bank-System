class BankSystem:
    number_of_accounts = 0 
    accounts = []  
    
    # Initialize account info
    def __init__(self , name , balance , email ,password) :
        self.__set_balance(balance) 
        self.__set_name(name)
        self.email = email
        self.password = password 
        BankSystem.number_of_accounts += 1  
        BankSystem.accounts.append(self)
    
    # Check password
    def authenticate(self):
        check_auth = input("Enter Password : ")
        return check_auth == self.password
    
    # Set balance (must be positive)
    def __set_balance(self , balance):
        if isinstance(balance , (int , float)) and balance > 0 :
            self.__balance = balance
        else:
            raise ValueError ("Invalid balance: must be a positive number")
    
    def get_balance(self):
        return self.__balance
    
    # Set name (must be string)
    def __set_name(self , name):
        if isinstance(name , str):
            self.__name = name
        else:
            raise ValueError("Invalid name: must be text")
   
    def get_name(self):
        return self.__name
    
    def deposit(self , amount):   
        if amount > 0:
            self.__balance += amount
        else:
            print("Invalid deposit amount")
    
    def withdraw(self , amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Invalid withdrawal amount")
    
    # Show account info (after password check)
    def display(self):
        if self.authenticate():
             return f"Account name: {self.__name}, Balance: {self.__balance}"
        return "Authentication failed"
    
    # Transfer money between accounts
    def trnsfer(self , to_account , amount , password):
        if not self.authenticate(password):
            return "Authentication failed"
        if amount <= 0:
            return "Invalid transfer amount"
        if self.get_balance() < amount :
            return "Insufficient funds"
        self.withdraw(amount)
        to_account.deposit(amount)
        return f"Transferred {amount} from {self.get_name()} to {to_account.get_name()}"
    
    @classmethod
    def find_account_by_email(cls , email):
        for account in cls.accounts:
            if account.email == email:
                return account
            return None
    
    @classmethod
    def find_account_by_name(cls ,name):
        for account in cls.accounts:
            if account.get_name() == name:
                return account
        return None

# Inherits from BankSystem (adds interest)
class SavingAccount(BankSystem):
    def __init__(self, name , balance , email ,password , interest_rate = 0.03):
        super().__init__(name, balance , email ,password )
        self.interest_rate = interest_rate
    
    def add_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        print(f"Interest of {interest:.2f} added!")
    # Show info + interest rate    
    def display(self):
        base_info = super().display()
        return f"{base_info} (Savings Account, Rate={self.interest_rate*100}%)"

# Inherits from BankSystem (adds transaction fee)
class CheckingAccount(BankSystem):
    def __init__(self, name, balance, email, password , transaction_fee=5):
        super().__init__(name, balance, email, password)
        self.transaction_fee = transaction_fee

    def withdraw(self , amount):
        total = amount + self.transaction_fee
        if amount > 0 and total <= self.get_balance():
            # Call base deposit/withdraw
            super().withdraw(total)
            print(f"Withdrawal of {amount} (+fee {self.transaction_fee}) successful.")
        else:
            print("Insufficient funds for withdrawal + fee") 
    # Show info + fee
    def display(self):
        base_info = super().display()
        return f"{base_info} (Checking Account, Fee={self.transaction_fee})"

# Testing
if __name__ == "__main__":
    acc1 = SavingAccount("Mohammed", 1000, "m.com", "1234", 0.05) 
    acc2 = CheckingAccount("Ali", 500, "a.com", "pass", 10)

    # Deposit + Interest
    acc1.deposit(200) # 1000 + 200 = 1200
    acc1.add_interest() # (1200) + (1200 * 0.05) = 1260

    # Withdraw with fee
    acc2.withdraw(100) # 500 - (100+10) = 390

    # Display (With Right And Wrong Password)
    print(acc1.display())  
    print(acc2.display())  

    # Transfer money form acc1 to acc2
    print(acc1.trnsfer(acc2, 200, "1234"))  # Right Password
    print(acc1.get_balance())  # Decreasing -> 200
    print(acc2.get_balance())  # increasing -> 200

    # wrong password
    print(acc1.trnsfer(acc2, 50, "wrong"))

    # Searching by name
    found_acc = BankSystem.find_account_by_name("Ali")
    if found_acc:
        print("Found by name:", found_acc.get_name(), found_acc.get_balance())

    # Searching by email
    found_acc2 = BankSystem.find_account_by_email("m.com")
    if found_acc2:
        print("Found by email:", found_acc2.get_name(), found_acc2.get_balance())

    # Total accounts
    print("Total accounts created:", BankSystem.number_of_accounts)

