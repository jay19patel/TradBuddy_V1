from Algo.StrategyManager.Manager import StrategyManagerExecution
from Broker.FyersBroker import Fyers
from Broker.TradBuddyBroker import TradBuddyBroker





if __name__ == '__main__':
    fyers_obj = Fyers()
    fyers_obj.authentication()
    tb_obj = TradBuddyBroker()
    StrategyManagerExecution(fyers_obj)
