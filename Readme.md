# **Day 1**

## **Task 1**
- [1] **Create Base Folder and Link With Github**
- [2] **Work on TradBuddy Algo in Folder Name [Algo]**


# **Day 2**

## **Task 1**
- [1] **Create StrategyManager code to handle Market Status and Strategy Status**
- [2] **Get Live Data from market using Fyers**
- [3] **For Fyers, Create Fyers Authentication and Fyers APIs Code to receive Market Live Data**
- [4] **Manage Fyers and Get Historical data and Create Strategies and generate Signals**

```py
Fyers Class
Fyers Authentication
Fyers Historical data
Manager handle Hist data and Genarate json file and fetch evry 1 mintes live strategy Signal
```


# **Day 3**

## **Task 1**
- [1] **Create Trader folder and create AutoTrader.py file**
- [2] **In AutoTrader file we build Worker which buy and sell trad aAcroding Status**

```py
```
{"NSE:NIFTY50-INDEX": {"strategy_1_status": "None", "strategy_2_status": "CE", "price": 22419.95, "updated_datetime": "2024-04-28 22:34:13"}, "NSE:NIFTYBANK-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "None", "price": 48201.05, "updated_datetime": "2024-04-28 22:34:13"}}









ORDER EXIT PROCESS EXECUTE
ACC-001 ORD-1714403137471452559
STOPLOSS HIT
TB ORDER: {'_id': ObjectId('662fb741513c0c0f01df2163'), 'order_id': 'ORD-1714403137471452559', 'account_id': 'ACC-001', 'strategy': 'strategy_1_status', 'date': '29-04-2024', 'trad_status': 'Open', 'trad_type': 'Buy', 'trad_index': 'NSE:NIFTYBANK-INDEX', 'trad_side': 'PE', 'trigger_price': 49424.05, 'option_symbol': 'NSE:BANKNIFTY2443049400PE', 'qnty': 15, 'buy_price': 131.4, 'sell_price': None, 'stoploss_price': 9500.0, 'target_price': 11000.0, 'buy_datetime': datetime.datetime(2024, 4, 29, 20, 35, 37, 471000), 'sell_datetime': None, 'buy_margin': 1971.0, 'sell_margin': None, 'trailing_count': 1, 'pnl_status': None, 'pnl': None, 'notes': 'Test'}
{'message': 'order_close: fail - Something wrong in Order Close', 'body': None, 'status': 400}