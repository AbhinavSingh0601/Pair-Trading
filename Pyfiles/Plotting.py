import main as mn
import Results as res
import matplotlib.pyplot as plt
import pandas as pd

df = mn.df

# Create a date range for the index
df["Daily Returns"] = res.daily_returns.to_list()
df["Portfolio Returns"] = res.Actual_returns.to_list()
df["BookSize"] = res.booksize_history

df["Portfolio Returns"].fillna(0)

# Set the date range as the index
print(df[["Portfolio Returns"]])

# Plot the closing price, MACD, and SIG
plt.figure(figsize=(12, 6))
#plt.plot(df.index, df['Daily Returns'], label='BookSize', color='blue')
plt.plot(df.index, df['Portfolio Returns'], label='Portfolio Returns', color='orange')
#plt.plot(df.index, df['BookSize'], label='Booksize', color='green')


plt.title('TSLA Stock Analysis')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.grid()

plt.show()


df = df[["Close","EMA12","EMA26","MACD","SIG","POS","Daily_Return","BookSize","Portfolio Returns"]]
df.to_csv("Prices TSLA.csv")