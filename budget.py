import tkinter as tk
from tkinter import ttk
import json

class BudgetManager:
    """Manages budget data including available funds, budgets, and expenditures."""
    def __init__(self, amount):
        """Initialize BudgetManager with starting funds."""
        self.available = amount
        self.budgets = {}
        self.expenditure = {}

    def add_budget(self, name, amount):
        """Add a new budget with the given name and amount."""
        name = name.lower()
        if name in self.budgets:
            raise ValueError("Budget exists")
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if amount > self.available:
            raise ValueError("Insufficient funds")
        self.budgets[name] = amount
        self.available -= amount
        self.expenditure[name] = []
        return self.available

    def change_budget(self, name, new_amount):
        """Change the amount of an existing budget."""
        name = name.lower()
        if name not in self.budgets:
            raise ValueError("Budget does not exist")
        if new_amount < 0:
            raise ValueError("Amount cannot be negative")
        old_amount = self.budgets[name]
        if new_amount > old_amount + self.available:
            raise ValueError("Insufficient funds")
        self.budgets[name] = new_amount
        self.available -= new_amount - old_amount
        return self.available

    def spend(self, name, amount):
        """Record spending for a budget and return remaining amount."""
        name = name.lower()
        if name not in self.expenditure:
            raise ValueError("No such budget")
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        self.expenditure[name].append(amount)
        budgeted = self.budgets[name]
        spent = sum(self.expenditure[name])
        return budgeted - spent

    def get_summary(self):
        """Return a summary of all budgets as a list of tuples."""
        summary = []
        total_budgeted = 0
        total_spent = 0
        total_remaining = 0
        for name in self.budgets:
            budgeted = self.budgets[name]
            spent = sum(self.expenditure[name])
            remaining = budgeted - spent
            summary.append((name, budgeted, spent, remaining))
            total_budgeted += budgeted
            total_spent += spent
            total_remaining += remaining
        summary.append(("Total", total_budgeted, total_spent, total_remaining))
        return summary

    def print_summary(self):
        """Print a formatted summary of all budgets to the console."""
        print("Budget            Budgeted      Spent  Remaining")
        print("--------------- ---------- ---------- ----------")
        total_budgeted = 0
        total_spent = 0
        total_remaining = 0
        for name in self.budgets:
            budgeted = self.budgets[name]
            spent = sum(self.expenditure[name])
            remaining = budgeted - spent
            print(f'{name:15s} {budgeted:10.2f}{spent:10.2f} '
                  f'{remaining:10.2f}')
            total_budgeted += budgeted
            total_spent += spent
            total_remaining += remaining
        print("--------------- ---------- ---------- ----------")
        print(f'{"Total":15s} {total_budgeted:10.2f}{total_spent:10.2f} '
              f'{total_remaining:10.2f}')

