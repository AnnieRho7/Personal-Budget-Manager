from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
    # Load credentials from the JSON file
    CREDS = Credentials.from_service_account_file('creds.json')
    SCOPED_CREDS = CREDS.with_scopes(SCOPE)
    GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
except Exception as e:
    print("Error loading credentials or authorizing gspread client:", e)
    exit(1)

try:
    # Open the spreadsheet
    SHEET = GSPREAD_CLIENT.open('personal-budget-manager')
except Exception as e:
    print("Error opening spreadsheet:", e)
    exit(1)

try:
    # Access worksheets
    INCOME_SHEET = SHEET.worksheet('income')
    EXPENSES_SHEET = SHEET.worksheet('expenses')
    SUMMARY_SHEET = SHEET.worksheet('summary')
except Exception as e:
    print("Error accessing worksheets:", e)
    exit(1)

expenses = []


def loadExpenses():
    """
    Loads the existing expenses from the Google Sheets.
    """
    expenses.clear()  # Clear the existing list to avoid duplicates

    category_column = {
        "Rent/Mortgage": "A",
        "Utilities": "B",
        "Shopping": "C",
        "Transport": "D",
        "Insurance": "E",
        "Entertainment": "F",
        "Savings": "G",
        "Miscellaneous": "H"
    }

    try:
        for category, column in category_column.items():
            column_index = column_to_index(column)
            values = EXPENSES_SHEET.col_values(column_index)

            for amount in values[1:]:  # Skip the header
                if amount.strip():
                    expenses.append({
                        'amount': float(amount),
                        'category': category
                    })
    except Exception as e:
        print("Error loading expenses:", e)


def addIncome(amount, category):
    """
    Adds an income entry to the income list.
    """
    try:
        amount = float(amount)

        # Define the category to column mapping
        category_column = {
            "Salary": "A",
            "Freelance": "B",
            "Misc": "C"
        }

        if category not in category_column:
            print("Invalid category. Please choose from 1, 2, 3")
            return

        # Update the income list 
        updateIncomeSheet(category, amount)
        print(f"€{amount:.2f} was successfully uploaded to {category}.")

    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
    except Exception as e:
        print("Error adding income:", e)


def updateIncomeSheet(category, amount):
    """
    Updates the Google Sheets with the new income data.
    """
    category_column = {
        "Salary": "A",
        "Freelance": "B",
        "Misc": "C"
    }

    try:
        column = category_column[category]
        column_index = column_to_index(column)
        existing_values = INCOME_SHEET.col_values(column_index)
        row_to_update = len(existing_values) + 1

        # Update the cell with the new amount
        INCOME_SHEET.update_cell(row_to_update, column_index, amount)
        print(f"Income added to {category}: €{amount:.2f}")

    except Exception as e:
        print("Error updating income sheet:", e)


def addExpense(amount, category):
    """
    Adds an expense and updates the Google Sheet.
    """
    try:
        amount = float(amount)

        category_column = {
            "1": "Rent/Mortgage",
            "2": "Utilities",
            "3": "Shopping",
            "4": "Transport",
            "5": "Insurance",
            "6": "Entertainment",
            "7": "Savings",
            "8": "Miscellaneous"
        }

        if category not in category_column:
            print("Invalid category. Please choose from 1 to 8")
            return

        category_name = category_column[category]

        updateExpenseSheet(category_name, amount)
        loadExpenses()  # Reload the expenses after adding a new one

        print(f"€{amount:.2f} was successfully uploaded to {category_name}.")

    except ValueError:
        print("Invalid amount. Please enter a numeric value.")
    except Exception as e:
        print("Error adding expense:", e)


def updateExpenseSheet(category, amount):
    """
    Updates the Google Sheets with the new expense data.
    """
    category_column = {
        "Rent/Mortgage": "A",
        "Utilities": "B",
        "Shopping": "C",
        "Transport": "D",
        "Insurance": "E",
        "Entertainment": "F",
        "Savings": "G",
        "Miscellaneous": "H"
    }

    try:
        column = category_column.get(category)
        if not column:
            raise ValueError(f"Column for category {category} not found.")

        column_index = column_to_index(column)
        existing_values = EXPENSES_SHEET.col_values(column_index)
        row_to_update = len(existing_values) + 1

        EXPENSES_SHEET.update_cell(row_to_update, column_index, amount)
        print(f"Expense added: {category} - €{amount:.2f}")

    except Exception as e:
        print("Error updating expense sheet:", e)


def column_to_index(column_letter):
    """
    Converts column letter (e.g., 'A') to its numeric index (1).
    """
    return ord(column_letter.upper()) - ord('A') + 1


