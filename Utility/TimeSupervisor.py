import schedule
from datetime import datetime,date
import time
import asyncio
import functools

import logging
import os
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def time_set_for_next_day(func, *args, **kwargs):

    schedule.clear()
    schedule.every().day.at("09:15").do(func, *args, **kwargs)
    print("Market schedule set for the next day")

def market_time_decorator(**kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargsDec):
            current_time = datetime.now().time()
            open_time = datetime.strptime(kwargs.get("Open_close_time", "9:14"), "%H:%M").time()
            close_time = datetime.strptime(kwargs.get("Close_time", "15:15"), "%H:%M").time()

            if open_time <= current_time <= close_time:
                print(f"Algorithm is Online [{func.__name__}]")
                schedule.every(kwargs.get("Interval", 60)).seconds.do(
                    lambda: time_set_for_next_day(func, *args, **kwargsDec) if datetime.now().time() > close_time else func(*args, **kwargsDec)
                )
            else:
                time_set_for_next_day(func, *args, **kwargsDec)
        return wrapper
    return decorator




def Run_at(time_str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            schedule.every().day.at(time_str).do(func, *args, **kwargs)
            print(f"Scheduled {func.__name__} to run at {time_str} every day")
            logging.info(f"Scheduled {func.__name__} to run at {time_str} every day")
            return func
        return wrapper
    return decorator






