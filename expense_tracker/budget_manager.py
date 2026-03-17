def set_budget() -> float:
    while True:
        budget_str = input("Enter your monthly budget: ").strip()
        try:
            budget = float(budget_str)
            if budget > 0:
                return budget
            print("Budget must be greater than 0.")
        except ValueError:
            print("Invalid amount. Please enter a number.")


def calculate_total_expenses(expenses: list, month: str) -> float:
    total = 0.0
    for expense in expenses:
        try:
            if not expense.get("date", "").startswith(month):
                continue
            total += float(expense["amount"])
        except (ValueError, TypeError, KeyError):
            continue
    return total


def track_budget(expenses: list, budget: float) -> None:
    from datetime import datetime
    if budget <= 0:
        print("No budget set. Please set a budget first (Option 3).")
        return

    current_month = datetime.now().strftime("%Y-%m")
    total = calculate_total_expenses(expenses, current_month)

    print(f"\nMonth: {current_month}")
    print(f"Total spent: ${total:.2f}")
    print(f"Monthly budget: ${budget:.2f}")
    if total > budget:
        print("You have exceeded your budget!")
    else:
        remaining = budget - total
        print(f"You have ${remaining:.2f} left for the month.")
