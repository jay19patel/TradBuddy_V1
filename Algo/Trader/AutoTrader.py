import asyncio
import os
import json
import schedule
from datetime import datetime
import time


from Algo.Trader.PlaceOrderManager import PlaceOrder

Strategy_path = f"{os.getcwd()}/Records/strategies_results.json"


def time_set_for_next_day():
    schedule.clear()
    schedule.every().day.at("09:15").do(worker)
    print("Market schedule set for the next day")


async def process_account(account,Fyers,TradBuddy):
    with open(Strategy_path, 'r') as file:
        strategies_results = json.load(file)
        account_number = account["account_id"]
        tasks = []
        for symbol, strategy_key in account["strategys"]:
            status = strategies_results.get(symbol, {}).get(strategy_key)
            price = strategies_results.get(symbol, {}).get("price")
            tasks.append(PlaceOrder(account_number, strategy_key, symbol, status,price,Fyers,TradBuddy))
        await asyncio.gather(*tasks)

async def worker(Fyers,TradBuddy):
    accounts = TradBuddy.account_list({"is_activate":"Activate"})
    await asyncio.gather(*(process_account(account,Fyers,TradBuddy) for account in accounts))


def run_worker(Fyers,TradBuddy):
    current_time = datetime.now().time()
    market_status = "Open"  
    if market_status == "Open":
        print("Algorithm is Online")
        # schedule.every(1).minutes.do(lambda: time_set_for_next_day() if current_time > datetime.strptime("15:15", "%H:%M").time() else asyncio.run(worker(Fyers,TradBuddy)))
        asyncio.run(worker(Fyers,TradBuddy))
    else:
        print("Market is closed")

    while True:
        schedule.run_pending()
        time.sleep(1)

