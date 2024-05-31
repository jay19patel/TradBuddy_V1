from Algo.StrategyManager.Manager import StrategyManagerExecution
from Algo.Trader.AutoTrader import run_worker
from Broker.FyersBroker import Fyers
from Broker.TradBuddyBroker import TradBuddyBroker
import threading
import schedule
import time
from MicroScripts.DailyStacks.Main import get_overview


if __name__ == '__main__':
    fyers_obj = Fyers()
    fyers_obj.authentication()
    tb_obj = TradBuddyBroker()

    try:
        thread1 = threading.Thread(target=StrategyManagerExecution, args=(fyers_obj,))
        thread2 = threading.Thread(target=run_worker, args=(fyers_obj, tb_obj))
        # thread3 = threading.Thread(target=get_overview, args=(fyers_obj.fyers_instance,))

        thread1.start()
        thread2.start()
        # thread3.start()

        thread1.join()
        thread2.join()
        # thread3.join()
    except Exception as e:
        print("Error in Main Execution:", e)

    while True:
        schedule.run_pending()
        time.sleep(1)
