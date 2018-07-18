# __Wall Street Watch__
## _a simple web application to track the stock market_
## _built using python and the flask framework_

### Current Features:
* Real-time stock quotes (update every 3 seconds)
	* From Google Finance
* Historical stock data 
	* From Alpha Vantage API and Quandl-WIKI
	* Displayed using Highstocks
* User account system to manage user specific watchlists
	* Maintaied using MySQL
* News feed for watched stocks (RSS)
	* From Yahoo Finance

#### @TODO
* ML to predict trends

### Requirements:
~~~~
python3
Flask
Flask-WTF
Flask-MySQLdb
passlib
demjson
feedparser
quandl
~~~~
