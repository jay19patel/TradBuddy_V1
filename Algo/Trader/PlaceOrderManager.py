import os
from Utility.OptionSelection import get_option_for

import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def PlaceOrder(account, strategy_name, trad_index, trad_side,trad_price,Fyers,TradBuddy):
    # FIND OPTION DETAILS-------------------

    account_id = account["account_id"]
    index_sl =account["base_stoploss"]
    index_tg = account["base_target"]




    get_option_details = get_option_for(trad_index,trad_side,trad_price)
    if get_option_details == None:
        logging.info("Option Details Not found")
        return

    option_symbol = get_option_details["SYMBOL"]
    genral_mux = 1
    option_lot = get_option_details["LOT"]
    option_expiry = get_option_details["EXDATETIME"]
    option_id = get_option_details["ID"]


    
    # GET LIVE MARKET DATA -------------------
    get_live_data = Fyers.get_current_ltp(f"{trad_index},{option_symbol}")
    if  "Unknown" in get_live_data:
        logging.info(f"Live Data Not found for index :{trad_index},{option_symbol}")
        return 
    # {'NIFTYBANK-INDEX': 48201.05, 'BANKNIFTY2443048200PE': 220}
    ((current_index_name, current_index_price), (current_option_name, current_option_price)) = tuple(zip(get_live_data.keys(),get_live_data.values()))



    # FIND SL - TARGET -------------------
    # index_sl,index_tg = 20,40
    current_option_sl, current_option_tg = [current_option_price * (100 - index_sl) / 100, current_option_price * (100 + index_tg) / 100]


    order_place_status = TradBuddy.order_place(
        account_id = account_id,
        strategy = strategy_name,
        trad_index = trad_index,
        trad_side = trad_side,
        trigger_price = current_index_price,
        option_symbol = option_symbol,
        qnty = option_lot*genral_mux,
        buyprice = current_option_price,
        sl_price = current_option_sl,
        target_price = current_option_tg,
        notes = "Test"        
    )
    logging.info(f" Order Placed : {option_symbol}-{account_id}-{strategy_name}")
    
    
