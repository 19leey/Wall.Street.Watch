from app import app
from .forms import LoginForm, RegisterForm, TickerForm
from flask import render_template, flash, redirect, url_for, request, session, logging
from .googlefinance import getQuotes
from .helper import initWatchedStocks, updateWatchedStocks, getQuandlData
import urllib.request
import json
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'wallstreetwatch'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


# Home
@app.route('/')
def home():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Watchlist
@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    form = TickerForm()

    cur = mysql.connection.cursor()

    num_watch = cur.execute("SELECT * FROM stocks")
    tickers = cur.fetchall()

    cur.close()

    stocks = initWatchedStocks(tickers)
    
    return render_template('watchlist.html', form=form, stocks=stocks, num_watch=num_watch)


# Update Watchlist
@app.route('/updateWatchlist', methods=['GET', 'POST'])
def updateWatchlist():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stocks")
    stocks = cur.fetchall()
    cur.close()

    data = updateWatchedStocks(stocks)

    return data


# Add Stock to Watchlist
@app.route('/add_stock', methods=['POST'])
def add_stock():
    cur = mysql.connection.cursor()

    ticker = request.form['ticker']

    if cur.execute("SELECT * FROM stocks WHERE ticker = %s", [ticker]) <= 0:

        try:
            quote = getQuotes(ticker)
        except urllib.error.HTTPError as err:
            return redirect(url_for('watchlist'))

        cur.execute("INSERT INTO stocks(ticker, owner) VALUES(%s, %s)", (ticker, session['username']))
        
        mysql.connection.commit()

        cur.close()

        return redirect(url_for('watchlist'))

    else:
        cur.close()

        return redirect(url_for('watchlist'))


# Remove Stock from Watchlist
@app.route('/remove/<string:ticker>', methods=['POST'])
def remove_stock(ticker):
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM stocks WHERE ticker = %s", [ticker])

    mysql.connection.commit()

    cur.close()

    return redirect(url_for('watchlist'))


# Stock Details
@app.route('/stock/<string:ticker>')
def stock(ticker):
    quote = getQuotes(ticker)
    data = []#getQuandlData(ticker)

    return render_template('stock.html', ticker=ticker, quote=quote, data=data)


# Update Stock
@app.route('/updateStock/<string:ticker>', methods=['GET', 'POST'])
def updateStock(ticker):
    quote = getQuotes(ticker)

    return json.dumps(quote)


# Conenct
@app.route('/connect', methods=['GET', 'POST'])
def connect():
    return render_template('connect.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate():
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password']))

        cur = mysql.connection.cursor()

        cur.execute("INSERT INTO users(firstname, lastname, email, username, password) VALUES(%s, %s, %s, %s, %s)", (firstname, lastname, email, username, password))

        mysql.connection.commit()

        cur.close()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']

        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            data = cur.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('home'))

            else:
                return render_template('login.html', form=form)

            cur.close()

        else:
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


# Logout
@app.route('/logout')
def logout():
    if session['logged_in']:
        session.clear()
        flash('logged out', 'success')

        return redirect(url_for('login'))







# For Purely Testing Purposes Only
@app.route('/test', methods=['GET', 'POST'])
def test():
    form = TickerForm()

    cur = mysql.connection.cursor()

    num_watch = cur.execute("SELECT * FROM stocks")
    stocks = cur.fetchall()

    cur.close()

    return render_template('temp.html', form=form, stocks=stocks, num_watch=num_watch)
