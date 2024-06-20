import numpy as np
import main as main
import math
import pandas as pd
import Mathematics as m

# Define the risk-free rate (assumed to be 0%)
risk_free_rate = 0

df = main.df

# Calculate daily returns
df['Daily_Return'] = df['Close'].pct_change()
df['Daily_Return'].fillna(0, inplace=True)



# Calculate portfolio returns and book size
portfolio_returns = [0]
booksize = 10000
booksize_history = [booksize]



for i in range(1, len(df)):
    if df['POS'].iloc[i] == 1:
        booksize += booksize * df['Daily_Return'].iloc[i]
    elif df['POS'].iloc[i] == -1:
        booksize -= booksize * df['Daily_Return'].iloc[i]
    portfolio_returns.append(booksize / 10000)  # Normalize to initial book size
    booksize_history.append(booksize)

#Calculating Actual Returns
series = pd.Series(booksize_history)
Actual_returns = series.pct_change()
Actual_returns.fillna(0, inplace=True)

# Calculate Sharpe Ratio
daily_returns = df['Daily_Return']
sharpe_ratio = (Actual_returns.mean() - risk_free_rate) / Actual_returns.std()
sharpe_ratio_d = (daily_returns.mean()-risk_free_rate)/daily_returns.std()



# Calculate Annualized Return
annualized_return = math.pow((booksize_history[-1])/10000,1/5)-1

# Calculate Benchmark Return (assuming benchmark as a constant return, e.g., 8% annually)
benchmark_return =  2.6322258601429116/100

# Calculate the number of executed trades
executed_trades = len(df[df['POS'] != 0])

# Calculate Maximum Drawdown
if(booksize_history[-1] == max(booksize_history)):
    max_drawdown = (min(booksize_history)- m.find_maximum_maxima(booksize_history))/m.find_maximum_maxima((booksize_history))
max_drawdown = (min(booksize_history)- max(booksize_history))/max(booksize_history)

# Calculate Win Ratio and Loss-Making Trades
positive_returns = Actual_returns[Actual_returns > 0]
negative_returns = Actual_returns[Actual_returns < 0]
win_ratio = len(positive_returns) / (len(positive_returns) + len(negative_returns))
loss_making_trades = len(negative_returns)
profit_making_trades = len(positive_returns)

# Calculate Largest Loss-Making Trade and Largest Profit-Making Trade
largest_loss = np.min(negative_returns)
largest_profit = np.max(positive_returns)

if(__name__ == "__main__"):
    # Print the results
    print("Sharpe Ratio of daily returns : ", sharpe_ratio_d)
    print("Sharpe Ratio of Actual returns : ", sharpe_ratio)
    print("Annualized Return: ", annualized_return*100, "%")
    print("Benchmark Return: ", benchmark_return*100, "%")
    print("Number of Executed Trades: ", executed_trades)
    print("Maximum Drawdown: ", max_drawdown*100,"%")
    print("Win Ratio: ", win_ratio)
    print("Loss-Making Trades: ", loss_making_trades)
    print("Profit-Making Trades: ", profit_making_trades)
    print("Largest Loss-Making Trade: ", largest_loss*100,"%")
    print("Largest Profit-Making Trade: ", largest_profit*100,"%")
    print("Final Booksize: $", booksize_history[-1])