def listExpenses():
    """
    Lists the last 10 expenses.
    """
    print("Last 10 Expenses:")
    for i, expense in enumerate(expenses[-10:], start=1):
        print(f"{i}. {expense['category']} - €{expense['amount']:.2f}")
    print()


def removeExpense():
    """
    Allows the user to remove an expense.
    Confirmation deleting expense.
    """
    if not expenses:
        print("No expenses to remove.")
        return

    print("Select the expense to remove:")
    listExpenses()

    try:
        selection = int(input("> "))
        if selection < 1 or selection > len(expenses):
            print("Please choose a valid expense number.")
            return
    except ValueError:
        print("Please enter a number.")
        return

    # Confirm deletion
    selected_expense = expenses[selection - 1]
    while True:
        confirmation = input(f"Remove {selected_expense['category']} - €{selected_expense['amount']:.2f}? (y/n): ").lower()
        if confirmation == 'y':
            try:
                expenses.pop(selection - 1)
                updateExpensesSheet()
                print("Expense removed.")
            except Exception as e:
                print("Error removing expense:", e)
            break
        elif confirmation == 'n':
            print("Operation canceled.")
            break
        else:
            print("Sorry, please choose 'y' or 'n'.")


def updateExpensesSheet():
    """
    Updates the Expense Worksheet.
    """
    try:
        # Preserve the headers
        headers = EXPENSES_SHEET.row_values(1)
        EXPENSES_SHEET.clear()
        EXPENSES_SHEET.insert_row(headers, 1)

        category_column = {
            "Rent/Mortgage": "A",
            "Utilities": "B",
            "Shopping": "C",
            "Transport": "D",
            "Insurance": "E",
            "Entertainment": "F",
            "Savings": "G",
            "Miscellaneous": "H"
        }

        for expense in expenses:
            category_name = expense['category']
            column = category_column[category_name]
            column_index = column_to_index(column)
            existing_values = EXPENSES_SHEET.col_values(column_index)
            row_to_update = len(existing_values) + 1
            EXPENSES_SHEET.update_cell(row_to_update, column_index, expense.get('amount'))
    except Exception as e:
        print("Error updating expenses sheet:", e)


def handleAddIncome():
    """
    Handle adding income by prompting user input for amount and category.
    """
    print("How much was this income?")
    while True:
        try:
            amountToAdd = input("> ")
            float(amountToAdd)
            break
        except ValueError:
            print("Invalid input. Please enter a valid amount.")

    print("Please choose a category:")
    print("1. Salary")
    print("2. Freelance")
    print("3. Misc")

    category_map = {
        "1": "Salary",
        "2": "Freelance",
        "3": "Misc"
    }

    while True:
        try:
            category_choice = input("> ")
            if category_choice in category_map:
                category = category_map[category_choice]
                break
            else:
                raise ValueError("Invalid input")
        except ValueError:
            print("Please enter a number between 1 and 3.")

    addIncome(amountToAdd, category)
    
def handleAddExpense():
    """
    Handle adding expense by prompting user input for amount and category.
    """
    print("How much was this expense?")
    while True:
        try:
            amountToAdd = input("> ")
            float(amountToAdd)
            break
        except ValueError:
            print("Please enter a valid amount.")

    print("Please choose a category (1-8):")
    print("1. Rent/Mortgage")
    print("2. Utilities")
    print("3. Shopping")
    print("4. Transport")
    print("5. Insurance")
    print("6. Entertainment")
    print("7. Savings")
    print("8. Miscellaneous")

    while True:
        try:
            category = input("> ")
            if category in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                addExpense(amountToAdd, category)
                loadExpenses()
                break
            else:
                raise ValueError("Invalid input")
        except ValueError:
            print("Enter a number between 1 and 8.")


def printMenu():
    """
    Displays the menu options to the user.
    """
    print('Please choose from one of the following options (1-6)... ')
    print('1. Add Income')
    print('2. Add Expense')
    print('3. Remove Expense')
    print('4. List expenses')
    print('5. View Summary')
    print('6. Exit')


if __name__ == "__main__":
    loadExpenses()
    while True:
        # Prompt the user
        printMenu()
        optionSelected = input('> ')

        if optionSelected == '1':
            handleAddIncome()

        elif optionSelected == '2':
            handleAddExpense()

        elif optionSelected == '3':
            removeExpense()

        elif optionSelected == '4':
            listExpenses()

        elif optionSelected == '5':
            print("Not implemented yet.")

        elif optionSelected == '6':
            print("Exiting the program.")
            break

        else:
            print("Please choose a number between 1 and 6.")
