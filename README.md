# Personal Expense Tracker

A beginner-friendly command-line application built with Python and SQLite. It helps users record everyday expenses, view spending, remove incorrect entries, and export records to CSV.

## Features

- Add an expense with date, category, amount, and optional note
- View all saved expenses and the total amount spent
- Delete an expense using its ID
- Export expenses to a CSV file for use in spreadsheet software
- Store data locally in an SQLite database
- Validate dates and amounts and handle common input errors

## Technology

- Python 3.9+
- SQLite (`sqlite3`, included with Python)
- CSV module (included with Python)
- `unittest` for tests

No third-party packages are required.

## Run the project

1. Install Python 3.9 or newer.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

   ```bash
   python main.py
   ```

The `expenses.db` database file is created automatically when you run the program.

## Menu

1. Add expense
2. View expenses and total
3. Delete expense
4. Export expenses to CSV
5. Exit

## Example

```text
=== PERSONAL EXPENSE TRACKER ===
1. Add expense
2. View expenses and total
3. Delete expense
4. Export expenses to CSV
5. Exit
Choose an option (1-5): 1
Date (YYYY-MM-DD, blank for today):
Category (e.g., Food, Travel): Food
Amount (₹): 150
Note (optional): Lunch
Expense saved successfully (ID: 1).
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

The tests use a temporary database location so they do not change your normal expense records.

## Concepts demonstrated

- Variables and data types
- Functions and modular programming
- Input validation and exception handling
- SQL queries and parameterized statements
- SQLite database operations (CRUD: create, read, update/delete; this app implements create, read, and delete)
- CSV export
- Automated unit testing

## Possible improvements

- Add a graphical interface with Tkinter or a web interface with Flask
- Add monthly category summaries and budgets
- Add password-protected user accounts

## GitHub upload

Create a new repository on GitHub, then run these commands from this folder:

```bash
git init
git add .
git commit -m "Add Personal Expense Tracker project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/personal-expense-tracker.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. Create the empty GitHub repository first; do not add a README there if you are using this README.
