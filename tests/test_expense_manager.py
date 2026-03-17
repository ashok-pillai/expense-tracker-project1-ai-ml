import unittest
from unittest.mock import patch
from io import StringIO

from expense_tracker.expense_manager import add_expense, view_expenses


class TestAddExpense(unittest.TestCase):

    def _add(self, inputs):
        with patch("builtins.input", side_effect=inputs):
            expenses = []
            add_expense(expenses)
            return expenses

    def test_adds_valid_expense(self):
        expenses = self._add(["2024-06-01", "Food", "15.50", "Lunch"])
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["date"], "2024-06-01")
        self.assertEqual(expenses[0]["category"], "Food")
        self.assertAlmostEqual(expenses[0]["amount"], 15.50)
        self.assertEqual(expenses[0]["description"], "Lunch")

    def test_retries_on_invalid_date_format(self):
        expenses = self._add(["06-01-2024", "not-a-date", "2024-06-01", "Food", "10.0", "Test"])
        self.assertEqual(expenses[0]["date"], "2024-06-01")

    def test_retries_on_zero_amount(self):
        expenses = self._add(["2024-06-01", "Food", "0", "-5", "10.0", "Dinner"])
        self.assertAlmostEqual(expenses[0]["amount"], 10.0)

    def test_retries_on_non_numeric_amount(self):
        expenses = self._add(["2024-06-01", "Food", "abc", "12.0", "Snack"])
        self.assertAlmostEqual(expenses[0]["amount"], 12.0)

    def test_retries_on_empty_category(self):
        expenses = self._add(["2024-06-01", "", "  ", "Food", "5.0", "Coffee"])
        self.assertEqual(expenses[0]["category"], "Food")

    def test_retries_on_empty_description(self):
        expenses = self._add(["2024-06-01", "Food", "5.0", "", "  ", "Coffee"])
        self.assertEqual(expenses[0]["description"], "Coffee")

    def test_appends_to_existing_list(self):
        existing = [{"date": "2024-01-01", "category": "Rent", "amount": 800.0, "description": "Jan rent"}]
        with patch("builtins.input", side_effect=["2024-06-01", "Food", "10.0", "Lunch"]):
            add_expense(existing)
        self.assertEqual(len(existing), 2)


class TestViewExpenses(unittest.TestCase):

    def _capture(self, expenses):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            view_expenses(expenses)
            return mock_out.getvalue()

    def test_empty_list_prints_notice(self):
        output = self._capture([])
        self.assertIn("No expenses recorded", output)

    def test_displays_all_fields(self):
        expenses = [{"date": "2024-06-01", "category": "Food", "amount": 15.50, "description": "Lunch"}]
        output = self._capture(expenses)
        self.assertIn("2024-06-01", output)
        self.assertIn("Food", output)
        self.assertIn("15.50", output)
        self.assertIn("Lunch", output)

    def test_skips_entry_with_missing_key(self):
        expenses = [{"date": "2024-06-01", "category": "Food", "amount": 10.0}]  # missing description
        output = self._capture(expenses)
        self.assertIn("missing fields", output)

    def test_skips_entry_with_invalid_amount(self):
        expenses = [{"date": "2024-06-01", "category": "Food", "amount": "bad", "description": "x"}]
        output = self._capture(expenses)
        self.assertIn("invalid amount", output)

    def test_displays_multiple_expenses(self):
        expenses = [
            {"date": "2024-06-01", "category": "Food", "amount": 10.0, "description": "A"},
            {"date": "2024-06-02", "category": "Travel", "amount": 30.0, "description": "B"},
        ]
        output = self._capture(expenses)
        self.assertIn("Food", output)
        self.assertIn("Travel", output)


if __name__ == "__main__":
    unittest.main()
