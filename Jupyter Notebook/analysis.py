ViewList = ["Datetime", "Day_Prev_Candle_Signal", "Day_Prev_Candle", "Day_RSI", "RSI", "Prev_Candle_Signal", "Prev_Candle", "TradSide"]
row_data = df[df["Datetime"].isin(tk["BuyDatetime"])].merge(tk[["BuyDatetime", "PnL Status"]], left_on="Datetime", right_on="BuyDatetime", how="inner")[ViewList + ["PnL Status"]]



an_side = "CE"
Column_name = "RSI"

import matplotlib.pyplot as plt

# Filter data for the specified trading side and PnL Status
df_loss = row_data[(row_data["TradSide"] == an_side) & (row_data["PnL Status"] == "Loss")]
df_profit = row_data[(row_data["TradSide"] == an_side) & (row_data["PnL Status"] == "Profit")]

# Create a figure and axis for subplots
fig, axs = plt.subplots(1, 2, figsize=(6, 3))

# Plot histograms for the Loss and Profit categories side by side
axs[0].hist(df_loss[Column_name], bins=20, color='red', alpha=0.7)
axs[0].set_title('Loss')
axs[0].set_xlabel(f"{Column_name} {an_side}")
axs[0].set_ylabel('Frequency')

axs[1].hist(df_profit[Column_name], bins=20, color='green', alpha=0.7)
axs[1].set_title('Profit')
axs[1].set_xlabel(f"{Column_name} {an_side}")
axs[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

