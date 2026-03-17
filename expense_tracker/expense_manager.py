from datetime import datetime


def add_expense(expenses: list) -> None:
    while True:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

    while True:
        category = input("Enter category: ").strip()
        if category:
            break
        print("Category cannot be empty.")

    while True:
        amount_str = input("Enter amount: ").strip()
        try:
            amount = float(amount_str)
            if amount > 0:
                break
            print("Amount must be greater than 0.")
        except ValueError:
            print("Invalid amount. Please enter a number.")

    while True:
        description = input("Enter description: ").strip()
        if description:
            break
        print("Description cannot be empty.")

    expenses.append({
        "date": date_str,
        "category": category,
        "amount": amount,
        "description": description,
    })
    print("Expense added successfully.")


def view_expenses(expenses: list) -> None:
    if not expenses:
        print("No expenses recorded.")
        return

    print(f"\n{'Date':<12} {'Category':<15} {'Amount':>10}  {'Description'}")
    print("-" * 55)
    for expense in expenses:
        required_keys = {"date", "category", "amount", "description"}
        if not required_keys.issubset(expense.keys()):
            print("(Skipping entry with missing fields)")
            continue
        try:
            amount = float(expense["amount"])
        except (ValueError, TypeError):
            print("(Skipping entry with invalid amount)")
            continue
        print(f"{expense['date']:<12} {expense['category']:<15} ${amount:>9.2f}  {expense['description']}")
    print()
