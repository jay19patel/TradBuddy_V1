import schedule
from datetime import datetime,date
import time
import asyncio
import functools


def market_time_decorator(Open_time="9:14", Close_time="15:15", Interval=60):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = datetime.now().time()
            open_time_dt = datetime.strptime(Open_time, "%H:%M").time()
            close_time_dt = datetime.strptime(Close_time, "%H:%M").time()

            print(open_time_dt , current_time , close_time_dt)
            if open_time_dt <= current_time <= close_time_dt:
                print(f"Algorithm is Online [{func.__name__}]")
                schedule.every(10).seconds.do(func, *args, **kwargs)
            else:
                schedule.clear()
                schedule.every().day.at("09:15").do(func, *args, **kwargs)
                print("Market is closed, scheduling for the next day")
        return wrapper
    return decorator




def Run_at(time_str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            schedule.every().day.at(time_str).do(func, *args, **kwargs)
            print(f"Scheduled {func.__name__} to run at {time_str} every day")
            return func
        return wrapper
    return decorator






