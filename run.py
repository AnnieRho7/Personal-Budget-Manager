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
    updateExpenseSheet(category, amount) 
    
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

def listExpenses():
    """
    Lists the last 10 expenses from the expenses sheet.
    """
    # Define the column mapping for categories
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
    
    expenses_list = []
    
    # Fetch data for each category
    for category, column in category_column.items():
        column_index = column_to_index(column)
        values = EXPENSES_SHEET.col_values(column_index)
        
        # Exclude the header row and get expenses
        for amount in values[1:]:
            if amount.strip():  # Skip empty entries
                expenses_list.append({
                    'amount': float(amount),
                    'category': category
                })
    
    
    # Print the last 10 expenses
    print("Last 10 Expenses:")
    for i, expense in enumerate(expenses_list[-10:], start=1):
        print(f"{i}. {expense['category']} - €{expense['amount']:.2f}")
        
    print()

def removeExpense():
    """
    Removes an expense from the expenses sheet based on user selection.
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
    
    expenses_list = []

    # Fetch expenses from each category
    for category, column in category_column.items():
        column_index = column_to_index(column)
        values = EXPENSES_SHEET.col_values(column_index)[1:]  # Skip header
        
        for row_index, amount in enumerate(values, start=2):  # Start from row 2
            if amount.strip():  # Skip empty entries
                expenses_list.append({
                    'amount': float(amount),
                    'category': category,
                    'row_index': row_index
                })

    # Check if there are expenses to remove
    if not expenses_list:
        print("No expenses to remove.")
        return

    # Display the expenses to choose from
    print("Expenses to choose from for removal:")
    for i, expense in enumerate(expenses_list, start=1):
        print(f"{i}. {expense['category']} - €{expense['amount']:.2f}")

    # Get user input for the expense to remove
    while True:
        try:
            selection = int(input("Select the number of the expense to remove: "))
            if 1 <= selection <= len(expenses_list):
                break
            raise ValueError("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number corresponding to the expense.")

    # Remove the selected expense
    selected_expense = expenses_list[selection - 1]
    selected_row = selected_expense['row_index']
    category = selected_expense['category']
    
    # Clear the cell for the selected expense
    column_index_number = column_to_index(category_column[category])
    EXPENSES_SHEET.update_cell(selected_row, column_index_number, '')  # Clear the cell

    print(f"Removed {selected_expense['category']} - €{selected_expense['amount']:.2f} from the sheet.")

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
    
    
