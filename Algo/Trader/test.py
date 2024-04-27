import asyncio

strategies_results = {
    "NSE:NIFTY50-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"},
    "NSE:NIFTYBANK-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"}
}

accounts = [
    {
        "account": 111,
        "strategies": [("NSE:NIFTY50-INDEX", "strategy_1_status"), ("NSE:NIFTYBANK-INDEX", "strategy_1_status")]
    },
    {
        "account": 222,
        "strategies": [("NSE:NIFTY50-INDEX", "strategy_2_status"), ("NSE:NIFTYBANK-INDEX", "strategy_1_status")]
    }
]


async def strategy_run(account, symbol, status):
    await asyncio.sleep(2)  # Wait for 2 seconds
    print(account, symbol, status)


async def process_account(account):
    account_number = account["account"]
    tasks = []
    for symbol, strategy_key in account["strategies"]:
        status = strategies_results.get(symbol, {}).get(strategy_key)
        tasks.append(strategy_run(account_number, symbol, status))
    await asyncio.gather(*tasks)


async def main():
    await asyncio.gather(*(process_account(account) for account in accounts))

if __name__ == "__main__":
    asyncio.run(main())
