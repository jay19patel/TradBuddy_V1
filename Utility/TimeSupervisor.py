import schedule
from datetime import datetime,date
import time
import asyncio
import functools



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
                schedule.clear()
                schedule.every().day.at("09:15").do(func, *args, **kwargsDec)
                print("Market is closed, scheduling for the next day")
        return wrapper
    return decorator

@market_time_decorator(Open_close_time="09:14", Close_time="15:15", Interval=60)
def my_function(param1, param2):
    print(f"Function executed with parameters: {param1}, {param2}")

# Example usage
if __name__ == "__main__":
    my_function("param1_value", "param2_value")
    
    while True:
        schedule.run_pending()
        time.sleep(1)



def Run_at(time_str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            schedule.every().day.at(time_str).do(func, *args, **kwargs)
            print(f"Scheduled {func.__name__} to run at {time_str} every day")
            return func
        return wrapper
    return decorator






