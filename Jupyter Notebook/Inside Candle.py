ce_condition = ((df["2Prev_High"] > df["1Prev_High"]) 
                & (df["2Prev_High"] < df["High"]) 
                & (df["Day_Prev_Candle_Signal"] == "Bullish") 
                & (df["Day_SuperTrend"] == 1) 
                & (df["Candle_Signal"].shift(1) == "Bullish")
                )

pe_condition = ((df["2Prev_Low"] < df["1Prev_Low"]) 
                & (df["2Prev_Low"] > df["Low"]) 
                & (df["Day_Prev_Candle_Signal"] == "Bearish")
                & (df["Day_SuperTrend"] == -1) 
                & (df["Candle_Signal"].shift(1) == "Bearish")
                )




trader = Trader(initial_balance = 100000,sl_points = 100,RiskToReward = "1:2")
trader.backtest(df)
trader.stats()
