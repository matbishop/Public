# CS50w Capstone: Finance

Requirements: [https://cs50.harvard.edu/web/2020/projects/final/capstone/](https://cs50.harvard.edu/web/2020/projects/final/capstone/)  
Demo: [https://youtu.be/uStb1hElwqw](https://youtu.be/uStb1hElwqw)

> This is my final project for CS50w. It is a financial application that allows a user to look up price information regarding more than 100 000 worldwide tickers with information obtained from Yahoo Finance. The user can log transactions on any of these tickers and create a portfolio which consolidates these transactions, converts them into a common currency and displays whether the user has made a combined profit or loss. In addition to this is a financial calculator to calculate ordinary and deferred future values for annuities with support for most commonly used interest rate periods. Conversion can also be done to calculate corresponding interest rates for different time periods.

## Languages, Frameworks & Packages
- Python
- [Django](https://www.djangoproject.com) with SQLite backend
- JavaScript
- HTML
- CSS
- [Bootstrap](https://getbootstrap.com)
- [yfinance](https://pypi.org/project/yfinance/)

## Functionality
The project starts with an investment calculator section that simplifies the calculation of annuities. The calculator presents the user with simple, easy to understand inputs and handles the calculations entirely with JavaScript. This allows instantaneous calculations - no reload of the page necessary.

The annuity calculator converts interest rates from any common period to an effective monthly or yearly rate (depending on contribution frequency), and a separate calculator is also present to present this functionality to the user. For this calculator to be useful, it can calculate an effective rate not only of monthly or annual periods, but all common periods.

The application also includes real-time lookup of information on more than 100 000 tickers. With the goal of using information from Yahoo Finance, a publicly available Python module is used. I included functionality to convert currencies using Python to determine the appropriate ticker to use in each case. 


Because of the availability of real-time information I added functionality to log real transactions made by a user. Information regarding these transactions is then found by looking up current information, whereafter profits and losses are also calculated. These transactions are then consolidated into a portfolio, and real time portfolio values are calculated after all transactions are converted to share a common currency - implemented as USD. Transactions can be removed and the portfolio will update accordingly.

## Files

### Templates

#### layout.html
All HTML files that follow extend `layout.html`, which contains the header linking the JavaScript, CSS and Bootstrap and common navigation bar. The navigation bar changes based on if a user is logged in or not, as specified in the next file explanation.

#### index.html
A home page that serves as a launcher to other parts of the application. If the user is not signed in, options to register and log in are presented, while the transaction and portfolio functionality is presented if a user is signed in.

#### login.html & register.html
These pages allow a user to register for the application and log in if they already have an account. These two pages are derived from earlier projects in CS50w, modified to have the desired functionality and look required for this application.

#### calculator.html
The calculator page consists of two sections as specified below. The logic for this page is completely written in JavaScript, and as such when doing calculations the page does not require a reload.

##### Interest Conversion
This section allows a user to convert interest rates from one compounding period to another. The conversion is accurate to 5 decimal places. The input and output period can be chosen from the following periods: Annually, Semiannually, Quarterly, Monthly, Weekly, Daily and Continuously.

Please note interest rate conversions are done on an assumption of 52 weeks and 365 days respectively.

##### Annuity Values
This section allows the user to calculate the future value of an annuity. Ordinary and deferred annuities are supported, as well as a choice between monthly and annual contributions. The interest rate can be given in any of the periods as listed above. 

#### shares.html
This page allows the lookup of information on any ticker present on Yahoo Finance. The following pricing information is provided: Currency, Price, 50 Day Moving Average, 100 Day Moving Average, Year Change, Year Low and Year High.

#### currency.html
This page allows the conversion of currencies. To determine the price of any currency simply input the desired currencies. The currencies should be provided in abbreviated form - ex. USD for United States Dollars. The amounts can be changed as desired.

#### transactions.html
This page allows the user to enter transactions with real-world data. The application was designed in a manner that a user can choose how a profit is calculated - inclusive or exclusive of fees. The user can choose to provide the value of a transaction inclusive or exclusive of fees, whereafter the result of the calculations will take this into account - if a value inclusive of fees is used as input, the profit shown will be a "true" profit.

The transactions offer a high degree of accuracy, as demonstrated with the precision supported:

- Transaction Value: max digits = 15, max decimal digits = 5  
- Share Amount: max digits = 21, max decimal digits = 5  

Support for the timestamp of a transaction is present, allowing for possible future implementation of calculations for precise returns over a respective period. Transactions are displayed in their respective original currency, and can easily be removed.

#### portfolio.html
The portfolio consolidates all the transactions the user has made. This is done by combining different transactions a user has made of a common ticker, and calculating a combined profit or loss. The portfolio also converts all transactions to USD, so that all entries on the page are displayed in the same currency. These converted transactions are also consolidated to show a combined profit or loss.

The total profit or loss of a user is also calculated and shown at the bottom of the table. This includes the original value the user has spent in total, converted into USD. Each respective ticker in the portfolio is accompanied by a red or green indicator, to show whether a consolidated profit or loss has been achieved.


### Static
#### styles.css
Additional styling is specified here as well as the functionality to make the application mobile responsive. This includes making tables on devices with narrower viewports scrollable.

#### finance.js
This file handles all logic for the calculator of the application. This allows the calculator to be used in browser without the need for reloading when calculating an answer. 

### Shell
#### create_site.sh
This file includes commands that can be run in the shell `python manage.py shell`, quickly creating an example user with a portfolio. The demo user (username `user1`, password `user1`) has multiple transactions with multiple tickers in multiple currencies, demonstrating the conversion, consolidation and calculation features of the portfolio section.

#### reset.sh
This file contains commands that can be run to delete all users and transactions in order to clear the application.

## How to Run
### Set Up
- Create migrations:  
`python manage.py makemigrations`  
`python manage.py migrate`
- Run application:  
`python manage.py runserver`
- Click on link provided in shell to open application in browser

### Create Demo User
- Run `python manage.py shell` in terminal
- Run commands specified in `shell/create_site.sh` (Note - if errors occur, run given commands manually in order provided)
- Sample user with username `user1` and password `user1` created with fictitious transactions & portfolio

### Reset application
- Run commands specified in `shell/reset.sh` in terminal
- Run application

## Possible improvements
- Sorting functionality for transactions - ex. all transactions of a specified ticker, a certain period or a certain return.
- Specific period return calculations.
- Optimisation: possible smarter lookup for transactions, as currently information for each transaction is obtained, even when information regarding the ticker has already been obtained
- Unit tests to verify answer values for the interest converter and annuity values (done manually during development)


