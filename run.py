import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('personal-budget-manager')

INCOME_SHEET = SHEET.worksheet('income')
EXPENSES_SHEET = SHEET.worksheet('expenses')
SUMMARY_SHEET = SHEET.worksheet('summary')

expenses = []

def addExpense(amount, category):
    """
    Adds an expense to the expenses list and updates the Google Sheet.
    """
    expense = {'amount': amount, 'category': category}
    expenses.append(expense)
    updateExpenseSheet(category, amount)  # Call the function to update Google Sheets
    
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

    # Get column letter for the selected category
    category_name = category_map[category]
    column = category_column[category_name]

    # Add the expense to the next available row in the appropriate column
    column_index = column_to_index(column)
    existing_values = EXPENSES_SHEET.col_values(column_index)
    row_to_update = len(existing_values) + 1

    # Update the cell with the new amount
    EXPENSES_SHEET.update_cell(row_to_update, column_index, amount)

def column_to_index(column_letter):
    """
    Converts column letter (e.g., 'A') to its numeric index (1).
    """
    return ord(column_letter.upper()) - ord('A') + 1

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
    expenses = []  # Initialize the expense list
    
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
    
    
