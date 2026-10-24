"""Personal Expense Tracker - a beginner-friendly Python CLI project."""
import sqlite3
from datetime import date, datetime
from pathlib import Path
import csv

DB_PATH = Path(__file__).with_name("expenses.db")


def connect_db():
    """Open a connection and ensure the expenses table exists."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expense_date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            note TEXT DEFAULT ''
        )
        """
    )
    connection.commit()
    return connection


def add_expense(expense_date, category, amount, note=""):
    """Validate and save one expense."""
    try:
        datetime.strptime(expense_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must use YYYY-MM-DD format.") from None

    category = category.strip()
    if not category:
        raise ValueError("Category cannot be empty.")
    try:
        amount = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number.") from None
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    with connect_db() as connection:
        cursor = connection.execute(
            "INSERT INTO expenses (expense_date, category, amount, note) VALUES (?, ?, ?, ?)",
            (expense_date, category, amount, note.strip()),
        )
        return cursor.lastrowid


def get_expenses():
    """Return all expenses, newest first."""
    with connect_db() as connection:
        return connection.execute(
            "SELECT id, expense_date, category, amount, note "
            "FROM expenses ORDER BY expense_date DESC, id DESC"
        ).fetchall()


def get_total():
    """Return the total amount spent."""
    with connect_db() as connection:
        row = connection.execute("SELECT COALESCE(SUM(amount), 0) AS total FROM expenses").fetchone()
        return float(row["total"])


def delete_expense(expense_id):
    """Delete an expense by ID. Return True if a row was deleted."""
    with connect_db() as connection:
        cursor = connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cursor.rowcount > 0


def export_to_csv(filename="expenses_export.csv"):
    """Export saved expenses to a CSV file."""
    rows = get_expenses()
    output_path = Path(filename)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ID", "Date", "Category", "Amount", "Note"])
        for row in rows:
            writer.writerow([row["id"], row["expense_date"], row["category"], f'{row["amount"]:.2f}', row["note"]])
    return output_path.resolve()


def show_expenses():
    expenses = get_expenses()
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print("\nID | Date       | Category        | Amount   | Note")
    print("-" * 68)
    for item in expenses:
        print(
            f'{item["id"]:>2} | {item["expense_date"]} | '
            f'{item["category"][:15]:<15} | ₹{item["amount"]:>7.2f} | {item["note"]}'
        )
    print(f"\nTotal spent: ₹{get_total():.2f}")


def prompt_add_expense():
    expense_date = input("Date (YYYY-MM-DD, blank for today): ").strip() or date.today().isoformat()
    category = input("Category (e.g., Food, Travel): ")
    amount = input("Amount (₹): ")
    note = input("Note (optional): ")
    try:
        expense_id = add_expense(expense_date, category, amount, note)
        print(f"Expense saved successfully (ID: {expense_id}).")
    except ValueError as error:
        print(f"Could not save expense: {error}")


def main():
    connect_db().close()
    while True:
        print(
            "\n=== PERSONAL EXPENSE TRACKER ===\n"
            "1. Add expense\n"
            "2. View expenses and total\n"
            "3. Delete expense\n"
            "4. Export expenses to CSV\n"
            "5. Exit"
        )
        choice = input("Choose an option (1-5): ").strip()
        if choice == "1":
            prompt_add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            try:
                expense_id = int(input("Enter expense ID to delete: "))
                print("Expense deleted." if delete_expense(expense_id) else "No expense found with that ID.")
            except ValueError:
                print("Please enter a valid numeric ID.")
        elif choice == "4":
            path = export_to_csv()
            print(f"Expenses exported to: {path}")
        elif choice == "5":
            print("Thank you for using Personal Expense Tracker!")
            break
        else:
            print("Invalid choice. Please choose a number from 1 to 5.")


if __name__ == "__main__":
    main()
