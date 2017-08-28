from app import app
from .forms import LoginForm, RegisterForm, TickerForm
from flask import render_template, flash, redirect
from .googlefinance import getQuotes
import urllib.request
import quandl
import json

# Home
@app.route('/')
def index():
        #flash('Hello', 'success')
    return render_template('home.html')

# About
@app.route('/about')
def about():
    return render_template('about.html')

# IMPLEMENT SQL DATABASE CONNECTION
from .tmp_stocks import Stocks

# Watchlist
@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    form = TickerForm()

    stocks = Stocks()
    data = []

    for stock in stocks:
        data.append(getQuotes(stock['ticker']))
    
    return render_template('watchlist.html', stocks=data, form=form)

# Update Watchlist
@app.route('/updateWatchlist', methods=['GET', 'POST'])
def updateWatchlist():
    stocks = Stocks()
    data = '';

    for stock in stocks:
        data += json.dumps(getQuotes(stock['ticker']))

    data = data.replace('][', ',')

    val = getQuotes('AAPL')

    return data

# Stock Details
@app.route('/stock/<string:ticker>')
def stock(ticker):
    quote = getQuotes(ticker)

    df = quandl.get('WIKI/' + ticker)
    tmp = df['Close'].to_json()
    data = tmp.replace('"', '').replace(',', '],[').replace('}', ']]').replace('{', '[[').replace(':', ',')

    return render_template('stock.html', ticker=ticker, quote=quote, data=data)

# Update Stock
@app.route('/updateStock/<string:ticker>', methods=['GET', 'POST'])
def updateStock(ticker):
    quote = getQuotes(ticker)

    return json.dumps(quote)

# Select
@app.route('/connect', methods=['GET', 'POST'])
def connect():
    return render_template('connect.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('register.html', form=form)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)





# For Purely Testing Purposes Only
@app.route('/test')
def test():
    quote = getQuotes('AAPL')


    return render_template('temp.html', stock=quote)
