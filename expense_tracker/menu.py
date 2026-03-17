from expense_tracker.file_handler import load_from_csv, save_to_csv
from expense_tracker.expense_manager import add_expense, view_expenses
from expense_tracker.budget_manager import set_budget, track_budget


def display_menu() -> None:
    print("\n===== Personal Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Set Budget")
    print("4. Track Budget")
    print("5. Save Expenses")
    print("6. Save and Exit")
    print("=====================================")


def run() -> None:
    expenses = load_from_csv()
    budget = 0.0

    if expenses:
        print(f"Loaded {len(expenses)} expense(s) from file.")

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            add_expense(expenses)
        elif choice == "2":
            view_expenses(expenses)
        elif choice == "3":
            budget = set_budget()
            print(f"Budget set to ${budget:.2f}")
        elif choice == "4":
            track_budget(expenses, budget)
        elif choice == "5":
            save_to_csv(expenses)
        elif choice == "6":
            save_to_csv(expenses)
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 6.")