class BudgetApp:
    """GUI application for managing budgets using tkinter."""
    def __init__(self, root):
        """Initialize the BudgetApp GUI with a BudgetManager instance."""
        self.manager = BudgetManager(1000)
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("800x600")  # Window size
        self.root.resizable(False, False)  # Make window non-resizable

        # Create a style for Treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", background="#ADD8E6", foreground="black")  # Light blue header
        style.configure("Treeview", background="white", foreground="black")
        style.map("Treeview", background=[("selected", "#FFB6C1")])  # Pinkish for selected rows

        # GUI elements
        self.label_amount = ttk.Label(root, text=f"Available Funds: ${self.manager.available:.2f}")
        self.label_amount.pack(pady=10)

        self.entry_budget = ttk.Entry(root)
        self.entry_budget.pack()
        self.entry_budget.insert(0, "Budget Name")
        self.entry_budget.bind("<FocusIn>", lambda event: self.clear_placeholder(self.entry_budget, "Budget Name"))
        self.entry_budget.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry_budget, "Budget Name"))

        self.entry_amount = ttk.Entry(root)
        self.entry_amount.pack()
        self.entry_amount.insert(0, "Amount")
        self.entry_amount.bind("<FocusIn>", lambda event: self.clear_placeholder(self.entry_amount, "Amount"))
        self.entry_amount.bind("<FocusOut>", lambda event: self.restore_placeholder(self.entry_amount, "Amount"))

        self.btn_add = ttk.Button(root, text="Add Budget", command=self.add_budget)
        self.btn_add.pack(pady=5)

        self.btn_change = ttk.Button(root, text="Change Budget", command=self.change_budget)
        self.btn_change.pack(pady=5)

        self.btn_spend = ttk.Button(root, text="Record Spend", command=self.spend)
        self.btn_spend.pack(pady=5)

        self.btn_summary = ttk.Button(root, text="Show Summary", command=self.show_summary)
        self.btn_summary.pack(pady=5)

        self.btn_clear = ttk.Button(root, text="Clear All", command=self.clear_all)
        self.btn_clear.pack(pady=5)

        # Create Treeview widget
        self.tree = ttk.Treeview(
            root,
            columns=("Budget Name", "Budgeted", "Spent", "Remaining"),
            show="headings",
            style="Treeview"
        )
        self.tree.heading("Budget Name", text="Budget Name")
        self.tree.heading("Budgeted", text="Budgeted")
        self.tree.heading("Spent", text="Spent")
        self.tree.heading("Remaining", text="Remaining")
        self.tree.column("Budget Name", width=200, anchor="center")  # Adjusted for window
        self.tree.column("Budgeted", width=150, anchor="center")    # Adjusted for window
        self.tree.column("Spent", width=150, anchor="center")       # Adjusted for window
        self.tree.column("Remaining", width=150, anchor="center")   # Adjusted for window
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Error/success label
        self.error_label = ttk.Label(root, text="", wraplength=780)  # Adjusted for window
        self.error_label.pack(pady=5)

        # Load data from file
        self.load_data()

        # Initialize table with loaded data
        self.show_summary()

    def clear_placeholder(self, entry, placeholder):
        """Clear placeholder text in an entry field when focused."""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def restore_placeholder(self, entry, placeholder):
        """Restore placeholder text in an entry field if empty."""
        if not entry.get():
            entry.insert(0, placeholder)

    def show_message(self, message, color="red"):
        """Display a message in the error label and clear it after 3 seconds."""
        self.error_label.config(text=message, foreground=color)
        self.root.after(3000, lambda: self.error_label.config(text=""))

    def save_data(self):
        """Save budget data to budgets.json."""
        try:
            with open("budgets.json", "w") as f:
                json.dump({
                    "available": self.manager.available,
                    "budgets": self.manager.budgets,
                    "expenditure": self.manager.expenditure
                }, f, indent=2)
        except Exception as e:
            self.show_message(f"Error saving data: {e}")

    def load_data(self):
        """Load budget data from budgets.json if it exists."""
        try:
            with open("budgets.json", "r") as f:
                data = json.load(f)
                self.manager.available = float(data.get("available", 1000))
                self.manager.budgets = {k: float(v) for k, v in data.get("budgets", {}).items()}
                self.manager.expenditure = {k: [float(x) for x in v] for k, v in data.get("expenditure", {}).items()}
                self.label_amount.config(text=f"Available Funds: ${self.manager.available:.2f}")
        except FileNotFoundError:
            pass  # File doesn't exist, use default initialization
        except Exception as e:
            self.show_message(f"Error loading data: {e}")

    def clear_all(self):
        """Reset all budget data and save the cleared state."""
        self.manager.available = 1000
        self.manager.budgets = {}
        self.manager.expenditure = {}
        self.label_amount.config(text=f"Available Funds: ${self.manager.available:.2f}")
        self.save_data()
        self.show_message("All budgets cleared.", color="green")
        self.show_summary()

    def add_budget(self):
        """Add a new budget via the GUI and save data."""
        try:
            name = self.entry_budget.get().lower()
            if name == "budget name" or not name.strip():
                raise ValueError("Enter a valid budget name")
            amount = self.entry_amount.get()
            if amount == "Amount" or not amount.strip():
                raise ValueError("Enter a valid amount")
            amount = float(amount)
            remaining = self.manager.add_budget(name, amount)
            self.label_amount.config(text=f"Available Funds: ${remaining:.2f}")
            self.entry_budget.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.restore_placeholder(self.entry_budget, "Budget Name")
            self.restore_placeholder(self.entry_amount, "Amount")
            self.save_data()
            self.show_message(f"Budget '{name}' added.", color="green")
            self.show_summary()
        except ValueError as e:
            self.show_message(f"Error: {e}")

    def change_budget(self):
        """Change an existing budget's amount via the GUI and save data."""
        try:
            name = self.entry_budget.get().lower()
            if name == "budget name" or not name.strip():
                raise ValueError("Enter a valid budget name")
            amount = self.entry_amount.get()
            if amount == "Amount" or not amount.strip():
                raise ValueError("Enter a valid amount")
            amount = float(amount)
            remaining = self.manager.change_budget(name, amount)
            self.label_amount.config(text=f"Available Funds: ${remaining:.2f}")
            self.entry_budget.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.restore_placeholder(self.entry_budget, "Budget Name")
            self.restore_placeholder(self.entry_amount, "Amount")
            self.save_data()
            self.show_message(f"Budget '{name}' changed to ${amount:.2f}.", color="green")
            self.show_summary()
        except ValueError as e:
            self.show_message(f"Error: {e}")

    def spend(self):
        """Record spending for a budget via the GUI and save data."""
        try:
            name = self.entry_budget.get().lower()
            if name == "budget name" or not name.strip():
                raise ValueError("Enter a valid budget name")
            amount = self.entry_amount.get()
            if amount == "Amount" or not amount.strip():
                raise ValueError("Enter a valid amount")
            amount = float(amount)
            remaining = self.manager.spend(name, amount)
            self.entry_budget.delete(0, tk.END)
            self.entry_amount.delete(0, tk.END)
            self.restore_placeholder(self.entry_budget, "Budget Name")
            self.restore_placeholder(self.entry_amount, "Amount")
            self.save_data()
            self.show_message(f"Spent ${amount:.2f} on '{name}'.", color="green")
            self.show_summary()
        except ValueError as e:
            self.show_message(f"Error: {e}")

    def show_summary(self):
        """Update the Treeview with the current budget summary."""
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Insert new data
        for name, budgeted, spent, remaining in self.manager.get_summary():
            self.tree.insert("", "end", values=(
                name,
                f"${budgeted:.2f}",
                f"${spent:.2f}",
                f"${remaining:.2f}"
            ))

if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetApp(root)
    root.mainloop()
