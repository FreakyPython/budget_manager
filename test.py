import budget

import tkinter as tk

outgoings = budget.BudgetManager(2500)
outgoings.add_budget("Groceries", 500)
outgoings.print_summary()


root = tk.Tk()
app = budget.BudgetApp(root)
root.mainloop()
