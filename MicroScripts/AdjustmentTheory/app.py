

# ADUJUSTMENT THERY 
# 2 vage pachi jeni expiry hoy e data index ne ley ne har 1 meintes he at the money no CE PE no Price csv ma add karvu

from Utility.TimeSupervisor import market_time_decorator
from Broker.FyersBroker import Fyers
from Utility.OptionSelection import todays_expiry,get_option_for
from Utility.TimeSupervisor import market_time_decorator
import os
import json
from datetime import datetime
import csv


fyerObj = Fyers()
fyerObj.authentication()


def get_symbol(trad_index,trad_side):
    trad_price = fyerObj.get_current_ltp(trad_index)
    print(f"Current LTP for Index {trad_index}: {trad_price}")
    option_data = get_option_for(trad_index,trad_side,trad_price.get(trad_index.split(":")[1]))
    symbol_is = option_data["SYMBOL"]
    index_sp = option_data["STRIKE PRICE"]
    return symbol_is,index_sp

@market_time_decorator(Open_time = "14:50",Close_time = "23:40",market_status="Open",Interval = 10)
def save_expiry_index_price_after_3_pm():
    expiry_indexs = todays_expiry()
    if expiry_indexs is not None:
        with open('MicroScripts/AdjustmentTheory/AdjustmentTheory.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            for exp_index in expiry_indexs:
                symbol_zip= get_symbol(exp_index, "CE")
                ce_symbol = f"{symbol_zip[0][:-2]}CE"
                pe_symbol = f"{symbol_zip[0][:-2]}PE"
                live_prices = fyerObj.get_current_ltp(f"{ce_symbol},{pe_symbol}")
                ce_side_price = live_prices.get(ce_symbol.split(":")[1])
                pe_side_price = live_prices.get(pe_symbol.split(":")[1])
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                index_sp = symbol_zip[1]
                writer.writerow([exp_index,index_sp,ce_symbol, ce_side_price, pe_symbol, pe_side_price, current_time])






