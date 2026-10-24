import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_file = Path(self.temp_dir.name) / "test_expenses.db"
        self.db_patcher = patch.object(main, "DB_PATH", self.db_file)
        self.db_patcher.start()
        main.connect_db().close()

    def tearDown(self):
        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def test_add_and_read_expense(self):
        expense_id = main.add_expense("2026-10-24", "Food", 120, "Lunch")
        self.assertGreater(expense_id, 0)
        expenses = main.get_expenses()
        self.assertEqual(len(expenses), 1)
        self.assertEqual(expenses[0]["category"], "Food")
        self.assertEqual(expenses[0]["amount"], 120.0)

    def test_total(self):
        main.add_expense("2026-10-24", "Food", 100)
        main.add_expense("2026-10-24", "Travel", 50)
        self.assertEqual(main.get_total(), 150.0)

    def test_reject_non_positive_amount(self):
        with self.assertRaises(ValueError):
            main.add_expense("2026-10-24", "Food", 0)

    def test_reject_invalid_date(self):
        with self.assertRaises(ValueError):
            main.add_expense("24-10-2026", "Food", 50)

    def test_delete_expense(self):
        expense_id = main.add_expense("2026-10-24", "Food", 50)
        self.assertTrue(main.delete_expense(expense_id))
        self.assertFalse(main.delete_expense(expense_id))
        self.assertEqual(main.get_expenses(), [])


if __name__ == "__main__":
    unittest.main()
