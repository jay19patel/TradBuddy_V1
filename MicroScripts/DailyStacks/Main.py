from MicroScripts.DailyStacks.FetchData import OptionChain,FiiDii,AdvancesDecline
from Utility.TimeSupervisor import market_time_decorator

import json
import os
# @market_time_decorator(Open_time = "9:15",Close_time = "23:15",market_status="Open",Interval = 60)
def get_overview(fyers_obj):
    option_chain_data = OptionChain(fyers_obj)
    fii_dii_data = FiiDii()
    advances_decline_data = AdvancesDecline()

    dict_data = {
        "OptionChainData": option_chain_data,
        "FiiDiiData": fii_dii_data,
        "AdvancesDeclineData": advances_decline_data
    }

    with open(os.path.join(os.getcwd(), "Records", "get_overview.json"), "w") as json_file:
        json.dump(dict_data, json_file, indent=4)

    # return dict_data
