import os
from Utility.OptionSelection import get_option_for

import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def PlaceOrder(account, strategy_name, trad_index, trad_side,trad_price,Fyers,TradBuddy):
    # FIND OPTION DETAILS-------------------

    get_option_details = get_option_for(trad_index,trad_side,trad_price)
    if get_option_details == None:
        logging.info("Option Details Not found")
        return

    option_symbol = get_option_details["SYMBOL"]
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




    account_id = account["account_id"]
    base_sl =account["base_stoploss"]
    base_tg = account["base_target"]
    todays_trad_margin = account["todays_trad_margin"]


    quantity, current_option_sl ,current_option_tg = TradBuddy.price=current_option_price(trad_amount=todays_trad_margin,
                                                                            quantity_per_lot=option_lot,
                                                                            price=current_option_price,
                                                                            rr =  base_sl/base_tg )

    
    # FIND SL - TARGET -------------------
    # index_sl,index_tg = 20,40
    # Dynamic karvanu chhe ke jab Nifty rey to SL nallu ne Qunity vadhare | Banknifty rey to SL motu ne quanity osi
    # current_option_sl, current_option_tg = [current_option_price * (100 - base_sl) / 100, current_option_price * (100 + base_tg) / 100]


    order_place_status = TradBuddy.order_place(
        account_id = account_id,
        strategy = strategy_name,
        trad_index = trad_index,
        trad_side = trad_side,
        trigger_price = current_index_price,
        option_symbol = option_symbol,
        qnty = quantity,
        buyprice = current_option_price,
        sl_price = current_option_sl,
        target_price = current_option_tg,
        notes = "Test"        
    )
    logging.info(f" Order Placed : {option_symbol}| QTY:[{buy_qty}]-{account_id}-{strategy_name}")
    
    
