import json
import logging
import os
from datetime import datetime
import asyncio

from Algo.Strategys.BaseStategys import strategy_1, strategy_2
from Utility.TimeSupervisor import market_time_decorator
from Utility.HistoricalData import GetHistoricalDataframe
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def find_entries(index_data, fyers_obj, TimeFrame):
    try:
        data = GetHistoricalDataframe(fyers_obj,index_data[0],TimeFrame)
        strategy_1_task = strategy_1(data, index_data[1])
        strategy_2_task = strategy_2(data, index_data[1])
        strategy_1_status, strategy_2_status = await asyncio.gather(strategy_1_task, strategy_2_task)
        
        return index_data[0], {
            "strategy_1_status": strategy_1_status,
            "strategy_2_status": strategy_2_status,
            "price": index_data[1],
            "updated_datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        error_msg = f"Error occurred while processing {index_data[0]}: {e}"
        print(error_msg)
        logging.error(error_msg)
        return []


async def store_strategy_statuses(fyers_obj):   
    print("Strategy Manager is Runing.")
    Symbol = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
    TimeFrame = "15"
    results = {}

    index_data = zip(Symbol, fyers_obj.get_current_ltp(",".join(Symbol)).values())
    gathered_results = await asyncio.gather(*(find_entries(data, fyers_obj, TimeFrame) for data in index_data))
    
    for result in gathered_results:
        if result:
            results[result[0]] = result[1]

            
    output_file_path = os.path.join(os.getcwd(), "Records", "strategies_results.json")
    try:
        with open(output_file_path, "w") as f:
            json.dump(results, f)
        logging.info("Strategy Manager Status Update successful")
    except Exception as e:
        error_msg = f"Error occurred while writing to strategies_results.json: {e}"
        print(error_msg)
        logging.error(error_msg)

@market_time_decorator(Open_time = "9:15",Close_time = "23:15",market_status="Open",Interval = 30)
def StrategyManagerExecution(fyers_obj):
    asyncio.run(store_strategy_statuses(fyers_obj))

