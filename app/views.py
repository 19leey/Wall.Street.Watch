from app import app
from .forms import LoginForm, RegisterForm, TickerForm
from flask import render_template, flash, redirect, url_for, request, session, logging
from .googlefinance import getQuotes
from .helper import initWatchedStocks, updateWatchedStocks, getQuandlData
import urllib.request
import json
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

# Config MySQL
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


# IMPLEMENT SQL DATABASE CONNECTION
from .tmp_stocks import Stocks

# Watchlist
@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    form = TickerForm()
    data = initWatchedStocks(Stocks())
    
    return render_template('watchlist.html', stocks=data, form=form)


# Update Watchlist
@app.route('/updateWatchlist', methods=['GET', 'POST'])
def updateWatchlist():
    data = updateWatchedStocks(Stocks())

    return data


# Stock Details
@app.route('/stock/<string:ticker>')
def stock(ticker):
    quote = getQuotes(ticker)
    data = getQuandlData(ticker)

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
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
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

    return render_template('temp.html', form=form)
