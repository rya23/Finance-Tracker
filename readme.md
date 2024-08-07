# Finance Tracker

Finance Tracker is a web application built with Django that helps you manage your finances by tracking expenses and incomes.


## Live Demo

Check out the [demo](https://rya234.pythonanywhere.com/) to see Finance Tracker in action!


## Features

- **Expense Tracking**: Add, edit, and delete expenses, categorize them, and view expense reports.
- **Income Tracking**: Record your income sources and keep track of your earnings.
- **Budget Management**: Set budgets for different expense categories and monitor your spending.
- **Monthly Reports**: View detailed reports of your expenses and incomes for each month.
- **User Authentication**: Authentication with Google Login .

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/rya23/FJ-BE-R2-Aarya-Thakur-Thadomal-Shahani-Engineering-College.git
   ```

2. Navigate to the project directory:

   ```
   cd FJ-BE-R2-Aarya-Thakur-Thadomal-Shahani-Engineering-College
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run database migrations:

   ```
   python manage.py migrate
   ```

5. Start the development server:

   ```
   python manage.py runserver
   ```

6. Access the application at `http://localhost:8000` in your web browser.

## Usage

1. Create a new account or log in if you already have one.
2. Add the category of expense or income sources
3. Add your expenses and incomes using the respective forms.
4. Set budgets for expense categories to manage your spending.
7. Get In App Alerts When Budget is exceeded
5. View monthly reports to analyze your financial activities.
6. Edit or delete entries as needed.


# Screenshots  


### Register Page

![register](/finance/static/Screenshot%202024-05-22%20at%2017-18-04%20Finance%20Tracker.png)

### Home Page
![home](/finance/static/Screenshot%202024-05-22%20at%2017-05-03%20Finance%20Tracker.png)

### Reports Page

![reports](/finance/static/Screenshot%202024-05-22%20at%2017-06-10%20Finance%20Tracker.png)


### Monthly Report
![reports](/finance/static/Screenshot%202024-05-22%20at%2017-48-59%20Finance%20Tracker.png)


### Category wise report
![category](/finance/static/Screenshot%202024-05-22%20at%2017-06-47%20Finance%20Tracker.png)


### Budget Exceeded Alert
![Budget Exceeded](/finance/static/Screenshot%202024-05-22%20at%2017-07-21%20Finance%20Tracker.png)
