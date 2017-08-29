from .googlefinance import getQuotes
import quandl
import json

# returns inital watched stocks
def initWatchedStocks(watchedStocks):
    stocks = watchedStocks
    data = []

    for stock in stocks:
        data.append(getQuotes(stock['ticker']))

    return data


# returns updated watched stocks
def updateWatchedStocks(watchedStocks):
    stocks = watchedStocks
    data = '';

    for stock in stocks:
        data += json.dumps(getQuotes(stock['ticker']))

    data = data.replace('][', ',')

    return data

# returns historical data from Quandl
def getQuandlData(ticker):
    df = quandl.get('WIKI/' + ticker)
    tmp = df['Close'].to_json()
    data = tmp.replace('"', '').replace(',', '],[').replace('}', ']]').replace('{', '[[').replace(':', ',')

    return data
