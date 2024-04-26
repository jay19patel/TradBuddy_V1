import time
import asyncio

strategies_results = {
    "NSE:NIFTY50-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"},
    "NSE:NIFTYBANK-INDEX": {"strategy_1_status": "CE", "strategy_2_status": "PE", "updated_datetime": "2024-04-20 22:43:42"}
}

account_strategies = {
    111: [("NSE:NIFTY50-INDEX", "strategy_1_status"), ("NSE:NIFTYBANK-INDEX", "strategy_1_status")],
    222: [("NSE:NIFTY50-INDEX", "strategy_2_status"), ("NSE:NIFTYBANK-INDEX", "strategy_2_status")]
}
def Time_set_for_next_day(market_status):
    schedule.clear()
    schedule.every().day.at("09:15").do(Worker)
    print(f"Market Status is : {market_status}")

async def strategy_code(account_id, strategies):
    for symbol, strategy in strategies:
        status = strategies_results[symbol][strategy]
        # Process status, e.g., await some_async_function(status)
        # await asyncio.sleep(3)  # Replace this with your actual processing
        print(symbol, strategy,status)

async def process_account(account_id, strategies):
    await strategy_code(account_id, strategies)

async def main():
    start_time = time.time()
    tasks = [process_account(account_id, strategies) for account_id, strategies in account_strategies.items()]
    await asyncio.gather(*tasks)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution Time: {execution_time} seconds")

# Run the async function
asyncio.run(main())
