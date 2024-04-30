import schedule
from datetime import datetime
import time
import asyncio

def time_set_for_next_day(func):
    schedule.clear()
    schedule.every().day.at("09:15").do(func)
    print("Market schedule set for the next day")

import functools

def market_time_decorator(**kwargs):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargsDec):
            current_time = datetime.now().time()
            if datetime.strptime(kwargsDec.get("Open_time", "00:00"), "%H:%M").time() <= current_time <= datetime.strptime(kwargsDec.get("Close_time", "23:59"), "%H:%M").time() and kwargsDec.get("market_status") == "Open":
                print("Algorithm is Online")
                schedule.every(kwargsDec.get("Interval", 60)).seconds.do(lambda: time_set_for_next_day(func) if datetime.now().time() > datetime.strptime("15:15", "%H:%M").time() else func(*args, **kwargs))
            else:
                schedule.clear()
                schedule.every().day.at("09:15").do(func)
                print("Market is closed, scheduling for the next day")
        return wrapper
    return decorator




