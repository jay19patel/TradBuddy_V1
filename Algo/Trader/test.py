import concurrent.futures

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
        "Strategy_2": ["NSE:NIFTYBANK-INDEX", "NSE:NIFTY50-INDEX"]
    }
}

def print_results(account_id, strategy_name, symbol, status, updated_datetime):
    print(f"Results for Account ID: {account_id}, Strategy: {strategy_name}, Symbol: {symbol}, Status: {status}, Updated Datetime: {updated_datetime}")

def worker(account_id, strategies):
    for strategy_name, symbols in strategies.items():
        for symbol in symbols:
            if symbol in strategies_results:
                result = strategies_results[symbol]
                print(account_id, strategy_name, symbol, result[f'{strategy_name.lower()}_status'], result['updated_datetime'])

def main():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for account_id, strategies in Account_list.items():
            futures.append(executor.submit(worker, account_id, strategies))
        for future in concurrent.futures.as_completed(futures):
            future.result()

if __name__ == "__main__":
    main()
