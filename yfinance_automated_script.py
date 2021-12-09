"""
This updates all the csv files stored in stock_data directory.
If user inputs a ticker that is present in stock_data, retrieve it.
If the input ticker is new, download 1 mo of data for that ticker and store in stock_data
"""

# Import package
import schedule

import yfinance as yf
import pandas as pd

def tick_input():
    """
    Gets user input, clean the $ sign, and change it to all uppercase
    """
    tick = str(input('Please enter stock ticker symbol like [$GME]:'))
    # test if it's a valid ticker name
    return tick[1:].upper()

get_tick = ['AMC', 'GME', 'TSLA', 'MSFT', 'AAPL', 'NKLA', 'GOOGL','RIVN', 'FB']


def get_data():
    """
    Get data if already in stock_data. Otherwise,
    store 1 mo of data and add the new ticker to the update list.
    """
    ticker = tick_input()
    if ticker not in get_tick:
        new_data = yf.download(tickers=ticker, period="1mo", interval="15m")
        new_data.to_csv('stock_data/'+ticker+'.csv')
        get_tick.append(ticker)

    return pd.read_csv('stock_data/'+ticker+'.csv')

data = get_data()

def job():
    """
    Scheduled Job that updates the csv files in stock_data daily.

    """
    for ticker in get_tick:
        new_daily = yf.download(tickers=ticker, period="1d", interval="15m")
        old_data = pd.read_csv('stock_data/'+ticker+'.csv', index_col=0)
        # index_col=0 to drop index column

        old_data = old_data.append(new_daily)
        old_data.to_csv('stock_data/'+ticker+'.csv')

schedule.every().day.at("16:00").do(job)
