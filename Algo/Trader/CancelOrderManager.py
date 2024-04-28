




# {'_id': ObjectId('662d4cd1d358320fae6a7543'), 'order_id': 'ORD-1714244817675834626', 'account_id': 'ACC-003', 'strategy': 'strategy_2_status', 'date': '28-04-2024', 'trad_status': 'Open', 'trad_type': 'Buy', 'trad_index': 'NSE:NIFTYBANK-INDEX', 'trad_side': 'PE', 'trigger_price': 48201.05, 'option_symbol': 'NSE:BANKNIFTY2443048200PE', 'qnty': 15, 'buy_price': 220, 'sell_price': None, 'stoploss_price': 176.0, 'target_price': 308.0, 'buy_datetime': datetime.datetime(2024, 4, 28, 0, 36, 57, 675000), 'sell_datetime': None, 'buy_margin': 3300, 'sell_margin': None, 'pnl_status': None, 'pnl': None, 'notes': 'Test'}
async def CancelOrder(order,Fyers,TradBuddy):
    print(order)
    # order_place_status = TradBuddy.order_place(
    #     # account_id = account_id,
    #     # strategy = strategy_name,
    #     # trad_index = trad_index,
    #     # trad_side = trad_side,
    #     # trigger_price = current_index_price,
    #     # option_symbol = option_symbol,
    #     # qnty = option_lot*genral_mux,
    #     # buyprice = current_option_price,
    #     # sl_price = current_option_sl,
    #     # target_price = current_option_tg,
    #     # notes = "Test"        
    # )
    # print(order_place_status)
    