Here's a simplified and clearer version of the Budget Manager documentation:

---

# Budget Manager

A Python application for managing budgets with a user-friendly Tkinter GUI, featuring a styled table to display budget summaries. The `BudgetManager` class allows programmatic budget management, while `BudgetApp` provides a graphical interface. You can import the code for scripting or run it as a standalone GUI app.

## Features
- **Add Budgets**: Allocate funds to specific categories (e.g., Groceries, Rent).
- **Modify Budgets**: Update the allocated amount for existing budgets.
- **Track Spending**: Record expenses for each budget category as a list of transactions.
- **View Summary**: Show a formatted table of budgets, amounts spent, and remaining balances.
- **GUI Interface**: Tkinter-based interface with a styled table (light blue headers, pinkish selection) and interactive entry fields.
- **Interactive Fields**: Entry fields with placeholder text ("Budget Name", "Amount") that clears on click and restores if left empty.

## Prerequisites
- Python 3.x
- Tkinter (included with Python)

## Installation
1. Ensure Python 3.x is installed.
2. Save the code in a file named `budget_manager.py`.
3. No additional packages are needed (Tkinter is built-in).

## Using the Code

### Option 1: Programmatic Use
Use the `BudgetManager` class in your Python scripts for budget management without the GUI.

1. Save the code as `budget_manager.py`.
2. Import and use it in your script:

```python
import budget_manager

# Create a budget with $2500 starting amount
outgoings = budget_manager.BudgetManager(2500)

# Add budgets
outgoings.add_budget("Groceries", 500)
outgoings.add_budget("Rent", 1000)

# Modify a budget
outgoings.change_budget("Groceries", 600)

# Record spending
outgoings.spend("Groceries", 50)
outgoings.spend("Groceries", 25)

# Print summary to console
outgoings.print_summary()
```

**Example Console Output**:
```
Budget            Budgeted      Spent  Remaining
--------------- ---------- ---------- ----------
groceries         600.00      75.00    525.00
rent             1000.00       0.00   1000.00
--------------- ---------- ---------- ----------
Total            1600.00      75.00   1525.00
```

### Option 2: Run the GUI
Run the script to launch the GUI:
```bash
python budget_manager.py
```

**Using the GUI**:
- Enter a budget name in the "Budget Name" field (placeholder clears on click).
- Enter an amount in the "Amount" field (placeholder clears on click).
- Click buttons to:
  - **Add Budget**: Create a new budget.
  - **Change Budget**: Update an existing budget.
  - **Record Spend**: Log spending for a budget.
  - **Show Summary**: Refresh the table with budget details.
- Placeholder text reappears if fields are left empty.
- The table shows Budget Name, Budgeted, Spent, and Remaining with:
  - Light blue headers.
  - Pinkish background for selected rows.

### Option 3: Use the GUI in Another Script
Launch the GUI programmatically:

```python
import budget_manager
import tkinter as tk

root = tk.Tk()
app = budget_manager.BudgetApp(root)
root.mainloop()
```

### Troubleshooting Imports
- **ModuleNotFoundError**: Ensure `budget_manager.py` is in the same directory as your script or add its path:
  ```python
  import sys
  sys.path.append('/path/to/directory')
  import budget_manager
  ```
- Use an alias if preferred:
  ```python
  import budget_manager as bm
  outgoings = bm.BudgetManager(2500)
  ```

## Code Structure

### `BudgetManager` Class
- `__init__(amount)`: Starts with a total amount and empty budgets.
- `add_budget(name, amount)`: Allocates funds to a category if enough funds are available.
- `change_budget(name, new_amount)`: Updates an existing budget’s amount.
- `spend(name, amount)`: Records spending as transactions and returns remaining budget.
- `get_summary()`: Returns budget details for display.
- `print_summary()`: Prints a formatted table to the console.

### `BudgetApp` Class (GUI)
- Creates a Tkinter interface with:
  - Entry fields with placeholder text.
  - Buttons for adding, modifying, spending, and showing summaries.
  - A styled Treeview table showing budget details.
- Table features:
  - Light blue headers, pinkish row selection.
  - Centered columns with appropriate widths.
  - Updates dynamically with budget changes.

## Limitations
- Budget names are case-insensitive (stored in lowercase).
- No support for negative amounts or overspending.
- Individual transactions are tracked but not shown in the GUI.
- Basic GUI; could be improved with features like budget deletion or transaction history.

## Contributing
Submit pull requests or open issues for bugs, improvements, or feature requests.

## License
MIT License

---

This version is more concise, organized, and easier to read while retaining all essential information. Let me know if you need further refinements or specific sections expanded!
