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
    
    ce_condition = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (df["Close"] > df['15EMA'])
                &(df["Prev_Candle_Signal"] != "Bearish")
               )

    pe_condition = ((df['Low'].shift(1) > df['15EMA'].shift(1)) & (df["Close"] < df['15EMA'])
                    &(df["Prev_Candle_Signal"] != "Bullish")
                )

    df['TradSide'] = np.select([ce_condition, pe_condition], ['CE', 'PE'], default='None')
    print("Status EMA CROSSOVER : ",df.iloc[-1]['TradSide'])

    await asyncio.sleep(2)
    return random.choices(["CE", "PE", "None"], weights=[0.15, 0.15, 0.7])[0]



async def strategy_3(df, current_price):
    # INSIDE CANDLE
    
    ce_condition = ((df["2Prev_High"] > df["1Prev_High"]) 
                & (df["2Prev_High"] < df["High"]) 
                & (df["Day_Prev_Candle_Signal"] == "Bullish") 
                & (df["RSI"] <= 80) 
                & (df["Candle_Signal"].shift(1) == "Bullish")
                )

    pe_condition = ((df["2Prev_Low"] < df["1Prev_Low"]) 
                    & (df["2Prev_Low"] > df["Low"]) 
                    & (df["Day_Prev_Candle_Signal"] == "Bearish")
                    & (df["RSI"] >= 20) 
                    & (df["Candle_Signal"].shift(1) == "Bearish")
                    )
    df["Inside_TradSide"] = np.select([ce_condition, pe_condition], ["CE", "PE"], default="None")
    print("Status INSIDE CANDLE : ",df.iloc[-1]['TradSide'])



    await asyncio.sleep(2)
    return random.choices(["CE", "PE", "None"], weights=[0.15, 0.15, 0.7])[0]




async def strategy_4(df, current_price):
    # BOTH INSIDE AND EMA
    ce_condition = ((df["2Prev_High"] > df["1Prev_High"]) 
                & (df["2Prev_High"] < df["High"]) 
                & (df["Day_Prev_Candle_Signal"] == "Bullish") 
                & (df["RSI"] <= 80) 
                & (df["Candle_Signal"].shift(1) == "Bullish")
                )

    pe_condition = ((df["2Prev_Low"] < df["1Prev_Low"]) 
                    & (df["2Prev_Low"] > df["Low"]) 
                    & (df["Day_Prev_Candle_Signal"] == "Bearish")
                    & (df["RSI"] >= 20) 
                    & (df["Candle_Signal"].shift(1) == "Bearish")
                    )
    df["Inside_TradSide"] = np.select([ce_condition, pe_condition], ["CE", "PE"], default="None")

    ce_condition = ((df['High'].shift(1) < df['15EMA'].shift(1)) & (df["Close"] > df['15EMA'])
                &(df["Prev_Candle_Signal"] != "Bearish")
               )

    pe_condition = ((df['Low'].shift(1) > df['15EMA'].shift(1)) & (df["Close"] < df['15EMA'])
                    &(df["Prev_Candle_Signal"] != "Bullish")
                )

    df['TradSide_EMA'] = np.select([ce_condition, pe_condition], ['CE', 'PE'], default='None')


    ce_condition = (df['TradSide_EMA'] == "CE") | (df["Inside_TradSide"] == "CE")
    pe_condition = (df['TradSide_EMA'] == "PE") | (df["Inside_TradSide"] == "PE")
    df['TradSide'] = np.select([ce_condition, pe_condition], ['CE', 'PE'], default='None')
    print("Status BOTH INSIDE AND EMAR : ",df.iloc[-1]['TradSide'])


    await asyncio.sleep(2)
    return random.choices(["CE", "PE", "None"], weights=[0.15, 0.15, 0.7])[0]


