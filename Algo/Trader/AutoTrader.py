
import threading
import time
import schedule
from datetime import datetime,timedelta
import os
import json 
from Broker.FyersBroker import Fyers

fyers_obj = Fyers()
fyers_obj.authentication()

def Time_set_for_next_day(market_status):
    schedule.clear()
    schedule.every().day.at("09:15").do(Worker)
    print(f"Market Status is : {market_status}")


Strategy_path = f"{os.getcwd()}/Records/strategies_results.json"

def Worker():
    with open(strategy_path, 'r') as file:
        strategies_results = json.load(file)


def RunWorker():
    current_time = datetime.now().time()
    market_status = fyers_obj.MarketStatus()
    if datetime.strptime("9:15", "%H:%M").time() <= current_time <= datetime.strptime("15:15", "%H:%M").time() and market_status == "OPEN":
        print("Algorithm is Online")
        schedule.every(1).minutes.do(lambda: Time_set_for_next_day() if current_time > datetime.strptime("15:15", "%H:%M").time() else Worker())
    else:
        Time_set_for_next_day(market_status)
    while True:
        schedule.run_pending()
        time.sleep(1)