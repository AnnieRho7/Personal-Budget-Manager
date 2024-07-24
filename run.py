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


def addExpense(amount, catagory):
    expense = {'amount': amount, {catagory}: catagory}
    expense.append(expense)


def printMenu():
    print('Please choose from one of the following options... ')
    print('Add Monthly Income')
    print('Add Expense')
    print('Remove Expense')
    print('List expenses')
    print('View Summary')