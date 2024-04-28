# from Algo.StrategyManager.Manager import StrategyManagerExecution


from Algo.Trader.AutoTrader import run_worker
import asyncio
from Broker.FyersBroker import Fyers
from Broker.TradBuddyBroker import TradBuddyBroker
if __name__ == '__main__':
    # StrategyManagerExecution()\
    fyers_obj = Fyers()
    fyers_obj.authentication()
    tb_obj = TradBuddyBroker()
    run_worker(fyers_obj,tb_obj)


    # Test PlaceOrder
    # from Algo.Trader.PlaceOrderManager import PlaceOrder
    # PlaceOrder('ACC-002', 'strategy_2_status', 'NSE:NIFTYBANK-INDEX', 'PE', 48201,fyers_obj, tb_obj)
