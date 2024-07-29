import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CATEGORY_COLUMN_EXPENSES = {
    "Rent/Mortgage": "A",
    "Utilities": "B",
    "Shopping": "C",
    "Transport": "D",
    "Insurance": "E",
    "Entertainment": "F",
    "Savings": "G",
    "Miscellaneous": "H"
}

CATEGORY_COLUMN_INCOME = {
    "Salary": "A",
    "Freelance": "B",
    "Misc": "C"
}

CATEGORY_MAPPING_EXPENSES = {
    "1": "Rent/Mortgage",
    "2": "Utilities",
    "3": "Shopping",
    "4": "Transport",
    "5": "Insurance",
    "6": "Entertainment",
    "7": "Savings",
    "8": "Miscellaneous"
}

CATEGORY_MAPPING_INCOME = {
    "1": "Salary",
    "2": "Freelance",
    "3": "Misc"
}


def load_gspread_client(credentials_file, scope):
    """Loads gspread client with given credentials and scope."""
    try:
        creds = Credentials.from_service_account_file(credentials_file)
        scoped_creds = creds.with_scopes(scope)
        client = gspread.authorize(scoped_creds)
        return client
    except Exception as e:
        print("Error loading credentials or authorizing gspread client:", e)
        exit(1)


def open_spreadsheet(client, spreadsheet_name):
    """Opens the Google Sheets spreadsheet with the given name."""
    try:
        sheet = client.open(spreadsheet_name)
        return sheet
    except Exception as e:
        print("Error opening spreadsheet:", e)
        exit(1)


def access_worksheet(sheet, worksheet_name):
    """Accesses the specified worksheet from the Google Sheets spreadsheet."""
    try:
        worksheet = sheet.worksheet(worksheet_name)
        return worksheet
    except Exception as e:
        print(f"Error accessing worksheet '{worksheet_name}':", e)
        exit(1)


GSPREAD_CLIENT = load_gspread_client('creds.json', SCOPE)
SHEET = open_spreadsheet(GSPREAD_CLIENT, 'personal-budget-manager')
INCOME_SHEET = access_worksheet(SHEET, 'income')
EXPENSES_SHEET = access_worksheet(SHEET, 'expenses')
SUMMARY_SHEET = access_worksheet(SHEET, 'summary')

expenses = []


def load_expenses():
    """Loads the existing expenses from the Google Sheets."""
    expenses.clear()  # Clear the existing list to avoid duplicates

    try:
        for category, column in CATEGORY_COLUMN_EXPENSES.items():
            column_index = column_to_index(column)
            values = EXPENSES_SHEET.col_values(column_index)

            for amount in values[1:]:  # Skip the header
                if amount.strip():
                    expenses.append({'amount': float(amount), 'category': category})

    except Exception as e:
        print("Error loading expenses:", e)


def add_income(amount, category):
    """Adds an income entry to the income list."""
    try:
        amount = float(amount)

        if category not in CATEGORY_COLUMN_INCOME:
            print("Invalid category. Please choose from 1, 2, 3\n")
            return
        # Update the income list
        update_income_sheet(CATEGORY_COLUMN_INCOME[category], amount)
        print(f"€{amount:.2f} was successfully uploaded to {category}.\n")

    except ValueError:
        print("Invalid amount. Please enter a numeric value.\n")
    except Exception as e:
        print("Error adding income:", e)


def update_income_sheet(column, amount):
    """Updates the Google Sheets with the new income data."""
    try:
        column_index = column_to_index(column)
        existing_values = INCOME_SHEET.col_values(column_index)
        row_to_update = len(existing_values) + 1

        INCOME_SHEET.update_cell(row_to_update, column_index, amount)
        print(f"Income added: €{amount:.2f}")

    except Exception as e:
        print("Error updating income sheet:", e)


def add_expense(amount, category):
    """Adds an expense and updates the Google Sheet."""
    try:
        amount = float(amount)

        if category not in CATEGORY_MAPPING_EXPENSES:
            print("Invalid category. Please choose from 1 to 8\n")
            return

        category_name = CATEGORY_MAPPING_EXPENSES[category]
        update_expense_sheet(CATEGORY_COLUMN_EXPENSES[category_name], amount)
        load_expenses()  # Reload the expenses after adding a new one

        print(f"€{amount:.2f} was successfully uploaded to {category_name}.\n")

    except ValueError:
        print("Invalid amount. Please enter a numeric value.\n")
    except Exception as e:
        print("Error adding expense:", e)


def update_expense_sheet(column, amount):
    """Updates the Google Sheets with the new expense data."""
    try:
        column_index = column_to_index(column)
        existing_values = EXPENSES_SHEET.col_values(column_index)
        row_to_update = len(existing_values) + 1

        EXPENSES_SHEET.update_cell(row_to_update, column_index, amount)
        print(f"Expense added: €{amount:.2f}\n")

    except Exception as e:
        print("Error updating expense sheet:", e)


def column_to_index(column_letter):
    """
    Converts column letter (e.g., 'A') to its numeric index (1).
    """
    return ord(column_letter.upper()) - ord('A') + 1


def list_expenses():
    """Lists the last 10 expenses."""

    print("Last 10 Expenses:")
    for i, expense in enumerate(expenses[-10:], start=1):
        print(f"{i}. {expense['category']} - €{expense['amount']:.2f}")


