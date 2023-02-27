from flask import Flask
import redis
import pika
import json

r = redis.Redis(host='localhost', port=6379, db=0, password="root")

app = Flask(__name__)

credentials = pika.PlainCredentials('root', 'root')
connection_parameters = pika.ConnectionParameters(
    'localhost', 5672, '/', credentials)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()


def fetchOne(ticker):
    price = r.get(ticker)
    if price is None:
        print(f'Fetching price: {ticker}')
        next(channel.consume(queue='amq.rabbitmq.reply-to',
                             auto_ack=True, inactivity_timeout=0.1))
        channel.basic_publish('', 'fetch', ticker, properties=pika.BasicProperties(
            reply_to='amq.rabbitmq.reply-to'))

        for method, properties, body in channel.consume('amq.rabbitmq.reply-to', auto_ack=True):
            price = handle_message(channel, method, properties, body)
            break
        if price == 'Invalid Ticker':
            r.set(ticker, price, ex=86400)
        else:
            r.set(ticker, price, ex=60)
    else:
        price = price.decode()
        print(f'DB Hit: {ticker}: {price}')
    return {
        'ticker': ticker,
        'price': price,
    }


def handle_message(ch, method, properties, body):
    ch.cancel()
    return body.decode()


@app.route("/api/<list_of_tickers>", methods=['GET'])
def getMany(list_of_tickers):
    list_of_tickers = list_of_tickers.split(',')
    prices_list = []
    for ticker in list_of_tickers:
        prices_list.append(fetchOne(ticker))
    return json.dumps(prices_list)


app.run('0.0.0.0', 5000)
