import asyncio
import os
import json
import schedule
from datetime import datetime
import time
import logging

from Algo.Trader.PlaceOrderManager import PlaceOrder

logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Strategy_path = f"{os.getcwd()}/Records/strategies_results.json"




# PLACE ORDER
async def process_order_place(account,Fyers,TradBuddy):

    with open(Strategy_path, 'r') as file:
        if file.read().strip() == "":
            logging.info("No Found Strategy JSON file.")
            return
        else:
            file.seek(0)
            strategies_results = json.load(file)
        try:
            account_number = account["account_id"]
            tasks = []
            print(account["strategy"],"strategy")
            for strategy_key in account["strategy"]:
                for symbol in account["strategy"][strategy_key]:
                    status = strategies_results.get(symbol, {}).get(strategy_key,"None")
                    price = strategies_results.get(symbol, {}).get("price")
                    is_already = TradBuddy.order_get({"trad_index": symbol, "trad_side": status, "trad_status": "Open"})
                    if status != "None" and len(is_already) <= 0 :
                        print(f"+----------------Buy[{symbol}]------------------+")
                        tasks.append(PlaceOrder(account_number, strategy_key, symbol, status,price,Fyers,TradBuddy))
            await asyncio.gather(*tasks)
        except Exception as e:
            logging.error(f"Error in [process_order_place] : {e}")


# CANCEL ORDER 
async def process_order_cancel(trad,all_price,Fyers,TradBuddy):
    live_price = max(all_price[trad["option_symbol"].split(":")[1]],0.1)
    # live_price = 0.1
    order_id = trad.get("order_id")
    account_id = trad.get("account_id")

    account = TradBuddy.account_get(account_id)

    try:
        if trad['target_price'] <= live_price :
            if account["body"]["trailing_status"] == "Activate":
                logging.info(f"TARGET TRAIL for : {order_id}")
                trailing_count = trad.get("trailing_count")

                trailed_sl_pr = account.get("trailing_stoploss",5)
                trailed_tg_pr = account.get("trailing_target",10)
                current_trailed_sl, current_trailed_tg = [live_price * (100 - trailed_sl_pr) / 100, live_price * (100 + trailed_tg_pr) / 100]


                update_query ={
                    "stoploss_price" : current_trailed_sl,
                    "target_price":current_trailed_tg,
                    "trailing_count" : trailing_count + 1
                }
                trail_status = TradBuddy.order_update(order_id,update_query)
                logging.info(trail_status)
                return 
            else:
                logging.info(f"TARGET HIT for : {order_id}")
                close_status = TradBuddy.order_close(account_id,order_id,live_price)
                logging.info(close_status)
                return

        if trad['stoploss_price'] >= live_price:
            logging.info(f"STOPLOSS HIT for : {order_id}")
            close_status = TradBuddy.order_close(account_id,order_id,live_price)
            print(close_status)
            return
    except Exception as e:
        logging.error(f"Error in [process_order_cancel] : {e}")


async def worker(Fyers,TradBuddy):
    try:
        # ORDER PLACE ----------------------------
        accounts = TradBuddy.account_list({"is_activate":"Activate"})
        await asyncio.gather(*(process_order_place(account,Fyers,TradBuddy) for account in accounts))

        # ORDER CANCEL ----------------------------
        open_trads = TradBuddy.order_opens()
        logging.info(f"OPEN TRADS:{len(open_trads)}")
        if len(open_trads) == 0 :
            return
        open_order_symbols =','.join({ i["option_symbol"] for i in  open_trads})
        open_order_live_price = Fyers.get_current_ltp(open_order_symbols)
        logging.info(f"Open Orders Live Price :{open_order_live_price}")
        if "Unknown" not in open_order_live_price :
            await asyncio.gather(*(process_order_cancel(trads,open_order_live_price,Fyers,TradBuddy) for trads in open_trads))
    except Exception as e:
        logging.error(f"Error in [Worker] : {e}")


from Utility.TimeSupervisor import market_time_decorator
@market_time_decorator(Open_time = "9:15",Close_time = "15:15",market_status="Open",Interval = 60)
def run_worker(Fyers,TradBuddy):
    asyncio.run(worker(Fyers,TradBuddy))

