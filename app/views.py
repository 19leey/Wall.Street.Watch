from app import app
from .forms import LoginForm, RegisterForm, TickerForm
from .helper import init_watched_stocks, update_watched_stocks, get_historical, get_quandl_data, get_news
from flask import render_template, flash, redirect, url_for, request, session, logging
from .googlefinance import getQuotes
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

    # get stocks watched by current user
    num_watch = cur.execute("SELECT * FROM stocks WHERE owner = %s", [session['username']])
    tickers = cur.fetchall()

    cur.close()

    stocks = init_watched_stocks(tickers)
    
    return render_template('watchlist.html', form=form, stocks=stocks, num_watch=num_watch)


# Update Watchlist
@app.route('/update_watchlist', methods=['GET', 'POST'])
def update_watchlist():
    cur = mysql.connection.cursor()
    # get stocks watched by current user
    cur.execute("SELECT * FROM stocks WHERE owner = %s", [session['username']])
    stocks = cur.fetchall()
    cur.close()

    data = update_watched_stocks(stocks)

    return data


# Add Stock to Watchlist
@app.route('/add_stock', methods=['POST'])
def add_stock():
    cur = mysql.connection.cursor()

    # get ticker value from form
    search_ticker = request.form['ticker']

    # check that stock exisits and get actual ticker value
    try:
        quote = getQuotes(search_ticker)
        ticker = quote[0]['StockSymbol']
    except urllib.error.HTTPError as err:
        return redirect(url_for('watchlist'))

    # check if stock is already being watched by user
    if cur.execute("SELECT * FROM stocks WHERE ticker = %s AND owner = %s", [ticker, session['username']]) <= 0:

        # insert stock into database
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

    # delete stock from database
    cur.execute("DELETE FROM stocks WHERE ticker = %s AND owner = %s", [ticker, session['username']])

    mysql.connection.commit()

    cur.close()

    return redirect(url_for('watchlist'))


# Stock Details
@app.route('/stock/<string:ticker>')
def stock(ticker):
    quote = getQuotes(ticker)
    data = get_historical(ticker)

    return render_template('stock.html', ticker=ticker, quote=quote, data=data)


# Update Stock
@app.route('/update_stock/<string:ticker>', methods=['GET', 'POST'])
def update_stock(ticker):
    quote = getQuotes(ticker)

    return json.dumps(quote)


# News Feed
@app.route('/news', methods=['GET', 'POST'])
def news():
    cur = mysql.connection.cursor()

    # get stocks watched by user
    cur.execute("SELECT * FROM stocks WHERE owner = %s", [session['username']])
    data = cur.fetchall()

    # get news feed data
    articles = get_news(data)

    return render_template('news.html', articles=articles)


# Update News Feed (WORKING?)
@app.route('/update_news', methods=['GET', 'POST'])
def update_news():
    #cur = mysql.connection.cursor()

    #cur.execute("SELECT * FROM stocks WHERE owner = %s", [session['username']])
    #data = cur.fetchall()

    #articles = get_news(data)

    return redirect('news')


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

        cur.execute("INSERT INTO users(firstname, lastname, email, username, password) VALUES(%s, %s, %s, %s, %s)", 
            (firstname, lastname, email, username, password))

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
    return render_template('temp.html')

