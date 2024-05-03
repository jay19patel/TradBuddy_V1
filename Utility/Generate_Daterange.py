from datetime import datetime , timedelta,date

def generate_date_range(day):
    current_date = datetime.now()
    past_date = current_date - timedelta(days=day)  
    date_ranges = []
    while past_date < current_date:
        next_date = past_date + timedelta(days=3*30)
        if next_date > current_date:
            next_date = current_date
        date_ranges.append((past_date, next_date))
        past_date = next_date + timedelta(days=1)
    return date_ranges