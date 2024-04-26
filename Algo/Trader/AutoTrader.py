import threading
import time
import schedule
from datetime import datetime
import os
import json 
import asyncio
import pymongo
from dotenv import load_dotenv
import schedule
load_dotenv()

db_client = os.getenv("MONGODB_STRING")
verion = 2
mongo_connection = pymongo.MongoClient(db_client)[f'TradBuddy_V{verion}_Worker_1']
account_collection = mongo_connection.get_collection("Account")

Strategy_path = f"{os.getcwd()}/Records/strategies_results.json"


def Time_set_for_next_day(market_status):
    schedule.clear()
    schedule.every().day.at("09:15").do(Worker)
    print(f"Market Status is : {market_status}")




async def strategy_code(account_id, strategies):
    with open(Strategy_path, 'r') as file:
        strategies_results = json.load(file)

    for symbol, strategy in strategies:
        status = strategies_results[symbol][strategy]
        print(symbol, strategy, status)  # Process status


async def process_account(account_id, strategies):
    await strategy_code(account_id, strategies)

async def Worker():
    print("Worker run")
    account_strategies = {
        "account":111,
        "strategies" : {
            111: [("NSE:NIFTY50-INDEX", "strategy_1_status"), ("NSE:NIFTYBANK-INDEX", "strategy_1_status")],
            222: [("NSE:NIFTY50-INDEX", "strategy_2_status"), ("NSE:NIFTYBANK-INDEX", "strategy_2_status")]
        }
    }
    # for account in account_collection.find({"is_activate": "Activate"}):
    for account in account_strategies:
        account_id = account["_id"]
        strategies = account["strategies"]
        print(account_id,strategies)
        # await process_account(account_id, strategies)


def RunWorker():
    current_time = datetime.now().time()
    market_status = "Open"  # Assuming market is open for testing
    # if datetime.strptime("9:15", "%H:%M").time() <= current_time <= datetime.strptime("15:15", "%H:%M").time() and market_status == "Open":
    if market_status == "Open":
        print("Algorithm is Online")
        # schedule.every(1).minutes.do(lambda: Time_set_for_next_day() if current_time > datetime.strptime("15:15", "%H:%M").time() else lambda: asyncio.run(Worker()))
        # schedule.every(10).seconds.do(lambda: Time_set_for_next_day() if current_time > datetime.strptime("15:15", "%H:%M").time() else lambda: asyncio.run(Worker()))
        schedule.every(10).seconds.do(asyncio.run(Worker()))
    else:
        print("Market is closed")

    while True:
        schedule.run_pending()
        time.sleep(1)


