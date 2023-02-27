import yfinance as yf

stock = yf.Ticker('pfe')
price = stock.fast_info['lastPrice']

print(price)
