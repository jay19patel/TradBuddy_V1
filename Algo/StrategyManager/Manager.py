
import time
import json
from datetime import datetime,timedelta
import schedule
import logging
import concurrent.futures
import os
from Algo.Strategys.BaseStategys import strategy_1, strategy_2

logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def Time_set_for_next_day():
    schedule.clear()
    schedule.every().day.at("09:15").do(start_algo)
    logging.info("Algorithm scheduled for the next day")


def store_strategy_statuses(fyers_obj):   
    print("Updating strategy statuses...")
    Symbol = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
    TimeFrame = "15"
    results = {}

    def find_entries(index_data):
        # index_data is live Price 
        try:
            data = fyers_obj.Historical_Data(index_data[0], TimeFrame)
            strategy_1_status = strategy_1(data, index_data[1])
            strategy_2_status = strategy_2(data, index_data[1])
            return index_data[0], {
                "strategy_1_status": strategy_1_status,
                "strategy_2_status": strategy_2_status,
                "price":index_data[1],
                "updated_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            error_msg = f"Error occurred while processing {index_data[0]}: {e}"
            print(error_msg)
            logging.error(error_msg)
            return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in executor.map(find_entries, zip(Symbol, fyers_obj.get_current_ltp(",".join(Symbol)).values())):
            if result:
                results[result[0]] = result[1]

    with open(f"{os.getcwd()}/Records/strategies_results.json", "w") as f:
        json.dump(results, f)
    logging.info("Status Update successful")


# def start_algo(fyers_obj):
#     current_time = datetime.now().time()
#     market_status = fyers_obj.MarketStatus()
#     if datetime.strptime("9:15", "%H:%M").time() <= current_time <= datetime.strptime("15:15", "%H:%M").time() and market_status == "OPEN":
#         logging.info("Algorithm is Online")
#         schedule.every(1).minutes.do(lambda: Time_set_for_next_day() if current_time > datetime.strptime("15:15", "%H:%M").time() else store_strategy_statuses(fyers_obj))
#     else:
#         logging.info("Algorithm is Offline")
#         Time_set_for_next_day()


def StrategyManagerExecution(fyers_obj):
    schedule.every(30).seconds.do(lambda: store_strategy_statuses(fyers_obj))
    while True:
            schedule.run_pending()
            time.sleep(1)

