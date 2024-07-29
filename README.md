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

I manually tested this project by doing the following:
- Passed it through the PEP8 linter and confirmed there are no major errors.
- Giving invaild inputs: String when numbers are expected. Trying to remove an expense that doesnt exist.
- Tested my local terminal and the Code Institute Heroku terminal.

### Bugs

### Known Issues and Resolutions

1. **Quota Exceeded Error**
   - **Description:** The application may encounter a `Quota Exceeded` error when the number of read requests to the Google Sheets API exceeds the allowed quota.
   - **Resolution:** Implement rate limiting and batch requests to manage API usage efficiently. Optimise the number of API calls made by the application.
   ![Quota Exceed Error](/readmeimages/error.png)

2. **Line Length Exceeding PEP 8 Standards**
   - **Description:** Some lines of code exceed the recommended 79-character limit set by PEP 8.
   - **Resolution:** Refactor long lines into shorter lines by breaking them up or using intermediate variables to improve readability.
   - I tried to fix this bug and follow the PEP8 guildlines but I still got an error.
   ![PEP8](/readmeimages/pep8v.png)

   ![PEP8](/readmeimages/error4.png)

   ![PEP8](/readmeimages/error3.png)
   

3. **Invalid User Input Handling**
   - **Description:** The error message for invalid menu options is generic and not very descriptive.
   - **Resolution:** Update error messages to clearly indicate when user input is invalid and guide users to provide the correct input.
   ![Error handling](/readmeimages/error2.png)


## Deployment

### Local Deployment

1. Clone the repository.
2. Install the required dependencies.
3. Set up Google Sheets API credentials.
4. Run the application.

### Heroku Deployment

1. Fork or clone the repository.
2. Create a new Heroku app.
3. Set buildpacks to python and NodeJS in that order.
4. Link the Heroku app to the repository.
5. Click on Deploy.

## Credits and References

- Code Institute for the deployment terminal and walk through project.
- My tutor for sharing various projects which gave me the inspiration to create a personal budget manager.
- My mentor for helping me refine my code and deepen my understanding of best practices.
- Youtube Educators. For their insightful tutorials and guidance on coding practices. Special thanks to Programming with Mosh, Shaun Halverson, Tech With Tim, and Internet Made Coder for their educational content.
- ChatGPT and Perplexity for their support in breaking down and understanding complex code concepts.
- W3Schools for their resources and tutorials that facilitated learning and coding throughout this project.

