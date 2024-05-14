from Broker.FyersBroker import Fyers
import pandas as pd
import pandas as pd
from ta.trend import EMAIndicator
import pandas_ta as pdta
import ta
import numpy as np


fyers_obj = Fyers()
fyers_obj.authentication()

temp = None
MaxList = list()
MinList = list()
def FindMinMax(row):
    global temp,MinList,MaxList
    if temp!= None :
        if row["SuperTrend"] == 1 and temp == 1:
            MaxList.append(row["High"])
        elif row["SuperTrend"] == -1 and temp == -1:
            MinList.append(row["Low"])
            
        elif row["SuperTrend"] == -1 and temp == 1:
            MinList.clear()
            MinList.append(row["Low"])
            temp = row["SuperTrend"]
            
        elif row["SuperTrend"] == 1 and temp == -1:
            MaxList.clear()
            MaxList.append(row["High"])
            temp = row["SuperTrend"]

        return min(MinList),max(MaxList)
            
    else:
        temp = row["SuperTrend"]
        MaxList.append(row["High"])
        MinList.append(row["Low"])
    
    return min(MinList),max(MaxList)

def Get_Main_DataSet():
    index_name = "BSE:SENSEX-INDEX"
    time_frame = "15" # 15 minutes
    days = 1200 # 1 day data 
    df = fyers_obj.Big_Historical_Data(index_name,time_frame,days)
    df_day = fyers_obj.Big_Historical_Data(index_name,"1D",days)

    df.drop(columns=['Volume'], inplace=True)
    df_day.drop(columns=['Volume'], inplace=True)

    super_trend = pdta.supertrend(high=df_day['High'], low=df_day['Low'], close=df_day['Close'], length=50, multiplier=4)

    df_day['SuperTrend'] = super_trend['SUPERTd_50_4.0']
    df_day['Candle'] = df_day.apply(lambda row: 'Green' if row['Close'] >= row['Open'] else 'Red', axis=1)
    df_day['CandleBody'] = abs(df_day['High'] - df_day['Low'])
    df_day['5EMA'] = EMAIndicator(close=df_day['Close'], window=5, fillna=False).ema_indicator()
    df_day['15EMA'] = EMAIndicator(close=df_day['Close'], window=15, fillna=False).ema_indicator()
    df_day['20EMA'] = EMAIndicator(close=df_day['Close'], window=20, fillna=False).ema_indicator()
    df_day['50EMA'] = EMAIndicator(close=df_day['Close'], window=50, fillna=False).ema_indicator()
    df_day['200EMA'] = EMAIndicator(close=df_day['Close'], window=200, fillna=False).ema_indicator()
    df_day['RSI'] = ta.momentum.RSIIndicator(df_day['Close'],window=6).rsi()

    # SHADOW FIND 
    df_day["upper_shadow"] = df_day['High'] - df_day[['Close', 'Open']].max(axis=1)
    df_day["lower_shadow"] = df_day[['Close', 'Open']].min(axis=1) - df_day['Low']
    df_day["total_shadow"] = df_day["upper_shadow"] + df_day["lower_shadow"]

    # Calculate percentage of upper and lower shadows
    df_day["upper_shadow_pr"] = (df_day["upper_shadow"] / df_day["total_shadow"] )*100
    df_day["lower_shadow_pr"] = (df_day["lower_shadow"] / df_day["total_shadow"])*100

    conditions = [
        np.logical_and(df_day["upper_shadow_pr"] <= 30, df_day["lower_shadow_pr"] >= 70),
        np.logical_and(df_day["upper_shadow_pr"] >= 70, df_day["lower_shadow_pr"] <= 30)
    ]

    choices = ["Bullish", "Bearish"]
    df_day['Candle_Signal'] = np.select(conditions, choices, default="Neutral")

    # Previes Day Data

    df_day['Prev_Candle_Signal'] =df_day['Candle_Signal'].shift(1)
    df_day['Prev_Candle'] = df_day['Candle'].shift(1)

    df_day.drop(['total_shadow','upper_shadow','lower_shadow'], axis=1, inplace=True)




    df_day['Datetime'] = pd.to_datetime(df_day['Datetime'])
    df_day['Date'] = df_day['Datetime'].dt.date
    df_day[['SwingMin', 'SwingMax']] = df_day.apply(FindMinMax, axis=1, result_type='expand')
    df_day = df_day.add_prefix('Day_')




    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Day_Date'] = df['Datetime'].dt.date
    first_candle_high = df.groupby('Day_Date')['High'].first()
    first_candle_low = df.groupby('Day_Date')['Low'].first()
    df['First_Candle_High'] = df['Day_Date'].map(first_candle_high)
    df['First_Candle_Low'] = df['Day_Date'].map(first_candle_low)


    df['Pivot'] = df[["High", "Low", "Close"]].mean(axis=1)
    df['Candle'] = df.apply(lambda row: 'Green' if row['Close'] >= row['Open'] else 'Red', axis=1)
    df['CandleBody'] = abs(df['High'] - df['Low'])
    df['5EMA'] = EMAIndicator(close=df['Close'], window=5, fillna=False).ema_indicator()
    df['15EMA'] = EMAIndicator(close=df['Close'], window=15, fillna=False).ema_indicator()
    df['20EMA'] = EMAIndicator(close=df['Close'], window=20, fillna=False).ema_indicator()
    df['50EMA'] = EMAIndicator(close=df['Close'], window=50, fillna=False).ema_indicator()
    df['200EMA'] = EMAIndicator(close=df['Close'], window=200, fillna=False).ema_indicator()
    df['RSI'] = ta.momentum.RSIIndicator(df['Close'],window=6).rsi()
    super_trend = pdta.supertrend(high=df['High'], low=df['Low'], close=df['Close'], length=50, multiplier=4)
    df['SuperTrend'] = super_trend['SUPERTd_50_4.0']

        # SHADOW FIND 
    df_upper_shadow = df['High'] - df[['Close', 'Open']].max(axis=1)
    df_lower_shadow = df[['Close', 'Open']].min(axis=1) - df['Low']
    total_range = df_upper_shadow + df_lower_shadow

    # Calculate percentage of upper and lower shadows
    df["upper_shadow_pr"] = (df_upper_shadow / total_range )*100
    df["lower_shadow_pr"] = (df_lower_shadow / total_range)*100

    conditions = [
        np.logical_and(df["upper_shadow_pr"] <= 30, df["lower_shadow_pr"] >= 70) ,
        np.logical_and(df["upper_shadow_pr"] >= 70, df["lower_shadow_pr"] <= 30)
    ]

    choices = ["Bullish", "Bearish"]
    df['Candle_Signal'] = np.select(conditions, choices, default="Neutral")


    df.dropna(inplace=True)
    df[["Small_Swing_Min","Small_Swing_Max"]]=df.apply(FindMinMax, axis=1, result_type='expand')

    
    merged_df = df_day.merge(df, on='Day_Date', how='inner')
    merged_df.dropna(inplace=True)
    merged_df.drop(['Day_Datetime'], axis=1, inplace=True)
    merged_df.to_csv("Jupyter Notebook/Sensex15.csv",index=False)
    print("Backtesing Data Save.")
    # return merged_df


Get_Main_DataSet()


# df["Status"] = (df['Pivot'] - df['Pivot'].shift(5) >= 60).shift(-6)