import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from typing import Optional

class BankSystem:
    number_of_accounts = 0 
    accounts = []  
    
    # Initialize account info
    def __init__(self, name, balance, email, password):
        self.__set_balance(balance) 
        self.__set_name(name)
        self.email = email
        self.password = password 
        BankSystem.number_of_accounts += 1  
        BankSystem.accounts.append(self)
   
    # Check password
    def authenticate(self, password):
        return password == self.password
    
    # Set balance (must be positive)
    def __set_balance(self, balance):
        if isinstance(balance, (int, float)) and balance > 0:
            self.__balance = balance
        else:
            raise ValueError("Invalid balance: must be a positive number")
    
    def get_balance(self):
        return self.__balance
    # Set name (must be string)    
    def __set_name(self, name):
        if isinstance(name, str) and name.strip():
            self.__name = name
        else:
            raise ValueError("Invalid name: must be text")
   
    def get_name(self):
        return self.__name
    
    def deposit(self, amount):   
        if amount > 0:
            self.__balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False
    # Transfer money between accounts    
    def transfer(self, to_account, amount, password):
        if not self.authenticate(password):
            return "Authentication failed"
        if amount <= 0:
            return "Invalid transfer amount"
        if self.get_balance() < amount:
            return "Insufficient funds"
        self.withdraw(amount)
        to_account.deposit(amount)
        return f"Transferred ${amount:.2f} from {self.get_name()} to {to_account.get_name()}"
    
    @classmethod
    def find_account_by_email(cls, email):
        for account in cls.accounts:
            if account.email == email:
                return account
        return None
    
    @classmethod
    def find_account_by_name(cls, name):
        for account in cls.accounts:
            if account.get_name() == name:
                return account
        return None

# Inherits from BankSystem (adds interest)
class SavingAccount(BankSystem):
    def __init__(self, name, balance, email, password, interest_rate=0.03):
        super().__init__(name, balance, email, password)
        self.interest_rate = interest_rate
    
    def add_interest(self):
        interest = self.get_balance() * self.interest_rate
        self.deposit(interest)
        return interest
    
    def get_account_type(self):
        return f"Savings (Rate: {self.interest_rate*100}%)"

# Inherits from BankSystem (adds transaction fee)
class CheckingAccount(BankSystem):
    def __init__(self, name, balance, email, password, transaction_fee=5):
        super().__init__(name, balance, email, password)
        self.transaction_fee = transaction_fee

    def withdraw(self, amount):
        total = amount + self.transaction_fee
        if amount > 0 and total <= self.get_balance():
            super().withdraw(total)
            return True
        return False
    
    def get_account_type(self):
        return f"Checking (Fee: ${self.transaction_fee})"

class BankGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Management System")
        self.root.geometry("900x650")
        self.root.configure(bg='#f0f0f0')
        
        # Current logged-in account
        self.current_account = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main title
        title_label = tk.Label(self.root, text="Bank Management System", 
                              font=("Arial", 20, "bold"), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=20)
        
        # Main frame
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left frame for account operations
        self.left_frame = tk.LabelFrame(self.main_frame, text="Account Operations", 
                                       font=("Arial", 12, "bold"), bg='#f0f0f0')
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Right frame for account info
        self.right_frame = tk.LabelFrame(self.main_frame, text="Account Information", 
                                        font=("Arial", 12, "bold"), bg='#f0f0f0')
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.create_left_panel()
        self.create_right_panel()
    
    def create_left_panel(self):
        # Create Account Section
        create_frame = tk.LabelFrame(self.left_frame, text="Create New Account", bg='#f0f0f0')
        create_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(create_frame, text="Create Savings Account", 
                 command=self.create_savings_account, bg='#4CAF50', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=5, padx=10, fill=tk.X)
        
        tk.Button(create_frame, text="Create Checking Account", 
                 command=self.create_checking_account, bg='#2196F3', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=5, padx=10, fill=tk.X)
        
        # Login Section
        login_frame = tk.LabelFrame(self.left_frame, text="Account Login", bg='#f0f0f0')
        login_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(login_frame, text="Login to Account", 
                 command=self.login_account, bg='#FF9800', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=5, padx=10, fill=tk.X)
        
        tk.Button(login_frame, text="Logout", 
                 command=self.logout_account, bg='#F44336', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=5, padx=10, fill=tk.X)
        
        # Transaction Section
        transaction_frame = tk.LabelFrame(self.left_frame, text="Transactions", bg='#f0f0f0')
        transaction_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(transaction_frame, text="Deposit Money", 
                 command=self.deposit_money, bg='#8BC34A', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=2, padx=10, fill=tk.X)
        
        tk.Button(transaction_frame, text="Withdraw Money", 
                 command=self.withdraw_money, bg='#FF5722', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=2, padx=10, fill=tk.X)
        
        tk.Button(transaction_frame, text="Transfer Money", 
                 command=self.transfer_money, bg='#9C27B0', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=2, padx=10, fill=tk.X)
        
        # Special Operations Section
        special_frame = tk.LabelFrame(self.left_frame, text="Special Operations", bg='#f0f0f0')
        special_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Button(special_frame, text="Add Interest (Savings)", 
                 command=self.add_interest, bg='#607D8B', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=2, padx=10, fill=tk.X)
        
        tk.Button(special_frame, text="View All Accounts", 
                 command=self.view_all_accounts, bg='#795548', fg='white',
                 font=("Arial", 10, "bold")).pack(pady=2, padx=10, fill=tk.X)
    
    def create_right_panel(self):
        # Main container with gradient-like background
        self.account_info_frame = tk.Frame(self.right_frame, bg='#f8f9fa')
        self.account_info_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Header frame
        header_frame = tk.Frame(self.account_info_frame, bg='#2c3e50', height=60)
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        header_frame.pack_propagate(False)
        
        self.header_label = tk.Label(header_frame, text="💳 ACCOUNT DASHBOARD", 
                                    font=("Arial", 14, "bold"), fg='white', bg='#2c3e50')
        self.header_label.pack(expand=True)
        
        # Account details frame with card-like design
        self.details_frame = tk.Frame(self.account_info_frame, bg='white', relief=tk.RAISED, bd=2)
        self.details_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create account info labels
        self.create_account_info_widgets()
        
        # Stats frame at bottom
        self.stats_frame = tk.Frame(self.account_info_frame, bg='#ecf0f1', height=80, relief=tk.GROOVE, bd=1)
        self.stats_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        self.stats_frame.pack_propagate(False)
        
        self.stats_label = tk.Label(self.stats_frame, text="", font=("Arial", 10, "bold"), 
                                   bg='#ecf0f1', fg='#2c3e50')
        self.stats_label.pack(expand=True)
        
        self.update_info_display()
    
    def create_account_info_widgets(self):
        # Profile section
        profile_frame = tk.Frame(self.details_frame, bg='white')
        profile_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Profile icon and name
        profile_header = tk.Frame(profile_frame, bg='white')
        profile_header.pack(fill=tk.X, pady=(0, 15))
        
        self.profile_icon = tk.Label(profile_header, text="👤", font=("Arial", 24), bg='white')
        self.profile_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        self.name_label = tk.Label(profile_header, text="", font=("Arial", 16, "bold"), 
                                  bg='white', fg='#2c3e50')
        self.name_label.pack(side=tk.LEFT, anchor=tk.W)
        
        # Account info grid
        info_grid = tk.Frame(profile_frame, bg='white')
        info_grid.pack(fill=tk.X, pady=10)
        
        # Balance display (prominent)
        balance_container = tk.Frame(info_grid, bg='#3498db', relief=tk.RAISED, bd=2)
        balance_container.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(balance_container, text="💰 CURRENT BALANCE", font=("Arial", 10, "bold"), 
                bg='#3498db', fg='white').pack(pady=(10, 5))
        
        self.balance_label = tk.Label(balance_container, text="$0.00", 
                                     font=("Arial", 20, "bold"), bg='#3498db', fg='white')
        self.balance_label.pack(pady=(0, 10))
        
        # Account details in styled boxes
        details_container = tk.Frame(info_grid, bg='white')
        details_container.pack(fill=tk.X, pady=10)
        
        # Email box
        email_box = tk.Frame(details_container, bg='#ecf0f1', relief=tk.GROOVE, bd=1)
        email_box.pack(fill=tk.X, pady=2)
        
        tk.Label(email_box, text="📧 Email:", font=("Arial", 9, "bold"), 
                bg='#ecf0f1', fg='#7f8c8d').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.email_label = tk.Label(email_box, text="", font=("Arial", 10), 
                                   bg='#ecf0f1', fg='#2c3e50')
        self.email_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Account type box
        type_box = tk.Frame(details_container, bg='#ecf0f1', relief=tk.GROOVE, bd=1)
        type_box.pack(fill=tk.X, pady=2)
        
        tk.Label(type_box, text="🏦 Account Type:", font=("Arial", 9, "bold"), 
                bg='#ecf0f1', fg='#7f8c8d').pack(anchor=tk.W, padx=10, pady=(5, 0))
        
        self.type_label = tk.Label(type_box, text="", font=("Arial", 10), 
                                  bg='#ecf0f1', fg='#2c3e50')
        self.type_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
        
        # Status indicator
        self.status_frame = tk.Frame(profile_frame, bg='white')
        self.status_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.status_indicator = tk.Label(self.status_frame, text="🔴 Not Logged In", 
                                        font=("Arial", 10, "bold"), bg='white', fg='#e74c3c')
        self.status_indicator.pack()
    
    def update_info_display(self):
        if self.current_account:
            # Update logged in account info
            self.header_label.config(text="💳 ACCOUNT DASHBOARD", fg='white')
            self.name_label.config(text=self.current_account.get_name())
            self.balance_label.config(text=f"${self.current_account.get_balance():,.2f}")
            self.email_label.config(text=self.current_account.email)
            
            # Determine account type with icon
            if isinstance(self.current_account, SavingAccount):
                account_type = f"💰 Savings Account"
                details = f"Interest Rate: {self.current_account.interest_rate*100}%"
                self.type_label.config(text=f"{account_type}\n{details}")
            elif isinstance(self.current_account, CheckingAccount):
                account_type = f"💳 Checking Account"
                details = f"Transaction Fee: ${self.current_account.transaction_fee}"
                self.type_label.config(text=f"{account_type}\n{details}")
            else:
                self.type_label.config(text="🏛️ Standard Account")
            
            # Update status
            self.status_indicator.config(text="🟢 Logged In", fg='#27ae60')
            
            # Update stats
            self.stats_label.config(text=f"📊 Total Accounts in System: {BankSystem.number_of_accounts}")
            
            # Change balance color based on amount
            balance = self.current_account.get_balance()
            if balance > 1000:
                self.balance_label.config(bg='#27ae60')  # Green for good balance
                balance_container = self.balance_label.master
                balance_container.config(bg='#27ae60')
                balance_container.children['!label'].config(bg='#27ae60')  # Header label
            elif balance > 100:
                self.balance_label.config(bg='#f39c12')  # Orange for medium balance  
                balance_container = self.balance_label.master
                balance_container.config(bg='#f39c12')
                balance_container.children['!label'].config(bg='#f39c12')
            else:
                self.balance_label.config(bg='#e74c3c')  # Red for low balance
                balance_container = self.balance_label.master
                balance_container.config(bg='#e74c3c')
                balance_container.children['!label'].config(bg='#e74c3c')
                
        else:
            # No account logged in
            self.header_label.config(text="💳 ACCOUNT DASHBOARD")
            self.name_label.config(text="Guest User")
            self.balance_label.config(text="$0.00", bg='#95a5a6')
            self.email_label.config(text="Please log in to view details")
            self.type_label.config(text="🔒 No Account Selected")
            self.status_indicator.config(text="🔴 Not Logged In", fg='#e74c3c')
            
            # Reset balance container color
            balance_container = self.balance_label.master
            balance_container.config(bg='#95a5a6')
            balance_container.children['!label'].config(bg='#95a5a6')
            
            # Update stats
            self.stats_label.config(text=f"📊 Total Accounts in System: {BankSystem.number_of_accounts}\n🔐 Please log in to access your account")
    
    def create_savings_account(self):
        dialog = AccountCreationDialog(self.root, "Create Savings Account")
        if dialog.result:
            try:
                data = dialog.result
                interest_rate = simpledialog.askfloat("Interest Rate", 
                                                    "Enter interest rate (e.g., 0.05 for 5%):", 
                                                    minvalue=0.01, maxvalue=1.0)
                if interest_rate:
                    account = SavingAccount(data['name'], data['balance'], 
                                          data['email'], data['password'], interest_rate)
                    messagebox.showinfo("Success", f"Savings account created for {data['name']}!")
                    self.update_info_display()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def create_checking_account(self):
        dialog = AccountCreationDialog(self.root, "Create Checking Account")
        if dialog.result:
            try:
                data = dialog.result
                fee = simpledialog.askfloat("Transaction Fee", 
                                          "Enter transaction fee:", 
                                          minvalue=0, maxvalue=100)
                if fee is not None:
                    account = CheckingAccount(data['name'], data['balance'], 
                                            data['email'], data['password'], fee)
                    messagebox.showinfo("Success", f"Checking account created for {data['name']}!")
                    self.update_info_display()
            except ValueError as e:
                messagebox.showerror("Error", str(e))
    
    def login_account(self):
        email = simpledialog.askstring("Login", "Enter your email:")
        if email:
            account = BankSystem.find_account_by_email(email)
            if account:
                password = simpledialog.askstring("Login", "Enter your password:", show='*')
                if password and account.authenticate(password):
                    self.current_account = account
                    messagebox.showinfo("Success", f"Welcome, {account.get_name()}!")
                    self.update_info_display()
                else:
                    messagebox.showerror("Error", "Invalid password!")
            else:
                messagebox.showerror("Error", "Account not found!")
    
    def logout_account(self):
        if self.current_account:
            name = self.current_account.get_name()
            self.current_account = None
            messagebox.showinfo("Logout", f"Goodbye, {name}!")
            self.update_info_display()
        else:
            messagebox.showwarning("Warning", "No account is currently logged in!")
    
    def deposit_money(self):
        if not self.current_account:
            messagebox.showwarning("Warning", "Please login first!")
            return
        
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:", minvalue=0.01)
        if amount:
            if self.current_account.deposit(amount):
                messagebox.showinfo("Success", f"${amount:.2f} deposited successfully!")
                self.update_info_display()
            else:
                messagebox.showerror("Error", "Invalid deposit amount!")
    
    def withdraw_money(self):
        if not self.current_account:
            messagebox.showwarning("Warning", "Please login first!")
            return
        
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:", minvalue=0.01)
        if amount:
            if self.current_account.withdraw(amount):
                if isinstance(self.current_account, CheckingAccount):
                    messagebox.showinfo("Success", 
                                      f"${amount:.2f} withdrawn (+ ${self.current_account.transaction_fee} fee)!")
                else:
                    messagebox.showinfo("Success", f"${amount:.2f} withdrawn successfully!")
                self.update_info_display()
            else:
                messagebox.showerror("Error", "Insufficient funds or invalid amount!")
    
    def transfer_money(self):
        if not self.current_account:
            messagebox.showwarning("Warning", "Please login first!")
            return
        
        recipient_email = simpledialog.askstring("Transfer", "Enter recipient's email:")
        if not recipient_email:
            return
        
        recipient = BankSystem.find_account_by_email(recipient_email)
        if not recipient:
            messagebox.showerror("Error", "Recipient account not found!")
            return
        
        amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:", minvalue=0.01)
        if not amount:
            return
        
        password = simpledialog.askstring("Transfer", "Enter your password for confirmation:", show='*')
        if password:
            result = self.current_account.transfer(recipient, amount, password)
            if "transferred" in result.lower():
                messagebox.showinfo("Success", result)
                self.update_info_display()
            else:
                messagebox.showerror("Error", result)
    
    def add_interest(self):
        if not self.current_account:
            messagebox.showwarning("Warning", "Please login first!")
            return
        
        if isinstance(self.current_account, SavingAccount):
            interest = self.current_account.add_interest()
            messagebox.showinfo("Success", f"Interest of ${interest:.2f} added to your account!")
            self.update_info_display()
        else:
            messagebox.showwarning("Warning", "Interest can only be added to savings accounts!")
    
    def view_all_accounts(self):
        if not BankSystem.accounts:
            messagebox.showinfo("Info", "No accounts exist!")
            return
        
        # Create beautiful accounts window
        accounts_window = tk.Toplevel(self.root)
        accounts_window.title("🏦 All Bank Accounts")
        accounts_window.geometry("800x600")
        accounts_window.configure(bg='#f8f9fa')
        accounts_window.transient(self.root)
        
        # Center the window
        accounts_window.geometry("+%d+%d" % (
            self.root.winfo_rootx() + 50, 
            self.root.winfo_rooty() + 50
        ))
        
        # Header section
        header_frame = tk.Frame(accounts_window, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg='#2c3e50')
        header_content.pack(expand=True, fill=tk.BOTH)
        
        title_label = tk.Label(header_content, text="🏦 BANK ACCOUNTS OVERVIEW", 
                              font=("Arial", 18, "bold"), fg='white', bg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Stats in header
        total_balance = sum(acc.get_balance() for acc in BankSystem.accounts)
        stats_label = tk.Label(header_content, 
                              text=f"📊 {len(BankSystem.accounts)} Accounts\n💰 Total: ${total_balance:,.2f}", 
                              font=("Arial", 12, "bold"), fg='#ecf0f1', bg='#2c3e50', justify=tk.RIGHT)
        stats_label.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Main content frame with scrollbar
        main_frame = tk.Frame(accounts_window, bg='#f8f9fa')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar for custom scrolling
        canvas = tk.Canvas(main_frame, bg='#f8f9fa', highlightthickness=0)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f8f9fa')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create account cards
        self.create_account_cards(scrollable_frame)
        
        # Bind mousewheel to canvas
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Footer with close button
        footer_frame = tk.Frame(accounts_window, bg='#ecf0f1', height=60)
        footer_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        footer_frame.pack_propagate(False)
        
        close_btn = tk.Button(footer_frame, text="✖️ Close", command=accounts_window.destroy,
                             bg='#e74c3c', fg='white', font=("Arial", 12, "bold"),
                             padx=30, pady=10)
        close_btn.pack(side=tk.RIGHT, padx=20, pady=15)
        
        refresh_btn = tk.Button(footer_frame, text="🔄 Refresh", 
                               command=lambda: self.refresh_accounts_view(scrollable_frame),
                               bg='#3498db', fg='white', font=("Arial", 12, "bold"),
                               padx=30, pady=10)
        refresh_btn.pack(side=tk.RIGHT, padx=10, pady=15)
    
    def create_account_cards(self, parent_frame):
        # Clear existing cards
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        for i, account in enumerate(BankSystem.accounts):
            # Determine card colors based on account type
            if isinstance(account, SavingAccount):
                card_color = '#27ae60'  # Green for savings
                icon = '💰'
                type_text = f"Savings Account\nInterest Rate: {account.interest_rate*100}%"
            elif isinstance(account, CheckingAccount):
                card_color = '#3498db'  # Blue for checking
                icon = '💳'
                type_text = f"Checking Account\nTransaction Fee: ${account.transaction_fee}"
            else:
                card_color = '#95a5a6'  # Gray for basic
                icon = '🏛️'
                type_text = "Standard Account"
            
            # Main card frame
            card_frame = tk.Frame(parent_frame, bg='white', relief=tk.RAISED, bd=2)
            card_frame.pack(fill=tk.X, padx=10, pady=8)
            
            # Card header with colored strip
            header_strip = tk.Frame(card_frame, bg=card_color, height=5)
            header_strip.pack(fill=tk.X)
            
            # Card content
            content_frame = tk.Frame(card_frame, bg='white', pady=15, padx=20)
            content_frame.pack(fill=tk.X)
            
            # Top row: Icon, Name, and Balance
            top_row = tk.Frame(content_frame, bg='white')
            top_row.pack(fill=tk.X, pady=(0, 10))
            
            # Icon and name on left
            left_section = tk.Frame(top_row, bg='white')
            left_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            icon_label = tk.Label(left_section, text=icon, font=("Arial", 24), bg='white')
            icon_label.pack(side=tk.LEFT, padx=(0, 10))
            
            name_section = tk.Frame(left_section, bg='white')
            name_section.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            name_label = tk.Label(name_section, text=account.get_name(), 
                                 font=("Arial", 16, "bold"), bg='white', fg='#2c3e50')
            name_label.pack(anchor=tk.W)
            
            email_label = tk.Label(name_section, text=f"📧 {account.email}", 
                                  font=("Arial", 10), bg='white', fg='#7f8c8d')
            email_label.pack(anchor=tk.W)
            
            # Balance on right
            balance_section = tk.Frame(top_row, bg='white')
            balance_section.pack(side=tk.RIGHT)
            
            balance_label = tk.Label(balance_section, text=f"${account.get_balance():,.2f}", 
                                   font=("Arial", 18, "bold"), bg='white', fg=card_color)
            balance_label.pack()
            
            # Bottom section: Account type and status
            bottom_row = tk.Frame(content_frame, bg='white')
            bottom_row.pack(fill=tk.X, pady=(5, 0))
            
            # Account type info
            type_info_frame = tk.Frame(bottom_row, bg='#f8f9fa', relief=tk.GROOVE, bd=1)
            type_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
            
            type_label = tk.Label(type_info_frame, text=type_text, 
                                 font=("Arial", 9), bg='#f8f9fa', fg='#2c3e50', justify=tk.LEFT)
            type_label.pack(padx=10, pady=5)
            
            # Status indicator
            status_frame = tk.Frame(bottom_row, bg='white')
            status_frame.pack(side=tk.RIGHT)
            
            # Check if this is the currently logged-in account
            if self.current_account and self.current_account == account:
                status_text = "🟢 Active"
                status_color = '#27ae60'
            else:
                status_text = "⚫ Inactive"
                status_color = '#95a5a6'
            
            status_label = tk.Label(status_frame, text=status_text, 
                                   font=("Arial", 10, "bold"), bg='white', fg=status_color)
            status_label.pack()
            
            # Add hover effects
            def on_enter(e, frame=card_frame):
                frame.config(relief=tk.RAISED, bd=3)
            
            def on_leave(e, frame=card_frame):
                frame.config(relief=tk.RAISED, bd=2)
            
            card_frame.bind("<Enter>", on_enter)
            card_frame.bind("<Leave>", on_leave)
            
            # Make all child widgets also respond to hover
            for child in self.get_all_children(card_frame):
                child.bind("<Enter>", on_enter)
                child.bind("<Leave>", on_leave)
    
    def get_all_children(self, widget):
        """Recursively get all child widgets"""
        children = [widget]
        for child in widget.winfo_children():
            children.extend(self.get_all_children(child))
        return children
    
    def refresh_accounts_view(self, scrollable_frame):
        """Refresh the accounts view"""
        self.create_account_cards(scrollable_frame)

class AccountCreationDialog:
    def __init__(self, parent, title):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.configure(bg='#f0f0f0')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 150))
        
        self.create_widgets()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_widgets(self):
        main_frame = tk.Frame(self.dialog, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Name
        tk.Label(main_frame, text="Full Name:", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor=tk.W)
        self.name_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.name_entry.pack(pady=(0, 10), fill=tk.X)
        
        # Email
        tk.Label(main_frame, text="Email:", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor=tk.W)
        self.email_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.email_entry.pack(pady=(0, 10), fill=tk.X)
        
        # Password
        tk.Label(main_frame, text="Password:", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor=tk.W)
        self.password_entry = tk.Entry(main_frame, font=("Arial", 10), width=30, show='*')
        self.password_entry.pack(pady=(0, 10), fill=tk.X)
        
        # Initial Balance
        tk.Label(main_frame, text="Initial Balance:", font=("Arial", 10, "bold"), bg='#f0f0f0').pack(anchor=tk.W)
        self.balance_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.balance_entry.pack(pady=(0, 20), fill=tk.X)
        
        # Buttons
        button_frame = tk.Frame(main_frame, bg='#f0f0f0')
        button_frame.pack(fill=tk.X)
        
        tk.Button(button_frame, text="Create Account", command=self.create_account,
                 bg='#4CAF50', fg='white', font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Cancel", command=self.cancel,
                 bg='#F44336', fg='white', font=("Arial", 10, "bold")).pack(side=tk.LEFT)
        
        # Focus on first entry
        self.name_entry.focus()
    
    def create_account(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        try:
            balance = float(self.balance_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid balance!")
            return
        
        if not all([name, email, password]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return
        
        if balance <= 0:
            messagebox.showerror("Error", "Balance must be positive!")
            return
        
        # Check if email already exists
        if BankSystem.find_account_by_email(email):
            messagebox.showerror("Error", "An account with this email already exists!")
            return
        
        self.result = {
            'name': name,
            'email': email,
            'password': password,
            'balance': balance
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        self.dialog.destroy()

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = BankGUI(root)
    root.mainloop()