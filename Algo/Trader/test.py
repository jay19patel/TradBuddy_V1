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
import asyncio

async def StrategyCode(args):
    name, strategy = args
    # print("Account Name :", name)
    for i in strategy:
        (symbol, strategy) = next(iter(i.items()))
        # print(strategies_results[symbol][strategy])
        # await asyncio.sleep(3)  # Replace this with your actual processing
        # print(symbol, strategy)

async def process_item(n):
    await StrategyCode((n['name'], n['strategy']))

start_time = time.time()

# Run all tasks concurrently
# Adjust the number of tasks based on your system's capabilities
tasks = [process_item(account) for account in Account_list]
await asyncio.gather(*tasks)

end_time = time.time()
execution_time = end_time - start_time
print(f"Execution Time: {execution_time} seconds")
