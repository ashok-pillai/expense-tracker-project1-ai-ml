import unittest
from unittest.mock import patch
from io import StringIO

from expense_tracker.budget_manager import set_budget, track_budget


class TestSetBudget(unittest.TestCase):

    def test_returns_valid_budget(self):
        with patch("builtins.input", return_value="500"):
            result = set_budget()
        self.assertAlmostEqual(result, 500.0)

    def test_returns_float(self):
        with patch("builtins.input", return_value="1200.75"):
            result = set_budget()
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 1200.75)

    def test_retries_on_zero(self):
        with patch("builtins.input", side_effect=["0", "200"]):
            result = set_budget()
        self.assertAlmostEqual(result, 200.0)

    def test_retries_on_negative(self):
        with patch("builtins.input", side_effect=["-100", "300"]):
            result = set_budget()
        self.assertAlmostEqual(result, 300.0)

    def test_retries_on_non_numeric(self):
        with patch("builtins.input", side_effect=["abc", "400"]):
            result = set_budget()
        self.assertAlmostEqual(result, 400.0)


class TestTrackBudget(unittest.TestCase):

    def _capture(self, expenses, budget):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            track_budget(expenses, budget)
            return mock_out.getvalue()

    def test_exceeded_message(self):
        expenses = [
            {"amount": 200.0},
            {"amount": 150.0},
        ]
        output = self._capture(expenses, 300.0)
        self.assertIn("exceeded your budget", output)

    def test_remaining_balance_message(self):
        expenses = [{"amount": 100.0}]
        output = self._capture(expenses, 500.0)
        self.assertIn("400.00", output)
        self.assertIn("left for the month", output)

    def test_exact_budget_shows_zero_remaining(self):
        expenses = [{"amount": 500.0}]
        output = self._capture(expenses, 500.0)
        self.assertIn("0.00", output)
        self.assertIn("left for the month", output)

    def test_empty_expenses_shows_full_budget_remaining(self):
        output = self._capture([], 300.0)
        self.assertIn("300.00", output)
        self.assertIn("left for the month", output)

    def test_skips_invalid_amounts(self):
        expenses = [
            {"amount": "bad"},
            {"amount": 50.0},
        ]
        output = self._capture(expenses, 100.0)
        self.assertIn("50.00", output)
        self.assertIn("left for the month", output)

    def test_displays_total_spent(self):
        expenses = [{"amount": 75.0}, {"amount": 25.0}]
        output = self._capture(expenses, 200.0)
        self.assertIn("100.00", output)


if __name__ == "__main__":
    unittest.main()
