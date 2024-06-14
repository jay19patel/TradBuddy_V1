from MicroScripts.DailyStacks.FetchData import OptionChain,FiiDii,AdvancesDecline
from Utility.TimeSupervisor import market_time_decorator
import datetime
import json
import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




db_client = os.getenv("MONGODB_STRING")
verion = 2
mongo_connection = pymongo.MongoClient(db_client)[f'TradBuddy_V{verion}_Worker_1']
dayly_stacks = mongo_connection["DailyStacks"]



@market_time_decorator(Open_time = "9:15",Close_time = "15:15",Interval = 300)
def get_overview(fyers_obj):
    try:
        option_chain_data = OptionChain(fyers_obj)
        fii_dii_data = FiiDii()
        advances_decline_data = AdvancesDecline()

        dict_data = {
            "UpdateTime": str(datetime.datetime.now()),
            "OptionChainData": option_chain_data,
            "FiiDiiData": fii_dii_data,
            "AdvancesDeclineData": advances_decline_data
        }
        # dayly_stacks.insert_one(dict_data)
        with open(os.path.join(os.getcwd(), "Records", "get_overview.json"), "w") as json_file:
            json.dump(dict_data, json_file, indent=5)
    except Exception as e:
        logging.warning(f"Some thing Wrong in Microscript Daily Stacks at {e}")

    # return dict_data




