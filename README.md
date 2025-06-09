Budget Manager
A Python application for managing budgets with a Tkinter-based GUI, featuring a styled Treeview table for displaying budget summaries. The BudgetManager class allows users to allocate budgets, modify budget amounts, track expenditures, and view a financial summary in a visually appealing table with interactive entry fields. The code can be imported into other Python scripts for programmatic use or run as a standalone GUI application.
Features

Add Budgets: Allocate funds to specific budget categories.
Modify Budgets: Adjust the allocated amount for existing budgets.
Track Spending: Record expenditures for each budget category as a list of transactions.
View Summary: Display a formatted table of budgets, total spent, and remaining balances in a Treeview widget or console.
GUI Interface: User-friendly Tkinter interface with a styled table (light blue headers, pinkish selection) and dynamic updates.
Interactive Entry Fields: Placeholder text ("Budget Name", "Amount") clears when the user clicks the field and restores if left empty.

Prerequisites

Python 3.x
Tkinter (included with standard Python installations)

Installation

Ensure Python is installed on your system.
No additional packages are required, as tkinter and ttk are part of the Python standard library.
Save the code in a file named budget_manager.py (or budget.py if preferred).

Importing the Classes

Import BudgetManager: Use the BudgetManager class for programmatic budget management without the GUI. Save the code in budget_manager.py and import it:
import budget_manager

outgoings = budget_manager.BudgetManager(2500)  # Start with $2500
outgoings.add_budget("Groceries", 500)         # Allocate $500 to Groceries
outgoings.print_summary()                      # Print summary to console


If the file is named budget.py, use:import budget
outgoings = budget.BudgetManager(2500)


Ensure the file is in the same directory as your script, or adjust the import path (e.g., from my_package import budget_manager).


Import BudgetApp: Use the BudgetApp class to launch the GUI in another script.
import budget_manager
import tkinter as tk

root = tk.Tk()
app = budget_manager.BudgetApp(root)
root.mainloop()


Troubleshooting Imports:

If you get ModuleNotFoundError, verify the file name and location.
Use an alias if needed:import budget_manager as budget
outgoings = budget.BudgetManager(2500)


Add the directory to your Python path if the file is elsewhere:import sys
sys.path.append('/path/to/directory')
import budget_manager





Usage

Run the GUI:

Execute the script to launch the GUI:
python budget_manager.py


Use the GUI to:

Click the "Budget Name" field to clear the placeholder and enter a budget name.
Click the "Amount" field to clear the placeholder and enter an amount.
Click "Add Budget" to create a new budget, "Change Budget" to modify an existing budget, or "Record Spend" to log spending.
Click "Show Summary" to refresh the table with the latest budget data.
Placeholder text reappears if the fields are left empty.




Programmatic Usage:
import budget_manager

outgoings = budget_manager.BudgetManager(2500)  # Start with $2500
outgoings.add_budget("Groceries", 500)         # Allocate $500 to Groceries
outgoings.add_budget("Rent", 1000)             # Allocate $1000 to Rent
outgoings.change_budget("Groceries", 600)      # Change Groceries budget to $600
outgoings.spend("Groceries", 50)               # Spend $50 on Groceries
outgoings.spend("Groceries", 25)               # Spend another $25 on Groceries
outgoings.print_summary()                      # Display budget summary



Code Structure

BudgetManager Class:

__init__(amount): Initializes with a starting amount and empty budgets/expenditures.
add_budget(name, amount): Allocates funds to a budget category if sufficient funds are available.
change_budget(name, new_amount): Modifies the allocated amount for an existing budget.
spend(name, amount): Records spending as a list of transactions and returns the remaining budget.
get_summary(): Returns a list of tuples containing budget details for display in the GUI.
print_summary(): Prints a formatted table to the console.


BudgetApp Class (GUI):

Creates a Tkinter-based interface with entry fields, buttons, and a styled Treeview table.
Entry fields clear placeholder text ("Budget Name", "Amount") on click and restore it if left empty.
Displays available funds, error/success messages, and a table with columns for Budget Name, Budgeted, Spent, and Remaining.
Table features light blue headers and pinkish row selection for visual appeal.



Example Output
Running the example commands:
import budget_manager

outgoings = budget_manager.BudgetManager(2500)
outgoings.add_budget("Groceries", 500)
outgoings.print_summary()

Console Output:
Budget            Budgeted      Spent  Remaining
--------------- ---------- ---------- ----------
groceries         500.00      0.00    500.00
--------------- ---------- ---------- ----------
Total             500.00      0.00    500.00

GUI Output (if using BudgetApp):

A Treeview table displays the same data with columns for "Budget Name", "Budgeted", "Spent", and "Remaining".
The table updates dynamically after adding, modifying, or spending from budgets.
Placeholder text in entry fields clears on click and restores if the user leaves the field empty.
Table appearance:
Headers: Light blue background with black text.
Selected rows: Pinkish background.
Columns are centered with appropriate widths.



Limitations

Budget names are case-insensitive and stored in lowercase.
No support for negative amounts or overspending beyond budgeted amounts.
Expenditure is tracked as a list of transactions, but individual transactions are not displayed in the GUI.
The GUI is basic and could be enhanced with features like budget deletion, transaction history, or data persistence.

Contributing
Contributions are welcome! Please submit a pull request or open an issue for bugs, improvements, or feature requests.
License
This project is licensed under the MIT License.