def remove_expense():
    """Allows the user to remove an expense."""

    if not expenses:
        print("No expenses to remove.\n")
        return

    print("Select the expense to remove:\n")
    list_expenses()

    try:
        selection = int(input("> "))
        if selection < 1 or selection > len(expenses):
            print("Please choose a valid expense number.\n")
            return
    except ValueError:
        print("Please enter a number.\n")
        return

    # Confirm deletion
    selected_expense = expenses[selection - 1]
    while True:
        confirmation = input(f"Remove {selected_expense['category']} - €{selected_expense['amount']:.2f}? (y/n): ").lower()
        if confirmation == 'y':
            try:
                expenses.pop(selection - 1)
                update_expenses_sheet()
                print("Expense removed.\n")
            except Exception as e:
                print("Error removing expense:", e)
            break
        elif confirmation == 'n':
            print("Operation canceled.\n")
            break
        else:
            print("Sorry, please choose 'y' or 'n'.\n")


def update_expenses_sheet():
    """Updates the Expense Worksheet."""

    try:
        # Preserve the headers
        headers = EXPENSES_SHEET.row_values(1)
        EXPENSES_SHEET.clear()
        EXPENSES_SHEET.insert_row(headers, 1)

        for expense in expenses:
            category_name = expense['category']
            column = category_column[category_name]
            column_index = column_to_index(column)
            existing_values = EXPENSES_SHEET.col_values(column_index)
            row_to_update = len(existing_values) + 1
            EXPENSES_SHEET.update_cell(row_to_update, column_index, expense.get('amount'))
    except Exception as e:
        print("Error updating expenses sheet:", e)


def handle_add_income():
    """Handle adding income by prompting user input for amount and category."""
    print("How much was this income?")
    while True:
        try:
            amount_to_add = input("> ")
            float(amount_to_add)
            break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    print("Please choose a category:")
    for key, value in CATEGORY_MAPPING_INCOME.items():
        print(f"{key}. {value}")

    while True:
        try:
            category_choice = input("> ")
            if category_choice in CATEGORY_MAPPING_INCOME:
                category = CATEGORY_MAPPING_INCOME[category_choice]
                break
            else:
                raise ValueError("Invalid input")
        except ValueError:
            print("Please enter a number between 1 and 3.")

    add_income(amount_to_add, category)


def handle_add_expense():
    """
    Handle adding expense by prompting user input for amount and category.
    """
    print("How much was this expense?")
    while True:
        try:
            amount_to_add = input("> ")
            float(amount_to_add)
            break
        except ValueError:
            print("Please enter a valid amount.\n")

    print("Please choose a category (1-8):")
    for key, value in CATEGORY_MAPPING_EXPENSES.items():
        print(f"{key}. {value}")

    while True:
        try:
            category = input("> ")
            if category in CATEGORY_MAPPING_EXPENSES:
                add_expense(amount_to_add, category)
                load_expenses()
                break
            else:
                raise ValueError("Invalid input")
        except ValueError:
            print("Enter a number between 1 and 8.\n")


def calculate_total_income():
    """Calculate the total income from the income sheet."""

    category_columns = ["A", "B", "C"]  # Columns for Salary, Freelance, and Misc
    total_income = 0.0

    for column in category_columns:
        values = INCOME_SHEET.col_values(column_to_index(column))
        for amount in values[1:]:  # Skip the header
            if amount.strip():
                # Remove commas from the amount string
                amount = amount.replace(',', '')
                total_income += float(amount)

    return total_income


def calculate_total_expenses():
    """Calculate the total expenses from the expense sheet."""

    category_columns = ["A", "B", "C", "D", "E", "F", "G", "H"]  # Columns for all expense categories
    total_expenses = 0.0

    for column in category_columns:
        values = EXPENSES_SHEET.col_values(column_to_index(column))
        for amount in values[1:]:  # Skip the header
            if amount.strip():
                amount = amount.replace(',', '')
                total_expenses += float(amount)

    return total_expenses


def calculate_total_net_savings(total_income, total_expenses):
    """Calculates the total net savings."""

    return total_income - total_expenses


def view_summary():
    """Displays the summary of total income, expenses, and net savings, and updates the summary worksheet."""

    try:
        total_income = calculate_total_income()
        total_expenses = calculate_total_expenses()
        total_net_savings = calculate_total_net_savings(total_income, total_expenses)

        print(f"Total Income: €{total_income:.2f}")
        print(f"Total Expenses: €{total_expenses:.2f}")
        print(f"Total Net Savings: €{total_net_savings:.2f}\n")

        update_summary_sheet(total_income, total_expenses, total_net_savings)

    except Exception as e:
        print("Error viewing summary:", e, "\n")


def update_summary_sheet(total_income, total_expenses, total_net_savings):
    """Updates the summary worksheet with the total income, total expenses, and total net savings."""
    try:
        cell_range = 'A2:C2'
        values = [[total_income, total_expenses, total_net_savings]]

        SUMMARY_SHEET.update(values, cell_range)
    except Exception as e:
        print("Error updating summary sheet:", e)


def print_break():
    print("\n" + "-" * 40 + "\n")


def print_menu():
    """Displays the menu options to the user."""

    print('Please choose from one of the following options (1-6)... ')
    print('1. Add Income')
    print('2. Add Expense')
    print('3. Remove Expense')
    print('4. List expenses')
    print('5. View Summary')
    print('6. Exit')


if __name__ == "__main__":
    load_expenses()
    while True:
        # Prompt the user
        print_menu()
        optionSelected = input('> ')
        if optionSelected == '1':
            handle_add_income()
        elif optionSelected == '2':
            handle_add_expense()
        elif optionSelected == '3':
            remove_expense()
        elif optionSelected == '4':
            list_expenses()
        elif optionSelected == '5':
            view_summary()
        elif optionSelected == '6':
            print("You have exited the program.")
            break

        else:
            print("Error. Please choose a number between 1 and 6.\n")
