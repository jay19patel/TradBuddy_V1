from Algo.StrategyManager.Manager import StrategyManagerExecution
from Algo.Trader.AutoTrader import run_worker
from Broker.FyersBroker import Fyers
from Broker.TradBuddyBroker import TradBuddyBroker
import threading
import schedule
import time

if __name__ == '__main__':
    fyers_obj = Fyers()
    fyers_obj.authentication()
    tb_obj = TradBuddyBroker()
    StrategyManagerExecution(fyers_obj)
    # thread1 = threading.Thread(target=StrategyManagerExecution, args=(fyers_obj,))
    # thread2 = threading.Thread(target=run_worker, args=(fyers_obj, tb_obj))

    # thread1.start()
    # thread2.start()

    # Wait for both threads to finish
    # thread1.join()
    # thread2.join()


    while True:
        schedule.run_pending()
        time.sleep(1)



# if __name__ == '__main__':
#     fyers_obj = Fyers()
#     fyers_obj.authentication()
#     tb_obj = TradBuddyBroker()
#     StrategyManagerExecution(fyers_obj,)
