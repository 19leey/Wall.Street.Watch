from .googlefinance import getQuotes
import pandas as pd
import quandl
import json
import time

# returns inital watched stocks
def initWatchedStocks(watchedStocks):
    stocks = watchedStocks
    data = []

    # create json array of watched stocks
    for stock in stocks:
        data.append(getQuotes(stock['ticker']))

    return data


# returns updated watched stocks
def updateWatchedStocks(watchedStocks):
    stocks = watchedStocks
    data = '';

    # create json array of watched stocks
    for stock in stocks:
        data += json.dumps(getQuotes(stock['ticker']))

    # manipulate format
    data = data.replace('][', ',')

    return data

# returns historical data from Quandl
def getQuandlData(ticker):
    df = quandl.get('WIKI/' + ticker)
    # manipulate json array format
    tmp = df['Close'].to_json()
    data = tmp.replace('"', '').replace(',', '],[').replace('}', ']]').replace('{', '[[').replace(':', ',')

    return data

# convert timestamp to epoch timestamp in milliseconds
def toEpoch(timestamp):
    pattern = '%Y-%m-%d'
    epoch = int(time.mktime(time.strptime(timestamp, pattern)))
    epoch = epoch*1000

    return epoch

# returns historical data from AlphaVantage API
def getAVHistorical(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&apikey=ZVEQV8BQ2W8K0GPM&outputsize=full&datatype=csv&symbol='+ticker
    df = pd.read_csv(url)

    # manipulate timestamps
    df.set_value(0, 'timestamp', df['timestamp'].iloc[0][:10])

    for x in range(len(df.index)):
        df.set_value(x, 'timestamp', toEpoch(df['timestamp'].iloc[x]))

    # reverse the dataframe
    df = df.iloc[::-1]

    # convert pandas dataframe to array of tuples
    subset = df[['timestamp', 'adjusted_close']]
    array = [tuple(x) for x in subset.values]

    # convert to Highstock array format
    tmp = str(array)
    data = tmp.replace('(', '[').replace(')', ']').replace(' ', '')

    return data
