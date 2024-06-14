import requests
import pandas as pd
import json
import time
import os
import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def GetNseData(url):
    headers = {
        'Referer': 'https://www.nseindia.com/',
        'Sec-Ch-Ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    time.sleep(2)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
            logging.warning(f"Failed to retrieve data from {url}, status code: {response.status_code}")
            return None

def OptionChain(fyers_obj):
    IndexNameList = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
    json_data = {}
    for index_name in IndexNameList:
        data = {
            "symbol": index_name,
            "strikecount": 5,
            "timestamp": ""
        }
        response = fyers_obj.optionchain(data=data)
        if response['s'] == "ok":
            option_chain = response['data']['optionsChain'][1:]
            json_data[index_name] = {
                "index_name": response['data']['optionsChain'][0]["symbol"],
                "index_price": round(response['data']['optionsChain'][0]["ltp"], 2),
                "index_price_chng": round(response['data']['optionsChain'][0]["ltpch"], 2),
                "index_price_chng_pr": round(response['data']['optionsChain'][0]["ltpchp"], 2),
                "india_vix": round(response['data']['indiavixData']['ltp'], 2),
                "india_vix_chng": round(response['data']['indiavixData']['ltpch'], 2),
                "india_vix_chng_pr": round(response['data']['indiavixData']['ltpchp'], 2),
                "total_put_oi": round(response["data"]["putOi"], 2),
                "total_call_oi": round(response["data"]["callOi"], 2),
                "5_call_oi_change": round(sum(i['oich'] for i in option_chain if i['option_type'] == "CE"), 2),
                "5_put_oi_change": round(sum(i['oich'] for i in option_chain if i['option_type'] == "PE"), 2),
                "5_call_oi_change_pr": round(sum(i['oichp'] for i in option_chain if i['option_type'] == "CE"), 2),
                "5_put_oi_change_pr": round(sum(i['oichp'] for i in option_chain if i['option_type'] == "PE"), 2),
                "5_pcr_oi": round(response["data"]["putOi"] / response["data"]["putOi"], 2),
                "5_pcr_volume": round(
                    sum(i['volume'] for i in option_chain if i['option_type'] == "PE") /
                    sum(i['volume'] for i in option_chain if i['option_type'] == "CE"), 2
                ) if sum(i['volume'] for i in option_chain if i['option_type'] == "CE") != 0 else 0,
                "5_pcr_oi_chng_pr": round(
                    sum(i['oichp'] for i in option_chain if i['option_type'] == "PE") /
                    sum(i['oichp'] for i in option_chain if i['option_type'] == "CE"), 2
                ) if sum(i['oichp'] for i in option_chain if i['option_type'] == "CE") != 0 else 0,
                "5_total_put_ask": round(sum(i['ask'] for i in option_chain if i['option_type'] == "PE"), 2),
                "5_total_put_bid": round(sum(i['bid'] for i in option_chain if i['option_type'] == "PE"), 2),
                "5_total_call_ask": round(sum(i['ask'] for i in option_chain if i['option_type'] == "CE"), 2),
                "5_total_call_bid": round(sum(i['bid'] for i in option_chain if i['option_type'] == "CE"), 2),
                "5_total_put_volume": round(sum(i['volume'] for i in option_chain if i['option_type'] == "PE"), 2),
                "5_total_call_volume": round(sum(i['volume'] for i in option_chain if i['option_type'] == "CE"), 2)
            }
        else:
            logging.warning(f"Failed to retrieve option chain data for {index_name}")
    return json_data

def FiiDii():
    data = GetNseData("https://www.nseindia.com/api/fiidiiTradeReact")
    if data:
        buying = round(sum([float(i['buyValue']) for i in data]), 2)
        selling = round(sum([float(i['sellValue']) for i in data]), 2)
        netvalue = round(sum([float(i['netValue']) for i in data]), 2)
        date = data[0]['date']
        output = {"Date": date, "Buying": buying, "Selling": selling, "Overall": netvalue}
        return output
    else:
        return {}

def AdvancesDecline():
    IndexNameList = ["NIFTY%20BANK", "NIFTY%2050"]
    adv_dec_data = {}
    for index_name in IndexNameList:
        datarow = GetNseData(f"https://www.nseindia.com/api/equity-stockIndices?index={index_name}")
        if datarow:
            try:
                data = dict(datarow)
                market_status = data['advance']
                df = pd.DataFrame(data['data'])
                listofcolumns = ['symbol', 'pChange']
                df = df[listofcolumns].sort_values(by='pChange')
                adv_dec_data[index_name] = df.to_dict(orient='records')
                adv_dec_data[f"{index_name}_advance"] = market_status
            except:
                logging.warning(f"Failed to retrieve AdvancesDecline for {index_name}")
        else:
            logging.warning(f"Failed to retrieve advance/decline data for {index_name}")
    return adv_dec_data

