# Budget Calculator
A budgeting app written in Python. Simply run the BudgetCalc.py file and enjoy.
Includes the following features:
- Add/remove custom categories and allowances.
- Income is automatically added to 'Money Left This Week' every week.
- Values can be reset and changed in the config.ini file.

Requires the following libraries:
- Pillow
- Tkinter
- Arrow

Please ensure these are all installed before attempting to run the app.

Usage:
- To deduct a value from one of the categories, simply type in the amount you spent and click "Calculate".
- Your weekly 'Goal' is calculated as the sum of expenses subtracted from your income i.e. Goal = Expenses - Income.
  If your income is less than your expenses, your weekly goal will be negative. This means that you will lose x amount each week.
- Change your income by altering the u_inc value in the config.ini file.
- By clicking Manage, you can add categories, change categorie allowances, and remove categories.
- To remove a categorie, you must type the name EXACTLY as it is displayed in the app.
