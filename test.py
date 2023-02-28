import yfinance as yf

stock = yf.Ticker('pfe')
name = stock.info
print(name)
price = stock.fast_info['lastPrice']

print(price)
