import concurrent.futures
from PlaceOrderManager import PlaceOrder

strategies_results = {
    "NSE:NIFTY50-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"},
    "NSE:NIFTYBANK-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"}
}

Account_list = {
    "111": {
        "Strategy_1": ["NSE:NIFTY50-INDEX"],
        "Strategy_2": ["NSE:NIFTYBANK-INDEX"]
    },
    "222": {
        "Strategy_1": ["NSE:NIFTY50-INDEX"],
        "Strategy_2": ["NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX"]
    },
    "333": {
        "Strategy_1": ["NSE:NIFTY50-INDEX"],
        "Strategy_2": ["NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX"]
    },
    "444": {
        "Strategy_1": ["NSE:NIFTY50-INDEX"],
        "Strategy_2": ["NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX", "NSE:NIFTYBANK-INDEX"]
    }
}

def worker(account_id, strategy_name, symbol, status):
    PlaceOrder(account_id, strategy_name, symbol, status)

def coin_current_check(executor, Account_list, strategies_results):
    futures = []
    for account_id, strategies in Account_list.items():
        for strategy_name, symbols in strategies.items():
            for symbol in symbols:
                if symbol in strategies_results:
                    result = strategies_results[symbol]
                    status = result[f'{strategy_name.lower()}_status']
                    futures.append(executor.submit(worker, account_id, strategy_name, symbol, status))
    for future in concurrent.futures.as_completed(futures):
        future.result()

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        coin_current_check(executor, Account_list, strategies_results)


if __name__ == "__main__":
    main()
