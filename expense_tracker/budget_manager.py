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


def track_budget(expenses: list, budget: float) -> None:
    total = 0.0
    for expense in expenses:
        try:
            total += float(expense["amount"])
        except (ValueError, TypeError, KeyError):
            continue

    print(f"\nTotal spent: ${total:.2f}")
    print(f"Monthly budget: ${budget:.2f}")
    if total > budget:
        print("You have exceeded your budget!")
    else:
        remaining = budget - total
        print(f"You have ${remaining:.2f} left for the month.")
