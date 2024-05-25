from Backtesting.get_data_set import Get_Main_DataSet
from Backtesting.Backtest_Statics import Backtest

import pandas as pd
import numpy as np




def StrategyTest(df,index_name,title,initial_balance,sl_points,RiskToReward,ce_condition,pe_condition):
    df["TradSide"] = np.select([ce_condition, pe_condition], ["CE", "PE"], default="None")
    trader = Backtest(index_name,initial_balance ,sl_points,RiskToReward,title)
    trader.backtest(df)
    return {"Statics":trader.stats(),"Trads":trader.trad_book}







def Strategy_1():
    title = "RSI"
    index_name = "BSE:SENSEX-INDEX"
    time_frame = "15" # 15 minutes
    days = 1200 # 1 day data 
    initial_balance = 10000
    sl_points = 100
    RiskToReward = "1:3"
    
    df = Get_Main_DataSet(index_name,time_frame,days)
    ce_condition = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (df["Close"] > df['15EMA'])
                    &(df["Prev_Candle_Signal"] != "Bearish")
                )

    pe_condition = ((df['Low'].shift(1) > df['15EMA'].shift(1)) & (df["Close"] < df['15EMA'])
                    &(df["Prev_Candle_Signal"] != "Bullish")
                )
    
    StrategyTest(df,index_name,title,initial_balance,sl_points,RiskToReward,ce_condition,pe_condition)

