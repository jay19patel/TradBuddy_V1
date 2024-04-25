import concurrent.futures

strategies_results = {
    "NSE:NIFTY50-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"},
    "NSE:NIFTYBANK-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"}
}

Account_list = [
    {
        "name": 111,
        "strategy": [
            {"NSE:NIFTY50-INDEX": "strategy_1_status"},
            {"NSE:NIFTYBANK-INDEX": "strategy_1_status"}
            ]
    },
    {
        "name": 222,
        "strategy": [
            {"NSE:NIFTY50-INDEX": "strategy_2_status"},
            {"NSE:NIFTYBANK-INDEX": "strategy_2_status"}
            ]
    }
]

def StrategyCode(args):
    name, strategy = args
    print("Account Name :",name)
    for i in strategy:
      (symbol, strategy) = next(iter(i.items()))
      print(strategies_results[symbol][strategy])
      print(symbol,strategy)

def process_item(n):
    with concurrent.futures.ThreadPoolExecutor() as executor1:
        executor1.map(StrategyCode, [(n['name'], n['strategy'])])

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_item, Account_list)
