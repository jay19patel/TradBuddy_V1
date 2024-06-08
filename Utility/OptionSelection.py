
import pandas as pd
import requests
from datetime import datetime
import os
import io
import os
import glob



import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def fetch_option_details():
    logging.info("Fetching new Option details from Online")
    spotnames = ['BANKNIFTY', 'FINNIFTY', 'NIFTY', 'SENSEX', 'BANKEX'] 
    # spotnames = ['BANKNIFTY','NIFTY'] 
    nse_fetch = requests.get('https://public.fyers.in/sym_details/NSE_FO.csv')
    bse_fetch = requests.get('https://public.fyers.in/sym_details/BSE_FO.csv')

    nse_df = pd.read_csv(io.StringIO(nse_fetch.text), header=None)
    bse_df = pd.read_csv(io.StringIO(bse_fetch.text), header=None)

    row_df = pd.concat([nse_df, bse_df])
    row_df = row_df[[0,1,3,8,9,13,15,16]]
    column_names = ["ID", "INDEX INFO", "LOT", "TIMESTAMP", "SYMBOL", "INDEX", "STRIKE PRICE", "SIDE"]
    row_df.columns = column_names
    row_df["EXDATETIME"] = pd.to_datetime(row_df["TIMESTAMP"], unit='s').dt.date

    current_date = datetime.now().strftime('%Y-%m-%d')
    filtered_df_row= row_df[row_df['INDEX'].isin(spotnames) & (pd.to_datetime(row_df["TIMESTAMP"], unit='s').dt.date >= datetime.now().date())]
    # If need then remove
    filtered_df = filtered_df_row.copy()

    filtered_df["INDEX"].replace({
        "NIFTY": "NSE:NIFTY50-INDEX",
        "BANKNIFTY": "NSE:NIFTYBANK-INDEX",
        "FINNIFTY": "NSE:NIFTY50-INDEX",
        "BANKEX": "NSE:BANKEX-INDEX",
        "SENSEX": "NSE:SENSEX-INDEX"
        },
        inplace=True)


    [os.remove(file) for file in glob.glob(f"{os.getcwd()}/Records/sym_details_*")]

    file_path = f"{os.getcwd()}/Records/sym_details_{current_date}.csv"
    filtered_df.to_csv(file_path, index=False)
    logging.info(f"Option details Successfully saved to {file_path}") 
 
# Index pass kare to at the money no symbol mali jay
def get_option_for(trad_index, trad_side, price,expiry = 0):
    tred_sp = round(price,-2)
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_path = f"{os.getcwd()}/Records/sym_details_{current_date}.csv"
    if not os.path.exists(file_path):
        fetch_option_details()

    option_df = pd.read_csv(file_path)
    option_df["EXDATETIME"] = pd.to_datetime(option_df["TIMESTAMP"], unit='s').dt.date

    final_data = option_df[
    (option_df["STRIKE PRICE"] == tred_sp)&
    (option_df["EXDATETIME"] >= datetime.now().date()) &
    (option_df["SIDE"] == trad_side) &
    (option_df['INDEX'] == trad_index)
    ]

    if final_data.shape[0] == 0:
        logging.info("Filter Datatable is Not available Some this wrong ")
        return None
    else:
        # expiry = 0 yani ki current next expiry  1 yani ki next 
        return final_data.iloc[expiry].to_dict()


def todays_expiry():
    current_date = datetime.now().strftime('%Y-%m-%d')
    file_path = f"{os.getcwd()}/Records/sym_details_{current_date}.csv"
    if not os.path.exists(file_path):
        fetch_option_details()
    option_df = pd.read_csv(file_path)
    option_df["EXDATETIME"] = pd.to_datetime(option_df["TIMESTAMP"], unit='s').dt.date
    final_data = option_df[option_df["EXDATETIME"] == datetime.now().date()]
    print(" Expiry Indexs",final_data["INDEX"].unique())
    return final_data["INDEX"].unique().tolist()

