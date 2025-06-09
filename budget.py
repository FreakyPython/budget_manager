import tkinter as tk
from tkinter import ttk

class BudgetManager:
    def __init__(self, amount):
        self.available = amount
        self.budgets = {}
        self.expenditure = {}

    def add_budget(self, name, amount):
        name = name.lower()
        if name in self.budgets:
            raise ValueError("Budget exists")
        if amount > self.available:
            raise ValueError("Insufficient funds")
        self.budgets[name] = amount
        self.available -= amount
        self.expenditure[name] = []
        return self.available

    def change_budget(self, name, new_amount):
        name = name.lower()
        if name not in self.budgets:
            raise ValueError("Budget does not exist")
        old_amount = self.budgets[name]
        if new_amount > old_amount + self.available:
            raise ValueError("Insufficient funds")
        self.budgets[name] = new_amount
        self.available -= new_amount - old_amount
        return self.available

    def spend(self, name, amount):
        name = name.lower()
        if name not in self.expenditure:
            raise ValueError("No such budget")
        self.expenditure[name].append(amount)
        budgeted = self.budgets[name]
        spent = sum(self.expenditure[name])
        return budgeted - spent

    def get_summary(self):
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
    def __init__(self, root):
        self.manager = BudgetManager(1000)
        self.root = root
        self.root.title("Budget Manager")
        self.root.geometry("600x400")

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
        self.tree.column("Budget Name", width=150, anchor="center")
        self.tree.column("Budgeted", width=100, anchor="center")
        self.tree.column("Spent", width=100, anchor="center")
        self.tree.column("Remaining", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Error/success label
        self.error_label = ttk.Label(root, text="", foreground="red")
        self.error_label.pack(pady=5)

        # Initialize table with sample data
        self.show_summary()

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def restore_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)

    def add_budget(self):
        try:
            name = self.entry_budget.get().lower()
            if name == "budget name":
                raise ValueError("Enter a valid budget name")
            amount = self.entry_amount.get()
            if amount == "Amount":
                raise ValueError("Enter a valid amount")
            amount = float(amount)
            remaining = self.manager.add_budget(name, amount)
            self.label_amount.config(text=f"Available Funds: ${remaining:.2f}")
            self.error_label.config(text=f"Budget '{name}' added.")
            self.show_summary()
        except ValueError as e:
            self.error_label.config(text=f"Error: {e}")

    def change_budget(self):
        try:
            name = self.entry_budget.get().lower()
            if name == "budget name":
                raise ValueError("Enter a valid budget name")
            amount = self.entry_amount.get()
            if amount == "Amount":
                raise ValueError("Enter a valid amount")
            amount = float(amount)
            remaining = self.manager.change_budget(name, amount)
            self.label_amount.config(text=f"Available Funds: ${remaining:.2f}")
            self.error_label.config(text=f"Budget '{name}' changed to ${amount:.2f}.")
            self.show_summary()
        except ValueError as e:
            self.error_label.config(text=f"Error: {e}")

    def spend(self):
        try:
            name = self.entry_budget.get().lower()
            if name == "budget name":
                raise ValueError("Enter a valid budget name")
            amount = self.entry_amount.get()
            if amount == "Amount":
                raise ValueError("Enter a valid amount")
            amount = float(amount)
            remaining = self.manager.spend(name, amount)
            self.error_label.config(text=f"Spent ${amount:.2f} on '{name}'.")
            self.show_summary()
        except ValueError as e:
            self.error_label.config(text=f"Error: {e}")

    def show_summary(self):
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
