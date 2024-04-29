import asyncio
import os
import json
import schedule
from datetime import datetime
import time


from Algo.Trader.PlaceOrderManager import PlaceOrder

Strategy_path = f"{os.getcwd()}/Records/strategies_results.json"


def time_set_for_next_day():
    schedule.clear()
    schedule.every().day.at("09:15").do(worker)
    print("Market schedule set for the next day")

# PLACE ORDER
async def process_order_place(account,Fyers,TradBuddy):
    print("ORDER PLACE PROCESS EXECUTE")

    with open(Strategy_path, 'r') as file:
        if file.read().strip() == "":
            print("NO JSON")
            return
        else:
            file.seek(0)
            strategies_results = json.load(file)


        account_number = account["account_id"]
        tasks = []
        for symbol, strategy_key in account["strategys"]:
            status = strategies_results.get(symbol, {}).get(strategy_key)
            price = strategies_results.get(symbol, {}).get("price")
            is_already = TradBuddy.order_get({"trad_index": symbol, "trad_side": status, "trad_status": "Open"})
            if status != "None" and len(is_already) >= 0:
                tasks.append(PlaceOrder(account_number, strategy_key, symbol, status,price,Fyers,TradBuddy))
        await asyncio.gather(*tasks)


# CANCEL ORDER 
async def process_order_cancel(trad,all_price,Fyers,TradBuddy):
    print("ORDER EXIT PROCESS EXECUTE")
    # trads = {'_id': ObjectId('662de513395e5149ad279c76'), 'order_id': 'ORD-1714283795535873810', 
    #  'account_id': 'ACC-003', 'strategy': 'strategy_1_status', 'date': '28-04-2024', 'trad_status': 'Open',
    #    'trad_type': 'Buy', 'trad_index': 'NSE:NIFTY50-INDEX', 'trad_side': 'CE', 'trigger_price': 22419.95, 
    #    'option_symbol': 'NSE:NIFTY2450222400CE', 'qnty': 25, 'buy_price': 187.5, 'sell_price': None, 
    #    'stoploss_price': 150.0, 'target_price': 262.5, 'buy_datetime': datetime.datetime(2024, 4, 28, 11, 26, 35, 535000),
    #      'sell_datetime': None, 'buy_margin': 4687.5, 'sell_margin': None, 'pnl_status': None, 'pnl': None, 'notes': 'Test'}
    # live = {'NIFTY2450222400CE': 187.5, 'BANKNIFTY2443048200CE': 362.3}
    
    # live_price = min(all_price[trad["option_symbol"].split(":")[1]],0.1)
    live_price = 0.1
    order_id = trad.get("order_id")
    account_id = trad.get("account_id")

    print(account_id,order_id)
    account = TradBuddy.account_get(account_id)


    if trad['target_price'] <= live_price :
        if account["body"]["trailing_status"] == "Activate":
            print("TARGET TRAIL")
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
            print(trail_status)
            return 
        else:
            print("TARGET HIT")
            close_status = TradBuddy.order_close(account_id,order_id,live_price)
            print(close_status)
            return

    if trad['stoploss_price'] >= live_price:
        print("STOPLOSS HIT")
        close_status = TradBuddy.order_close(account_id,order_id,live_price)
        print(close_status)
        return
    print("SKIP")
            
    

async def worker(Fyers,TradBuddy):
    
    # ORDER PLACE ----------------------------
    accounts = TradBuddy.account_list({"is_activate":"Activate"})
    await asyncio.gather(*(process_order_place(account,Fyers,TradBuddy) for account in accounts))

    # ORDER CANCEL ----------------------------
    open_trads = TradBuddy.order_opens()
    print("OPEN TRADS :",len(open_trads))
    if len(open_trads) == 0 :
        return
    open_order_symbols =','.join({ i["option_symbol"] for i in  open_trads})
    open_order_live_price = Fyers.get_current_ltp(open_order_symbols)
    print(open_order_symbols)
    print(open_order_live_price)
    if "Unknown" not in open_order_live_price :
        await asyncio.gather(*(process_order_cancel(trads,open_order_live_price,Fyers,TradBuddy) for trads in open_trads))


# TEST RUN---------------------------
# def run_worker(Fyers,TradBuddy):
#     asyncio.run(worker(Fyers,TradBuddy))
#     while True:
#         schedule.run_pending()
#         time.sleep(1)



# MAIN RUN---------------------------
def run_worker(Fyers,TradBuddy):
    current_time = datetime.now().time()
    market_status = "Open"  
    if market_status == "Open":
        print("Algorithm is Online")
        # schedule.every(1).minutes.do(lambda: time_set_for_next_day() if current_time > datetime.strptime("15:15", "%H:%M").time() else asyncio.run(worker(Fyers,TradBuddy)))
        schedule.every(10).seconds.do(lambda: asyncio.run(worker(Fyers,TradBuddy)))
        # asyncio.run(worker(Fyers,TradBuddy))
    else:
        print("Market is closed")

    while True:
        schedule.run_pending()
        time.sleep(1)

