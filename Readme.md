
![image](https://github.com/jay19patel/TradBuddy_365/assets/107461719/ffbc8a82-847d-479d-a4df-cf88344ab8b1)

![image](https://github.com/jay19patel/TradBuddy_365/assets/107461719/365da78a-7a5b-4379-82ea-97add34bb4be)


![image](https://github.com/jay19patel/TradBuddy_365/assets/107461719/a5697c39-3283-4560-9f33-0d2bd4e6de6c)

![image](https://github.com/jay19patel/TradBuddy_365/assets/107461719/d4455beb-9836-40dd-a68c-315efb426ecd)


# TradBuddy Modules
![Untitled Diagram](https://github.com/jay19patel/TradBuddy/assets/107461719/5a9a27d8-51b6-42b9-81a2-23200fc1c6b7)


# Flow of Modules
![Flow](https://github.com/jay19patel/TradBuddy/assets/107461719/3f474c5e-c226-42da-b6c9-11a455317f78)



# Important Functionalities

    - Multiple User Support (Fyers Registration)
    - Multiple Accounts (Paper Trading, Real Trading, and Adjustable Account Settings)
    - Account Management (Automatic and Manual Adjustment of Settings like Stop Loss, Target, Trailing, etc.)
    - Automated Buy and Sell Orders
    - Risk Management 
    - Day-wise Analysis
    - Comprehensive Analysis Across All Accounts
    - Strategy Building and Selection, Customized for Different Accounts
    - Backtesting Capabilities
    - Each Component is Independent, Allowing for Individual Code Updates and Process Changes



# Function List

## TradBuddyBroker Class

### Methods
1. `profile_create`: Creates a new user profile.
2. `profile_login`: Authenticates a user profile.
3. `profile_get`: Retrieves the profile information of the authenticated user.
4. `account_create`: Creates a new trading account.
5. `account_update`: Updates the details of a trading account.
6. `account_get`: Retrieves the details of a specific trading account.
7. `account_list`: Lists all trading accounts associated with the authenticated user.
8. `account_delete`: Deletes a trading account.
9. `account_transaction_create`: Performs a transaction (deposit/withdrawal) for a trading account.
10. `account_transaction_view`: Retrieves the transaction history of a trading account.
11. `order_place`: Places a new order for trading.
12. `order_close`: Closes a specific order.
13. `order_book`: Retrieves the order book for a trading account.
14. `generate_report`: Generates a trading report for a trading account.
15. `perform_analysis`: Performs analysis on trading data for a specific account.

### Middleware
- `check_authentication`: Middleware function to check user authentication status before accessing certain methods.

### Custom Imports
- `pandas as pd`
- `generate_password_hash, check_password_hash` from `werkzeug.security`
- Custom imports from `DB.Connection` and `Utility.Generator`


