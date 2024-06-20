import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Get Microsoft stock data
msft = yf.Ticker("TSLA")
df = msft.history(period="6y")

# Calculate Exponential Moving Averages (EMA)
df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()

# Calculate Moving Average Convergence Divergence (MACD)
df['MACD'] = df['EMA12'] - df['EMA26']

# Calculate MACD Signal Line (EMA of MACD) SIGNAL(SIG)
df['SIG'] = df['MACD'].ewm(span=9, adjust=False).mean()
df['POST'] = df['MACD']-df['SIG']

df = df.loc["20171109":"20221109"]

#defining the variable position to determine whether it's CLOSE = 0 or open and if open BUY=1 and SELL = -1
position = 0
position_arr = []

# Create a 'Pos' column based on MACD and SIG intersection and volume condition
df['Pos'] = ''

for i in range(0,11):
    position_arr.append(0)

for i in range(11, len(df)):
    if(df['Volume'].iloc[i] > df['Volume'].iloc[i-10:i].mean()):
        if (df['POST'].iloc[i] > 0 and df['POST'].iloc[i-1] <0):
            df.at[df.index[i], 'Pos'] = 'BUY'
            position = 1
        elif  (df['POST'].iloc[i] < 0 and df['POST'].iloc[i-1] >0 ):
            df.at[df.index[i], 'Pos'] = 'SELL'
            position = -1
    else:
        if (df['POST'].iloc[i] > 0 and df['POST'].iloc[i - 1] < 0):
            df.at[df.index[i], 'Pos'] = 'buy'
            if(position == -1):
                position = 0
        elif (df['POST'].iloc[i] < 0 and df['POST'].iloc[i - 1] > 0):
            df.at[df.index[i], 'Pos'] = 'sell'
            if(position == 1):
                position = 0
    position_arr.append(position)

df["POS"] = position_arr

if(__name__ == "__main__"):
    # Plot the closing price, MACD, and SIG
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['Close'], label='Closing Price', color='blue')
    plt.plot(df.index, df['MACD'], label='MACD', color='orange')
    plt.plot(df.index, df['SIG'], label='SIG', color='green')

    # Plot Buy and Sell signals
    buy_signals = df[df['Pos'] == 'BUY']
    sell_signals = df[df['Pos'] == 'SELL']
    plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal', alpha=1)
    plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal', alpha=1)

    plt.title('Microsoft Stock Analysis')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()

    plt.show()

    # Print the DataFrame with the 'Pos' column


    print(df[['Close', 'MACD', 'SIG', 'Pos']])