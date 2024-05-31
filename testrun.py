
from Broker.FyersBroker import Fyers

from MicroScripts.DailyStacks.Main import get_overview


fyers_obj = Fyers()
fyers_obj.authentication()



get_overview(fyers_obj.fyers_instance)


# fyers_obj



