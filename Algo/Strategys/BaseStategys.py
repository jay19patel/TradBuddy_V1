import random
import time
import asyncio
import numpy as np
import pandas as pd
async def strategy_1(df, current_price):
    # Dummmy Random Trad for Testing
    await asyncio.sleep(2)
    return random.choices(["CE", "PE", "None"], weights=[0.15, 0.15, 0.7])[0]

async def strategy_2(df, current_price):
    # EMA CORSSOVER
    ce_condition = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (current_price > df['15EMA'])
               )
    pe_condition = ((df['Low'].shift(1) > df['5EMA'].shift(1)) & (current_price < df['5EMA'])
                )
    df['TradSide'] = np.select([ce_condition, pe_condition], ['CE', 'PE'], default='None')
    
    TradSide_Status = df.iloc[-1]['TradSide']
    print("Status EMA CANDLE : ",TradSide_Status)
    return TradSide_Status



async def strategy_3(df, current_price):
    # INSIDE CANDLE
    
    ce_condition = ((df["2Prev_High"] > df["1Prev_High"]) 
                & (df["2Prev_High"] < current_price) 
                & (df["Day_Prev_Candle_Signal"] == "Bullish") 
                )

    pe_condition = ((df["2Prev_Low"] < df["1Prev_Low"]) 
                    & (df["2Prev_Low"] >current_price) 
                    & (df["Day_Prev_Candle_Signal"] == "Bearish")
                    )
    df["TradSide"] = np.select([ce_condition, pe_condition], ["CE", "PE"], default="None")
    TradSide_Status = df.iloc[-1]['TradSide']
    print("Status INSIDE CANDLE : ",TradSide_Status)
    return TradSide_Status



async def strategy_4(df, current_price):
    # # BOTH INSIDE AND EMA
    ce_condition_inside = ((df["2Prev_High"] > df["1Prev_High"]) 
                & (df["2Prev_High"] < current_price) 
                & (df["Day_Prev_Candle_Signal"] == "Bullish") 
                )

    pe_condition_inside = ((df["2Prev_Low"] < df["1Prev_Low"]) 
                    & (df["2Prev_Low"] >current_price) 
                    & (df["Day_Prev_Candle_Signal"] == "Bearish")
                    )
    df["Inside_TradSide"] = np.select([ce_condition_inside, pe_condition_inside], ["CE", "PE"], default="None")

    ce_condition_ema = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (current_price > df['15EMA'])
               )

    pe_condition_ema = ((df['Low'].shift(1) > df['15EMA'].shift(1)) & (current_price < df['15EMA'])
                )

    df['TradSide_EMA'] = np.select([ce_condition_ema, pe_condition_ema], ['CE', 'PE'], default='None')


    ce_condition = (df['TradSide_EMA'] == "CE") | (df["Inside_TradSide"] == "CE")
    pe_condition = (df['TradSide_EMA'] == "PE") | (df["Inside_TradSide"] == "PE")
    df['TradSide'] = np.select([ce_condition, pe_condition], ['CE', 'PE'], default='None')
    TradSide_Status = df.iloc[-1]['TradSide']
    print("Status INSIDE + EMA CANDLE : ",TradSide_Status)

    return TradSide_Status


