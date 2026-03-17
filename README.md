# Personal Expense Tracker

A command-line based Personal Expense Tracker built in Python that allows users to log, view, and manage their daily expenses while tracking them against a monthly budget. All data is persisted locally in a CSV file and automatically reloaded on the next session. The project uses only Python's standard library — no third-party packages are required.

---

## Project Structure

```
personal-expense-tracker/
├── main.py
├── expense_tracker/
│   ├── __init__.py
│   ├── file_handler.py
│   ├── expense_manager.py
│   ├── budget_manager.py
│   └── menu.py
```

---

## Modules

### `main.py`
The entry point of the application. Imports and calls `menu.run()` to start the program.

### `expense_tracker/file_handler.py`
Handles all CSV read and write operations.
- `save_to_csv()` — writes the current list of expenses to `data/expenses.csv`, creating the `data/` directory automatically if it does not exist.
- `load_from_csv()` — reads expenses from the CSV file on startup, casting the `amount` field to a float. Returns an empty list if the file does not exist.

### `expense_tracker/expense_manager.py`
Manages adding and displaying expenses.
- `add_expense()` — prompts the user for date (`YYYY-MM-DD`), category, amount, and description.
- `view_expenses()` — prints all expenses in a formatted table. Skips and notifies the user of any entries with missing fields or invalid amounts.

### `expense_tracker/budget_manager.py`
Handles budget setting and tracking.
- `set_budget()` — prompts the user to enter a monthly budget and returns it.
- `calculate_total_expenses()` — sums all expense amounts for the current month and returns the total.
- `track_budget()` — aggregates expenses for the current month and compares the total against the set budget. Displays either an exceeded warning or the remaining balance.

### `expense_tracker/menu.py`
Drives the application loop.
- `display_menu()` — prints the six menu options.
- `run()` — loads expenses from CSV on startup, then enters a loop handling user selections:
  - Option 1: Add an expense
  - Option 2: View all expenses
  - Option 3: Set budget
  - Option 4: Track budget (current month vs budget)
  - Option 5: Save expenses to CSV
  - Option 6: Save and exit

---

## Data Storage
Expenses are stored in `data/expenses.csv` with four columns: `date`, `category`, `amount`, `description`. The file is created automatically on the first save and loaded back into memory each time the program starts.

---

## How to Run

```bash
python main.py
```
