import os
import csv
import tempfile
import unittest

from expense_tracker.file_handler import save_to_csv, load_from_csv


class TestSaveToCsv(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filepath = os.path.join(self.tmpdir, "sub", "expenses.csv")

    def test_creates_directory_if_missing(self):
        save_to_csv([], self.filepath)
        self.assertTrue(os.path.exists(self.filepath))

    def test_writes_header_and_rows(self):
        expenses = [
            {"date": "2024-01-01", "category": "Food", "amount": 10.0, "description": "Lunch"},
            {"date": "2024-01-02", "category": "Travel", "amount": 25.5, "description": "Bus"},
        ]
        save_to_csv(expenses, self.filepath)
        with open(self.filepath) as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["category"], "Food")
        self.assertEqual(rows[1]["amount"], "25.5")

    def test_saves_empty_list(self):
        save_to_csv([], self.filepath)
        with open(self.filepath) as f:
            content = f.read()
        self.assertIn("date,category,amount,description", content)

    def test_overwrites_existing_file(self):
        save_to_csv([{"date": "2024-01-01", "category": "Food", "amount": 5.0, "description": "A"}], self.filepath)
        save_to_csv([{"date": "2024-02-01", "category": "Rent", "amount": 800.0, "description": "B"}], self.filepath)
        rows = load_from_csv(self.filepath)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["category"], "Rent")


class TestLoadFromCsv(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filepath = os.path.join(self.tmpdir, "expenses.csv")

    def test_returns_empty_list_when_file_missing(self):
        result = load_from_csv("/nonexistent/path/expenses.csv")
        self.assertEqual(result, [])

    def test_loads_and_casts_amount_to_float(self):
        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
            writer.writeheader()
            writer.writerow({"date": "2024-03-01", "category": "Food", "amount": "12.75", "description": "Dinner"})
        rows = load_from_csv(self.filepath)
        self.assertEqual(len(rows), 1)
        self.assertIsInstance(rows[0]["amount"], float)
        self.assertAlmostEqual(rows[0]["amount"], 12.75)

    def test_skips_rows_with_invalid_amount(self):
        with open(self.filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
            writer.writeheader()
            writer.writerow({"date": "2024-03-01", "category": "Food", "amount": "bad", "description": "x"})
            writer.writerow({"date": "2024-03-02", "category": "Travel", "amount": "20.0", "description": "y"})
        rows = load_from_csv(self.filepath)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["category"], "Travel")

    def test_round_trip(self):
        original = [
            {"date": "2024-05-01", "category": "Food", "amount": 9.99, "description": "Coffee"},
            {"date": "2024-05-02", "category": "Rent", "amount": 1200.0, "description": "May rent"},
        ]
        save_to_csv(original, self.filepath)
        loaded = load_from_csv(self.filepath)
        self.assertEqual(len(loaded), 2)
        self.assertAlmostEqual(loaded[0]["amount"], 9.99)
        self.assertAlmostEqual(loaded[1]["amount"], 1200.0)


if __name__ == "__main__":
    unittest.main()
