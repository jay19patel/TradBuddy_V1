import pandas as pd
import numpy as np

# Sample OHLC data
data = {'Open': [100, 110, 105],
        'High': [150, 115, 115],
        'Low': [90, 100, 95],
        'Close': [100, 105, 110]}

# Create a DataFrame
df = pd.DataFrame(data)

def calculate_shadow_length(row):
    total_range = row['High'] - row['Low']
    upper_shadow = row['High'] - max(row['Open'], row['Close'])
    lower_shadow = min(row['Open'], row['Close']) - row['Low']
    return upper_shadow / total_range, lower_shadow / total_range

def classify_candle(row):
    upper_shadow_length, lower_shadow_length = calculate_shadow_length(row)
    
    conditions = [
        np.logical_and(upper_shadow_length < 0.2, lower_shadow_length > 0.7),
        np.logical_and(upper_shadow_length > 0.7, lower_shadow_length < 0.2)
    ]
    choices = ["Bullish", "Bearish"]
    
    return np.select(conditions, choices, default="Neutral")

# Apply classification function to each row
df['Classification'] = df.apply(classify_candle, axis=1)

df
