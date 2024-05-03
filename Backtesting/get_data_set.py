
from Broker.FyersBroker import Fyers

fyers_obj = Fyers()
fyers_obj.authentication()


row_data = fyers_obj.Big_Historical_Data("NSE:NIFTY50-INDEX",15,1)

print(row_data)
