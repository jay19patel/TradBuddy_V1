import os
from Utility.OptionSelection import get_option_for,todays_expiry

import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_index_sortname(option_symbol):
    index_mapping = {
        "NSE:NIFTY50-INDEX": "NIFTY",
        "NSE:NIFTYBANK-INDEX":"BANKNIFTY",
        "NSE:FINNIFTY-INDEX": "FINNIFTY",
        "BSE:BANKEX-INDEX": "BANKEX",
        "BSE:SENSEX-INDEX": "SENSEX"
    }
    return index_mapping.get(option_symbol)


async def PlaceOrder(account_id, strategy_name, trad_index, trad_side,trad_price,Fyers,TradBuddy):
    # print(account_id, strategy_name, trad_index, trad_side,trad_price,Fyers,TradBuddy)

    todays_expiry()
    # # FIND OPTION DETAILS-------------------
    # print(get_index_sortname(trad_index),trad_side,trad_price)
    # get_option_details = get_option_for(get_index_sortname(trad_index),trad_side,trad_price)
    # # {'ID': 101124043049532, 'INDEX INFO': 'BANKNIFTY 24 Apr 30 48200 PE', 'LOT': 15, 
    # #  'TIMESTAMP': 1714471200, 'SYMBOL': 'NSE:BANKNIFTY2443048200PE', 'INDEX': 'BANKNIFTY', 
    # #  'STRIKE PRICE': 48200.0, 'SIDE': 'PE', 'EXDATETIME': ('2024-04-30 10:00:00')}

    # if get_option_details == None:
    #     logging.info("Option Details Not found")
    #     return

    # option_symbol = get_option_details["SYMBOL"]
    # genral_mux = 1
    # option_lot = get_option_details["LOT"]
    # option_expiry = get_option_details["EXDATETIME"]
    # option_id = get_option_details["ID"]

    
    # # GET LIVE MARKET DATA -------------------
    # get_live_data = Fyers.get_current_ltp(f"{trad_index},{option_symbol}")
    # if  "Unknown" in get_live_data:
    #     logging.info(f"Live Data Not found for index :{trad_index},{option_symbol}")
    #     return 
    # # {'NIFTYBANK-INDEX': 48201.05, 'BANKNIFTY2443048200PE': 220}
    # ((current_index_name, current_index_price), (current_option_name, current_option_price)) = tuple(zip(get_live_data.keys(),get_live_data.values()))



    # # FIND SL - TARGET -------------------
    # index_sl,index_tg = 20,40
    # current_option_sl, current_option_tg = [current_option_price * (100 - index_sl) / 100, current_option_price * (100 + index_tg) / 100]


    # order_place_status = TradBuddy.order_place(
    #     account_id = account_id,
    #     strategy = strategy_name,
    #     trad_index = trad_index,
    #     trad_side = trad_side,
    #     trigger_price = current_index_price,
    #     option_symbol = option_symbol,
    #     qnty = option_lot*genral_mux,
    #     buyprice = current_option_price,
    #     sl_price = current_option_sl,
    #     target_price = current_option_tg,
    #     notes = "Test"        
    # )
    # logging.info(f" Order Placed : {order_place_status}")
    
    
