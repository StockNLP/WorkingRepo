"""
This downloads one month of stock data for the initial 9 tickers
and store them into directory stock_data as csv files.
"""

# Import packages
import os
import yfinance as yf
os.mkdir(os.getcwd()+'/stock_data')
get_tick = ['AMC', 'GME', 'TSLA', 'MSFT', 'AAPL', 'NKLA', 'GOOGL','RIVN', 'FB']


# Get the data
for ticker in get_tick:
    data = yf.download(tickers=ticker, period="1mo", interval="15m")
    data.to_csv('stock_data/'+ticker+'.csv')
