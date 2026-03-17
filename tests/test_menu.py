import unittest
from unittest.mock import patch, call
from io import StringIO

from expense_tracker.menu import display_menu, run


class TestDisplayMenu(unittest.TestCase):

    def test_prints_all_five_options(self):
        with patch("sys.stdout", new_callable=StringIO) as mock_out:
            display_menu()
            output = mock_out.getvalue()
        for option in ["1. Add Expense", "2. View Expenses", "3. Set/Track Budget",
                       "4. Save Expenses", "5. Save and Exit"]:
            self.assertIn(option, output)


class TestRunMenuRouting(unittest.TestCase):
    """Test that each menu option calls the correct function."""

    def _run_with_choices(self, choices):
        """Helper: runs the menu with given choice sequence, exits on '5'."""
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("builtins.input", side_effect=choices), \
             patch("sys.stdout", new_callable=StringIO):
            run()

    def test_option_1_calls_add_expense(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("expense_tracker.menu.add_expense") as mock_add, \
             patch("builtins.input", side_effect=["1", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        mock_add.assert_called_once()

    def test_option_2_calls_view_expenses(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("expense_tracker.menu.view_expenses") as mock_view, \
             patch("builtins.input", side_effect=["2", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        mock_view.assert_called_once()

    def test_option_3_calls_set_budget_and_track_budget(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("expense_tracker.menu.set_budget", return_value=500.0) as mock_set, \
             patch("expense_tracker.menu.track_budget") as mock_track, \
             patch("builtins.input", side_effect=["3", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        mock_set.assert_called_once()
        mock_track.assert_called_once_with([], 500.0)

    def test_option_3_passes_updated_budget_to_track(self):
        """Budget returned by set_budget must be forwarded to track_budget."""
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("expense_tracker.menu.set_budget", return_value=1200.0), \
             patch("expense_tracker.menu.track_budget") as mock_track, \
             patch("builtins.input", side_effect=["3", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        mock_track.assert_called_once_with([], 1200.0)

    def test_option_4_calls_save_to_csv(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv") as mock_save, \
             patch("builtins.input", side_effect=["4", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        # called once for option 4, once for option 5
        self.assertEqual(mock_save.call_count, 2)

    def test_option_5_saves_and_exits(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv") as mock_save, \
             patch("builtins.input", return_value="5"), \
             patch("sys.stdout", new_callable=StringIO) as mock_out:
            run()
        mock_save.assert_called_once()
        self.assertIn("Goodbye", mock_out.getvalue())

    def test_invalid_option_prints_error_and_continues(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("builtins.input", side_effect=["9", "abc", "5"]), \
             patch("sys.stdout", new_callable=StringIO) as mock_out:
            run()
        output = mock_out.getvalue()
        self.assertIn("Invalid option", output)


class TestRunStartup(unittest.TestCase):

    def test_loads_expenses_from_csv_on_startup(self):
        existing = [{"date": "2024-01-01", "category": "Food", "amount": 10.0, "description": "A"}]
        with patch("expense_tracker.menu.load_from_csv", return_value=existing) as mock_load, \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("builtins.input", return_value="5"), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        mock_load.assert_called_once()

    def test_prints_loaded_count_when_expenses_exist(self):
        existing = [
            {"date": "2024-01-01", "category": "Food", "amount": 10.0, "description": "A"},
            {"date": "2024-01-02", "category": "Travel", "amount": 20.0, "description": "B"},
        ]
        with patch("expense_tracker.menu.load_from_csv", return_value=existing), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("builtins.input", return_value="5"), \
             patch("sys.stdout", new_callable=StringIO) as mock_out:
            run()
        self.assertIn("Loaded 2 expense(s)", mock_out.getvalue())

    def test_no_loaded_message_when_no_expenses(self):
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("builtins.input", return_value="5"), \
             patch("sys.stdout", new_callable=StringIO) as mock_out:
            run()
        self.assertNotIn("Loaded", mock_out.getvalue())

    def test_budget_starts_at_zero_before_option_3(self):
        """track_budget should receive 0.0 if option 3 is never called before."""
        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("expense_tracker.menu.set_budget", return_value=0.0), \
             patch("expense_tracker.menu.track_budget") as mock_track, \
             patch("builtins.input", side_effect=["3", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        args = mock_track.call_args[0]
        self.assertEqual(args[1], 0.0)

    def test_expenses_list_passed_to_add_and_view(self):
        """add_expense and view_expenses should receive the same list object."""
        captured = {}
        def fake_add(expenses):
            captured["add"] = expenses
        def fake_view(expenses):
            captured["view"] = expenses

        with patch("expense_tracker.menu.load_from_csv", return_value=[]), \
             patch("expense_tracker.menu.save_to_csv"), \
             patch("expense_tracker.menu.add_expense", side_effect=fake_add), \
             patch("expense_tracker.menu.view_expenses", side_effect=fake_view), \
             patch("builtins.input", side_effect=["1", "2", "5"]), \
             patch("sys.stdout", new_callable=StringIO):
            run()
        self.assertIs(captured["add"], captured["view"])


if __name__ == "__main__":
    unittest.main()
