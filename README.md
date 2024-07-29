# Personal Budget Manager

## Introduction

The Personal Budget Manager is an application designed to help the user manage their personal finances using Google Sheets for data storage. It allows the user to track their income and expenses, categorise their spending, and view summaries of their financial data. This application is ideal for individuals looking to gain better control over their finances by tracking their expenses.

## Live Project

[View live project here](https://personal-budget-manager9-b331ef6b8de1.herokuapp.com/)

## Table of Contents

- [User Experience (UX)](#user-experience-ux)
  - [User Stories](#user-stories)
  - [Developer Goals](#developer-goals)
- [Features](#features)
  - [Add Income](#add-income)
  - [Add Expense](#add-expense)
  - [Remove Expense](#remove-expense)
  - [List Expenses](#list-expenses)
  - [View Summary](#view-summary)
  - [Future Features](#future-features)
- [Technologies Used](#technologies-used)
  - [Languages](#languages)
  - [Frameworks and Libraries](#frameworks-and-libraries)
  - [Tools](#tools)
- [Testing](#testing)
  - [Unit Testing](#unit-testing)
  - [Integration Testing](#integration-testing)
  - [User Acceptance Testing](#user-acceptance-testing)
  - [Resolved Bugs](#resolved-bugs)
- [Deployment](#deployment)
  - [Local Deployment](#local-deployment)
  - [Heroku Deployment](#heroku-deployment)
- [Credits and References](#credits-and-references)

## User Experience (UX)

### User Stories

- As a user, I want to easily add and categorise my income.
- As a user, I want to easily add and categorise my expenses.
- As a user, I want to view a list of my recent expenses.
- As a user, I want to remove expenses if needed.
- As a user, I want to view a summary of my total income, expenses, and net savings.

### Developer Goals

- As a developer, I want to create a user-friendly interface that is easy to navigate.
- As a developer, I want to ensure data security and privacy for users.
- As a developer, I want to build a scalable and maintainable codebase.

## Features

### Add Income

- Users can add new income entries by specifying the amount and category (Salary, Freelance, Misc).
- The income is then updated in the Google Sheets.

![Add Income](/readmeimages/addincome.png)

![Add Income](/readmeimages/addincome2.png)

![Add Income](/readmeimages/addincomesheet.png)

### Add Expense

- Users can add new expense entries by specifying the amount and category (Rent/Mortgage, Utilities, Shopping, etc.).
- The expenses are then updated in the Google Sheets.

![Add Expense](/readmeimages/addexpense.png)

![Add Expense](/readmeimages/addexpense2.png)

![Add Expense](/readmeimages/addexpensesheet.png)

### Remove Expense

- Users can remove expenses from their list.
- The Google Sheets are updated accordingly.

![Remove Expense](/readmeimages/removeexpense.png)

![Remove Expense](/readmeimages/removeexpense2.png)

![Remove Expense](/readmeimages/deleteconfirm.png)

### List Expenses

- Users can view a list of their last 10 expenses.

![Remove Expense](/readmeimages/listexpense.png)

![Remove Expense](/readmeimages/list.png)

### View Summary

- Users can view a summary of their total income, expenses, and net savings.
- The summary is updated in the Google Sheets.

![View Summary](/readmeimages/summary.png)

![View Summary](/readmeimages/summary2.png)

### Future Features

- Adding up expense categories for better tracking.
- Monthly tracking for better financial management.
- Budgeting tools to set and track financial goals.
- Mobile application for on-the-go access.

## Technologies Used

### Languages

- Python

### Frameworks and Libraries

- gspread (to interact with Google Sheets)
- Google Auth for authentication

### Tools

- GitHub for version control
- Heroku for deployment
- Google Cloud for API integrations

## Testing

### Unit Testing

-  (add later)

### Integration Testing

- (add later)

### User Acceptance Testing

- (add later)

### Resolved Bugs

-  (add later)

## Deployment

### Local Deployment

1. Clone the repository.
2. Install the required dependencies.
3. Set up Google Sheets API credentials.
4. Run the application.

### Heroku Deployment

-  (add later)

## Credits and References

-  (add later)