import gspread
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
    Loads the existing expenses from the Google Sheets into the expenses list.
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
        for category, column in category_column.items():
            column_index = column_to_index(column)
            values = EXPENSES_SHEET.col_values(column_index)

            for amount in values[1:]:
                if amount.strip():
                    expenses.append({
                        'amount': float(amount),
                        'category': category
                    })
    except Exception as e:
        print("Error loading expenses:", e)

def addExpense(amount, category):
    """
    Adds an expense to the expenses list and updates the Google Sheet.
    """
    try:
        expense = {'amount': float(amount), 'category': category}
        expenses.append(expense)
        updateExpenseSheet(category, amount)
    except Exception as e:
        print("Error adding expense:", e)

def updateExpenseSheet(category, amount):
    """
    Updates the Google Sheets with the new expense data.
    """
    category_map = {
        "1": "Rent/Mortgage",
        "2": "Utilities",
        "3": "Shopping",
        "4": "Transport",
        "5": "Insurance",
        "6": "Entertainment",
        "7": "Savings",
        "8": "Miscellaneous"
    }

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
        # Get column letter for the selected category
        category_name = category_map[category]
        column = category_column[category_name]

        # Add the expense to the next available row in the appropriate column
        column_index = column_to_index(column)
        existing_values = EXPENSES_SHEET.col_values(column_index)
        row_to_update = len(existing_values) + 1

        # Update the cell with the new amount
        EXPENSES_SHEET.update_cell(row_to_update, column_index, amount)
    except Exception as e:
        print("Error updating expense sheet:", e)

def column_to_index(column_letter):
    """
    Converts column letter (e.g., 'A') to its numeric index (1).
    """
    return ord(column_letter.upper()) - ord('A') + 1

def listExpenses():
    """
    Lists the last 10 expenses from the expenses list.
    """
    print("Last 10 Expenses:")
    for i, expense in enumerate(expenses[-10:], start=1):
        print(f"{i}. {expense['category']} - €{expense['amount']:.2f}")
    print()

def removeExpense():
    """
    Allows the user to remove an expense by selecting from the last 10 expenses listed.
    Ensures the user confirms the deletion before proceeding.
    """
    if not expenses:
        print("No expenses to remove.")
        return

    print("Select the expense to remove:")
    listExpenses()

    try:
        selection = int(input("> "))
        if selection < 1 or selection > len(expenses):
            print("Invalid selection. Please choose a valid expense number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    # Confirm deletion
    selected_expense = expenses[selection - 1]
    while True:
        confirmation = input(f"Are you sure you want to remove {selected_expense['category']} - €{selected_expense['amount']:.2f}? (yes/no): ").lower()
        if confirmation == 'yes':
            try:
                expenses.pop(selection - 1)
                updateExpensesSheet()
                print("Expense removed.")
            except Exception as e:
                print("Error removing expense:", e)
            break
        elif confirmation == 'no':
            print("Operation canceled.")
            break
        else:
            print("Sorry, please choose 'yes' or 'no'.")

def updateExpensesSheet():
    """
    Updates the Google Sheets with the current expense data.
    """
    try:
        # Clear the sheet first
        EXPENSES_SHEET.clear()

        # Re-populate the sheet with the updated expenses
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
            EXPENSES_SHEET.update_cell(row_to_update, column_index, expense['amount'])
    except Exception as e:
        print("Error updating expenses sheet:", e)

def printMenu():
    """
    Displays the menu options to the user.
    """
    print('Please choose from one of the following options (1-6)... ')
    print('1. Add Monthly Income')
    print('2. Add Expense')
    print('3. Remove Expense')
    print('4. List expenses')
    print('5. View Summary')
    print('6. Exit')

if __name__ == "__main__":
    loadExpenses()  # Load existing expenses from the spreadsheet
    while True:
        # Prompt the user
        printMenu()
        optionSelected = input('> ')

        if optionSelected == '1':
            print("Add Monthly Income is not implemented yet.")

        elif optionSelected == '2':
            print("How much was this expense?")
            while True:
                try:
                    amountToAdd = input("> ")
                    float(amountToAdd)  # Check if the input is a valid float number
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid amount.")

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
                        break
                    else:
                        raise ValueError("Invalid input")
                except ValueError:
                    print("Invalid input. Please enter a number between 1 and 8.")

            addExpense(amountToAdd, category)  # Call function to add expense to list and update Google Sheets

        elif optionSelected == '3':
            removeExpense()

        elif optionSelected == '4':
            listExpenses()

        elif optionSelected == '5':
            print("View Summary is not implemented yet.")

        elif optionSelected == '6':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please choose a number between 1 and 6.")