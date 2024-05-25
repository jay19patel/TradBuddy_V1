import pandas as pd
from tabulate import tabulate
class Backtest:
    def __init__(self,initial_balance,sl_points,RiskToReward,index_name,title):
        self.balance = initial_balance
        self.RiskToReward  = RiskToReward
        self.sl_points = sl_points
        self.index_name = index_name
        self.title = title
        self.trad_book = pd.DataFrame(columns=['IndexName', 'TradSide', 'Status', 'Quantity', 'BuyPrice',
                                               'BuyDatetime', 'SellPrice', 'SellDatetime','SLValue',
                                               'TargetValue', 'PnL Status','PnL'])
        

    def backtest(self, df):
        open_order = None
        TradSide = None
        tg_order = None
        sl_order = None

        for index, row in df.iterrows():
            if row["TradSide"] != "None" and open_order is None:
                open_order = row["Close"]
                TradSide = row["TradSide"]
                sl = self.sl_points * int(self.RiskToReward.split(":")[0])
                tg = sl * int(self.RiskToReward.split(":")[1])
                sl_order, tg_order = (open_order - sl, open_order + tg) if TradSide == "CE" else (open_order + sl, open_order - tg)
                symbol =  self.index_name
                quantity = 10
                new_log = pd.DataFrame({'IndexName': [symbol],'TradSide':[TradSide],'Status':["Open"] ,'Quantity': [quantity], 'BuyPrice': [open_order],
                                'BuyDatetime': [row["Datetime"]], 'SellDatetime': [None], 'SellPrice': [None],
                                'PnL': [0],'SLValue': [sl_order], 'TargetValue': [tg_order], 'PnL Status': [None] })
                self.trad_book = pd.concat([self.trad_book, new_log], ignore_index=True)
            if open_order is not None:
                if (TradSide == "CE" and (row["Close"] >= tg_order or row["Close"] <= sl_order)) or \
                   (TradSide == "PE" and (row["Close"] <= tg_order or row["Close"] >= sl_order)):
                    pnl = row["Close"] - open_order if TradSide == "CE" else open_order - row["Close"]
                    self.balance += pnl
                    
                    index = self.trad_book.shape[0] -1
                    self.trad_book.at[index, 'SellPrice'] = row["Close"]
                    self.trad_book.at[index, 'SellDatetime'] = row["Datetime"]
                    self.trad_book.at[index, 'Status'] = "Done"
                    self.trad_book.at[index, 'PnL'] = pnl
                    self.trad_book.at[index, 'PnL Status'] = "Profit" if  pnl >0  else "Loss"
                    self.trad_book.at[index, 'SellDatetime'] = row["Datetime"]
                    open_order = None

    
    def stats(self):
            df = self.trad_book
            total_trade = len(df.index)
            pnl = df.PnL.sum()
            winners = len(df[df.PnL > 0])
            losers = len(df[df.PnL <= 0])
            win_ratio = round((winners / total_trade) * 100, 2)
    
            # Calculate CE and PE trades
        
            ce_trades = f"{(len(df[(df['TradSide'] == 'CE') & (df['PnL'] > 0)]) / len(df[df['TradSide'] == 'CE']) * 100):.2f}%" if len(df[df['TradSide'] == 'CE']) != 0 else 0
            pe_trades = f"{(len(df[(df['TradSide'] == 'PE') & (df['PnL'] > 0)]) / len(df[df['TradSide'] == 'PE']) * 100):.2f}%" if len(df[df['TradSide'] == 'PE']) != 0 else 0

    
            # Calculate additional metrics
            capital = self.balance
            max_win = round(df[df.PnL > 0].PnL.max(), 2) if winners > 0 else 0
            max_profit_sum = round(df[df.PnL > 0].PnL.sum(), 2) if winners > 0 else 0
            max_loss = round(df[df.PnL <= 0].PnL.min(), 2) if losers > 0 else 0
            max_loss_sum = round(df[df.PnL <= 0].PnL.sum(), 2) if losers > 0 else 0
            total_profit = round(df.PnL.sum(), 2)
            total_profit_percentage = round((total_profit / self.balance) * 100, 2)
            trading_days = pd.to_datetime(df['BuyDatetime']).dt.strftime('%Y%m%d').nunique()


            parameters = ['Total Trading Days','Total Trades','RiskToReward','Base SL','Capital', 'Total Wins', 'Total Losses', 'Win Ratio','Total Profit', 'Grow Profit %',
                              'Max Win', 'Max Win Score','Max Loss', 'Max Loss Score','CE Trades', 'PE Trades', 'Stategy Name']


        
            data_points = [trading_days,total_trade, self.RiskToReward ,self.sl_points,capital, winners, losers, f"{win_ratio}%",total_profit,f"{total_profit_percentage}%",
                           max_win, max_profit_sum,max_loss, max_loss_sum,ce_trades, pe_trades, self.title]

        
            data = list(zip(parameters, data_points))

            return data
    
            # Print the tabular representation
            # print(tabulate(data, headers=['Parameters', 'Values'], tablefmt='psql'))
    
            # excel_file = "statistics.csv"
            # try:
            #     existing_df = pd.read_csv(excel_file)
            #     new_data = pd.DataFrame([data_points], columns=parameters)
            #     updated_df = pd.concat([existing_df, new_data], ignore_index=True)
            #     updated_df.to_csv(excel_file, index=False)
            # except FileNotFoundError:
            #     new_data = pd.DataFrame([data_points], columns=parameters)
            #     new_data.to_csv(excel_file, index=False)