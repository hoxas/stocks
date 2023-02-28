from flask import Flask
import redis
import pika
import json
from flask_cors import CORS
from threading import Thread
import time

r = redis.Redis(host='redis', port=6379, db=0, password="root")


credentials = pika.PlainCredentials('root', 'root')
connection_parameters = pika.ConnectionParameters(
    'rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(connection_parameters)
channel = connection.channel()


def send_heartbeat(connection):
    while True:
        print('sending heartbeat')
        connection.process_data_events()
        time.sleep(50)


heartbeat_thread = Thread(target=send_heartbeat, args=[connection])
heartbeat_thread.start()

connection.process_data_events()


app = Flask(__name__)
CORS(app)


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


@app.route("/api/", methods=['GET'])
def main():
    return "RUNNING"


@app.route("/api/<list_of_tickers>", methods=['GET'])
def getMany(list_of_tickers):
    list_of_tickers = list_of_tickers.split(',')
    prices_list = []
    for ticker in list_of_tickers:
        prices_list.append(fetchOne(ticker))
    return json.dumps(prices_list)


app.run('0.0.0.0', 5000)
