import schedule
from datetime import datetime
import time
import asyncio

def market_time_decorator(**kwargs):
    def decorator(func):
        async def wrapper():
            current_time = datetime.now().time()
            if datetime.strptime("23:15", "%H:%M").time() <= current_time <= datetime.strptime("23:50", "%H:%M").time() and kwargs.get("market_status") == "Open":
                print("Algorithm is Online")
                await func(**kwargs)
            else:
                schedule.clear()
                schedule.every().day.at("09:15").do(func, **kwargs)
                print("Market is closed, scheduling for the next day")

        return wrapper
    return decorator


@market_time_decorator(market_status="Open")
async def test():
    print("Your function is running with args:")

async def main():
    test()
    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

asyncio.run(main())
