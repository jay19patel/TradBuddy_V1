import schedule
from datetime import datetime
import time
import asyncio

import logging
logging.basicConfig(filename=f"{os.getcwd()}/Records/StrategyManager.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def time_set_for_next_day(func):
    schedule.clear()
    schedule.every().day.at("09:15").do(func)
    logging.INFO("Market schedule set for the next day")

import functools


def market_time_decorator(**kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargsDec):
            current_time = datetime.now().time()
            if datetime.strptime(kwargs.get("Open_close_time", "9:14"), "%H:%M").time() <= current_time <= datetime.strptime(kwargs.get("Close_time", "15:15"), "%H:%M").time() and kwargs.get("market_status") == "Open":
                logging.INFO(f"Algorithm is Online [{func.__name__}]")
                schedule.every(kwargs.get("Interval", 60)).seconds.do(lambda: time_set_for_next_day(func) if datetime.now().time() > datetime.strptime(kwargs.get("Close_time", "15:15"), "%H:%M").time() else func(*args, **kwargsDec))
            else:
                schedule.clear()
                schedule.every().day.at("09:15").do(func)
                logging.INFO("Market is closed, scheduling for the next day")
        return wrapper
    return decorator



