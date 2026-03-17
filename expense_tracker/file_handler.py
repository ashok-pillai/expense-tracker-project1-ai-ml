import csv
import os


def save_to_csv(expenses: list, filepath="data/expenses.csv") -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
        writer.writeheader()
        writer.writerows(expenses)
    print(f"Expenses saved to {filepath}.")


def load_from_csv(filepath="data/expenses.csv") -> list:
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        expenses = []
        for row in reader:
            try:
                row["amount"] = float(row["amount"])
            except (ValueError, KeyError):
                continue
            expenses.append(row)
    return expenses
